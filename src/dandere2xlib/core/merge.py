#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os

from context import Context
from dandere2xlib.core.plugins.correction import correct_image
from dandere2xlib.core.plugins.fade import fade_image
from dandere2xlib.core.plugins.pframe import pframe_image
from dandere2xlib.utils.dandere2x_utils import get_lexicon_value, get_list_from_file, wait_on_file
from wrappers.frame.frame import Frame

from wrappers.frame.asyncframe import AsyncFrameWrite, AsyncFrameRead

def merge_loop(context: Context, start_frame: int):
    # load variables from context
    workspace = context.workspace
    upscaled_dir = context.upscaled_dir
    merged_dir = context.merged_dir
    inversion_data_dir = context.inversion_data_dir
    pframe_data_dir = context.pframe_data_dir
    correction_data_dir = context.correction_data_dir
    fade_data_dir = context.fade_data_dir
    frame_count = context.frame_count
    extension_type = context.extension_type
    logger = logging.getLogger(__name__)

    # Load the genesis image + the first upscaled image.

    base = Frame()
    base.load_from_string_wait(merged_dir + "merged_" + str(start_frame) + extension_type)

    f1 = Frame()
    f1.load_from_string_wait(upscaled_dir + "output_" + get_lexicon_value(6, 1) + ".png")

    # When upscaling every frame between start_frame to frame_count, there's obviously no x + 1 at frame_count - 1 .
    # So just make a small note not to load that image. Pretty much load images concurrently until we get to x - 1
    last_frame = False
    for x in range(start_frame, frame_count):
        logger.info("Upscaling frame " + str(x))

        # Check if we're at the last image
        if x == frame_count - 1:
            last_frame = True

        # load the next image ahead of time.

        if not last_frame:
            background_frame_load = AsyncFrameRead(upscaled_dir + "output_" + get_lexicon_value(6, x + 1) + ".png")
            background_frame_load.start()

        # load vectors needed to piece image back together
        prediction_data_list = get_list_from_file(pframe_data_dir + "pframe_" + str(x) + ".txt")
        difference_data_list = get_list_from_file(inversion_data_dir + "inversion_" + str(x) + ".txt")
        correction_data_list = get_list_from_file(correction_data_dir + "correction_" + str(x) + ".txt")
        fade_data_list = get_list_from_file(fade_data_dir + "fade_" + str(x) + ".txt")

        output_file = workspace + "merged/merged_" + str(x + 1) + extension_type

        new_base = make_merge_image(context, f1, base,
                                    prediction_data_list, difference_data_list, correction_data_list, fade_data_list)

        background_frame_write = AsyncFrameWrite(new_base, output_file)
        background_frame_write.start()

        # Assign variables for next iteration
        base = new_base
        # ensure the file is loaded for background_frame_load. If we're on the last frame, the thread will
        # Still be waiting for that image, but just manually close the thread if we're done.
        if not last_frame:
            while not background_frame_load.load_complete:
                wait_on_file(upscaled_dir + "output_" + get_lexicon_value(6, x + 1) + ".png")

            f1 = background_frame_load.loaded_image


# find the last photo to be merged, then start the loop from there
def merge_loop_resume(context: Context):
    workspace = context.workspace
    frame_count = context.frame_count

    logger = logging.getLogger(__name__)
    last_found = frame_count

    # to-do, replace this file with the actual variable for merged
    while last_found > 1:
        exists = os.path.isfile(workspace + os.path.sep + "merged" + os.path.sep + "merged_" + str(last_found) + ".jpg")
        logging.info(workspace + os.path.sep + "merged" + os.path.sep + "merged_" + str(last_found) + ".jpg")

        if not exists:
            last_found -= 1

        elif exists:
            break

    logger.info("resume info: last found: " + str(last_found))
    merge_loop(context, start_frame=last_found)


def make_merge_image(context: Context, frame_inversion: Frame, frame_base: Frame,
                     list_predictive: list, list_differences: list, list_corrections: list, list_fade: list):
    # Load context
    logger = logging.getLogger(__name__)

    out_image = Frame()
    out_image.create_new(frame_base.width, frame_base.height)

    # assess the two cases where out images are either duplicates or a new frame completely
    if not list_predictive and not list_differences:
        out_image.copy_image(frame_inversion)
        return out_image

    if list_predictive and not list_differences:
        out_image.copy_image(frame_base)
        return out_image

    # by copying the image first as the first step, all the predictive elements like
    # (0,0) -> (0,0) are also coppied
    out_image.copy_image(frame_base)

    # run the image through the same plugins IN ORDER it was ran in d2x_cpp
    out_image = pframe_image(context, out_image, frame_base, frame_inversion, list_differences, list_predictive)
    out_image = fade_image(context, out_image, list_fade)
    out_image = correct_image(context, out_image, list_corrections)

    return out_image



# For debugging
def main():
    pass


if __name__ == "__main__":
    main()
