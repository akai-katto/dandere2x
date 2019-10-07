#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import subprocess

from PIL import Image

from context import Context
from dandere2xlib.core.plugins.correction import correct_image
from dandere2xlib.core.plugins.fade import fade_image
from dandere2xlib.core.plugins.pframe import pframe_image
from dandere2xlib.utils.dandere2x_utils import get_lexicon_value, get_list_from_file, wait_on_file, file_exists
from wrappers.ffmpeg.ffmpeg import migrate_tracks
from wrappers.frame.asyncframe import AsyncFrameWrite, AsyncFrameRead
from wrappers.frame.frame import Frame
from dandere2xlib.utils.yaml_utils import get_options_from_section
from wrappers.ffmpeg.pipe import Pipe


def merge_loop(context: Context):
    """
    Call the 'make_merge_image' method for every image that needs to be upscaled.

    This method is sort of the driver for that, and has tasks needed to keep merging running smoothly.

    This method became a bit messy due to optimization-hunting, but the most important calls of the loop can be read in
    the 'Loop-iteration Core' area.

    Method Tasks:

        - Read / Write files that are used by merge asynchronously.
        - Load the text files containing the vectors needed for 'make_merge_image'

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

    # create the pipe that Dandere2x will use to store the outputs of the video.
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

        # Check if we're at the last image
        if x == frame_count - 1:
            last_frame = True

        # load the next image ahead of time.
        if not last_frame:
            background_frame_load = AsyncFrameRead(upscaled_dir + "output_" + get_lexicon_value(6, x + 1) + ".png")
            background_frame_load.start()

        #######################
        # Loop-iteration Core #
        #######################

        logger.info("Upscaling frame " + str(x))

        prediction_data_list = get_list_from_file(pframe_data_dir + "pframe_" + str(x) + ".txt")
        residual_data_list = get_list_from_file(residual_data_dir + "residual_" + str(x) + ".txt")
        correction_data_list = get_list_from_file(correction_data_dir + "correction_" + str(x) + ".txt")
        fade_data_list = get_list_from_file(fade_data_dir + "fade_" + str(x) + ".txt")

        frame_next = make_merge_image(context, f1, frame_previous,
                                      prediction_data_list, residual_data_list,
                                      correction_data_list, fade_data_list)

        pipe.save(frame_next)

        if context.preserve_frames:
            output_file = workspace + "merged/merged_" + str(x + 1) + extension_type
            background_frame_write = AsyncFrameWrite(frame_next, output_file)
            background_frame_write.start()

        #######################################
        # Assign variables for next iteration #
        #######################################

        if not last_frame:
            while not background_frame_load.load_complete:
                wait_on_file(upscaled_dir + "output_" + get_lexicon_value(6, x + 1) + ".png")

            f1 = background_frame_load.loaded_image

        frame_previous = frame_next
        context.signal_merged_count = x

        # Ensure the file is loaded for background_frame_load. If we're on the last frame, simply ignore this section
        # Because the frame_count + 1 does not exist.

    pipe.wait_finish_stop_pipe()

    logger.info("Migrating audio tracks from the original video..")

    while not file_exists(context.output_file):
        # add the original file audio to the nosound file
        migrate_tracks(context, context.nosound_file,
                       context.input_file, context.output_file)

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

    # If list_predictive and list_predictive are both empty, then the residual frame
    # is simply the new image.
    if not list_predictive and not list_predictive:
        out_image.copy_image(frame_residual)
        return out_image

    # by copying the image first as the first step, all the predictive
    # elements of the form (x,y) -> (x,y) are also copied
    out_image.copy_image(frame_previous)

    # run the image through the same plugins IN ORDER it was ran in d2x_cpp
    out_image = pframe_image(context, out_image, frame_previous, frame_residual, list_residual, list_predictive)
    out_image = fade_image(context, out_image, list_fade)
    out_image = correct_image(context, out_image, list_corrections)

    return out_image


# For debugging
def main():
    pass


if __name__ == "__main__":
    main()
