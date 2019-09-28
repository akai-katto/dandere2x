#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import logging
import os

from PIL import Image
from context import Context
from dandere2xlib.core.plugins.correction import correct_image
from dandere2xlib.core.plugins.fade import fade_image
from dandere2xlib.core.plugins.pframe import pframe_image
from dandere2xlib.utils.dandere2x_utils import get_lexicon_value, get_list_from_file, wait_on_file
from wrappers.ffmpeg.ffmpeg import migrate_tracks
from wrappers.frame.asyncframe import AsyncFrameWrite, AsyncFrameRead
from wrappers.frame.frame import Frame


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
    logger = logging.getLogger(__name__)

    # # # ffmpeg piping stuff # # #

    ffmpeg_pipe_encoding = context.ffmpeg_pipe_encoding

    if ffmpeg_pipe_encoding:
        nosound_file = context.nosound_file
        frame_rate = str(context.frame_rate)
        input_file = context.input_file
        output_file = context.output_file
        ffmpeg_dir = context.ffmpeg_dir
        ffmpeg_pipe_encoding_type = context.ffmpeg_pipe_encoding_type

        if ffmpeg_pipe_encoding_type in ["jpeg", "jpg"]:
            vcodec = "mjpeg"
            pipe_format = "JPEG"

        elif ffmpeg_pipe_encoding_type == "png":
            vcodec = "png"
            pipe_format = "PNG"

        else:
            print("  Error: no valid ffmpeg_pipe_encoding_type set. Using jpeg as default")
            vcodec = "mjpeg"
            pipe_format = "JPEG"

        print("\n    WARNING: EXPERIMENTAL FFMPEG PIPING IS ENABLED\n")

        ffmpegpipe = subprocess.Popen([ffmpeg_dir, "-loglevel", "panic", '-y', '-f',
                                       'image2pipe', '-vcodec', vcodec, '-r', frame_rate,
                                       '-i', '-', '-vcodec', 'libx264', '-preset', 'medium',
                                       '-qscale', '5', '-crf', '17',
                                       '-vf', ' pp=hb/vb/dr/fq|32, deband=range=22:blur=false',
                                       '-r', frame_rate, nosound_file],
                                      stdin=subprocess.PIPE)

        # pipe the first merged image as it will not be done afterwards
        wait_on_file(merged_dir + "merged_" + str(1) + extension_type)
        im = Image.open(merged_dir + "merged_" + str(1) + extension_type)

        # best jpeg quality since we won't be saving up disk space
        im.save(ffmpegpipe.stdin, format=pipe_format, quality=100)

    # # #  # # #  # # #  # # #

    # Load the genesis image + the first upscaled image.
    frame_previous = Frame()
    frame_previous.load_from_string_wait(merged_dir + "merged_" + str(1) + extension_type)

    f1 = Frame()
    f1.load_from_string_wait(upscaled_dir + "output_" + get_lexicon_value(6, 1) + ".png")

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

        if not ffmpeg_pipe_encoding:  # ffmpeg piping is disabled, traditional way

            # Write the image in the background for the preformance increase
            output_file_merged = workspace + "merged/merged_" + str(x + 1) + extension_type
            background_frame_write = AsyncFrameWrite(frame_next, output_file_merged)
            background_frame_write.start()

        else:  # ffmpeg piping is enabled

            # Write the image directly into ffmpeg pipe
            im = frame_next.get_pil_image()
            im.save(ffmpegpipe.stdin, format=pipe_format, quality=95)

        #######################################
        # Assign variables for next iteration #
        #######################################

        if not last_frame:
            while not background_frame_load.load_complete:
                wait_on_file(upscaled_dir + "output_" + get_lexicon_value(6, x + 1) + ".png")

            f1 = background_frame_load.loaded_image

        frame_previous = frame_next

        # Ensure the file is loaded for background_frame_load. If we're on the last frame, simply ignore this section
        # Because the frame_count + 1 does not exist.

    if ffmpeg_pipe_encoding:
        ffmpegpipe.stdin.close()
        ffmpegpipe.wait()

        # add the original file audio to the nosound file
        migrate_tracks(context, nosound_file, input_file, output_file)


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

    # by copying the image first as the first step, all the predictive elements like
    # (0,0) -> (0,0) are also coppied
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
