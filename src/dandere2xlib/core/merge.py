#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

from context import Context
from dandere2xlib.core.plugins.correction import correct_image
from dandere2xlib.core.plugins.fade import fade_image
from dandere2xlib.core.plugins.pframe import pframe_image
from dandere2xlib.utils.dandere2x_utils import get_lexicon_value, get_list_from_file, wait_on_file, file_exists
from wrappers.ffmpeg.ffmpeg import migrate_tracks
from wrappers.ffmpeg.pipe import Pipe
from wrappers.frame.asyncframe import AsyncFrameWrite, AsyncFrameRead
from wrappers.frame.frame import Frame


def merge_loop(context: Context):
    """
    Description:
        - This class is the driver for merging all the files that need to be merged together.
          Essentially, it calls the 'make_merge_image' method for every image that needs to be upscaled.
        - Other tasks are to ensure the files exist, async writing for optimizations, as well
          as signalling to other parts of Dandere2x we've finished upscaling.

    Method Tasks:

        - Read / Write files that are used by merge asynchronously.
        - Load the text files containing the vectors needed for 'make_merge_image'
        - Create upscaled images, and sends them to the FFMPEG pipe.
        - Signal to the other parts of dandere2x what frame we've just upscaled through the
          'context.signal_merged_count' variable.


    """

    # load variables from context
    workspace = context.workspace
    upscaled_dir = context.residual_upscaled_dir
    merged_dir = context.merged_dir
    residual_data_dir = context.residual_data_dir
    pframe_data_dir = context.pframe_data_dir
    correction_data_dir = context.correction_data_dir
    fade_data_dir = context.fade_data_dir
    frame_count = context.frame_count
    extension_type = context.extension_type
    nosound_file = context.nosound_file
    logger = logging.getLogger(__name__)

    # # #  # # #  # # #  # # #

    # Create the ffmpeg pipe that Dandere2x will be the output video (minus the sound, since that needs
    # to get migrated separately).
    pipe = Pipe(context, nosound_file)
    pipe.start_pipe_thread()

    # Load the genesis image + the first upscaled image.
    frame_previous = Frame()
    frame_previous.load_from_string_wait(merged_dir + "merged_" + str(1) + extension_type)

    f1 = Frame()
    f1.load_from_string_wait(upscaled_dir + "output_" + get_lexicon_value(6, 1) + ".png")

    pipe.save(frame_previous)

    # When upscaling every frame between start_frame to frame_count, there's obviously no x + 1 at frame_count - 1 .
    # So just make a small note not to load that image. Pretty much load images concurrently until we get to x - 1
    last_frame = False
    for x in range(1, frame_count):

        ###################################
        # Loop-iteration pre-requirements #
        ###################################

        # Check if we're at the last image, which affects the behaviour of the loop.
        if x == frame_count - 1:
            last_frame = True

        # Pre-load the next iteration of the loop image ahead of time, if we're not on the last frame.
        if not last_frame:
            background_frame_load = AsyncFrameRead(upscaled_dir + "output_" + get_lexicon_value(6, x + 1) + ".png")
            background_frame_load.start()

        #######################
        # Loop-iteration Core #
        #######################

        logger.info("Upscaling frame " + str(x))

        # Load the needed vectors to create the merged image.
        prediction_data_list = get_list_from_file(pframe_data_dir + "pframe_" + str(x) + ".txt")
        residual_data_list = get_list_from_file(residual_data_dir + "residual_" + str(x) + ".txt")
        correction_data_list = get_list_from_file(correction_data_dir + "correction_" + str(x) + ".txt")
        fade_data_list = get_list_from_file(fade_data_dir + "fade_" + str(x) + ".txt")

        # Create the actual image itself.
        frame_next = make_merge_image(context, f1, frame_previous,
                                      prediction_data_list, residual_data_list,
                                      correction_data_list, fade_data_list)

        ###############
        # Saving Area #
        ###############

        # Directly write the image to the ffmpeg pipe line.
        pipe.save(frame_next)

        # Manually write the image if we're preserving frames (this is for enthusiasts / debugging).
        if context.preserve_frames:
            output_file = workspace + "merged/merged_" + str(x + 1) + extension_type
            background_frame_write = AsyncFrameWrite(frame_next, output_file)
            background_frame_write.start()

        #######################################
        # Assign variables for next iteration #
        #######################################

        # last_frame + 1 does not exist, so don't load.
        if not last_frame:
            # We need to wait until the next upscaled image exists before we move on.
            while not background_frame_load.load_complete:
                wait_on_file(upscaled_dir + "output_" + get_lexicon_value(6, x + 1) + ".png")

            f1 = background_frame_load.loaded_image

        frame_previous = frame_next

        # Signal to the rest of the dandere2x process we've finished upscaling frame 'x'.
        context.signal_merged_count = x

    pipe.wait_finish_stop_pipe()

    logger.info("Migrating audio tracks from the original video..")

    # todo:
    # There's a bug currently where migrate tracks can fail, so the current work around is to
    # keep trying until migration tracks succeeds. The source of the bug is unknown.
    while not file_exists(context.output_file):
        # add the original file audio to the nosound file
        migrate_tracks(context, context.nosound_file,
                       context.sound_file, context.output_file)

    logger.info("Finished migrating tracks.")


def make_merge_image(context: Context, frame_residual: Frame, frame_previous: Frame,
                     list_predictive: list, list_residual: list, list_corrections: list, list_fade: list):
    """
    This section can best be explained through pictures. A visual way of expressing what 'merging'
    is doing is this section in the wiki.

    https://github.com/aka-katto/dandere2x/wiki/How-Dandere2x-Works#part-2-using-observations-to-save-time

    Inputs:
        - frame(x)
        - frame(x+1)_residual
        - Residual vectors mapping frame(x+1)_residual -> frame(x+1)
        - Predictive vectors mapping frame(x) -> frame(x+1)

    Output:
        - frame(x+1)
    """

    # Load context
    logger = logging.getLogger(__name__)

    out_image = Frame()
    out_image.create_new(frame_previous.width, frame_previous.height)

    # If list_predictive and list_predictive are both empty, then the residual frame is simply the newly produced image.
    if not list_predictive and not list_predictive:
        out_image.copy_image(frame_residual)
        return out_image

    # By copying the image first as the first step, all the predictive elements of the form (x,y) -> (x,y)
    # are also copied. This allows us to ignore copying vectors (x,y) -> (x,y), which prevents redundant copying,
    # thus saving valuable computational time.
    out_image.copy_image(frame_previous)

    ###################
    # Plugins Section #
    ###################

    # Note: Run the plugins in the SAME order it was ran in dandere2x_cpp. If not, it won't work correctly.
    out_image = pframe_image(context, out_image, frame_previous, frame_residual, list_residual, list_predictive)
    out_image = fade_image(context, out_image, list_fade)
    out_image = correct_image(context, out_image, list_corrections)

    return out_image


# For debugging
def main():
    pass


if __name__ == "__main__":
    main()
