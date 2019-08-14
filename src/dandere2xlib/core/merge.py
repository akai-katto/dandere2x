#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: Dandere2X Merge
Author: CardinalPanda
Date Created: March 22, 2019
Last Modified: April 2, 2019
"""
import logging
import os

from context import Context
from dandere2xlib.core.correction import correct_image
from dandere2xlib.utils.dandere2x_utils import get_lexicon_value
from dandere2xlib.utils.dandere2x_utils import get_list_from_file
from dandere2xlib.core.fade import fade_image
from dandere2xlib.core.pframe import pframe_image
from wrappers.frame import Frame

import time

# todo - clean this function up into a few smaller functions.
def make_merge_image(context: Context, frame_inversion: Frame, frame_base: Frame,
                     list_predictive: list, list_differences: list, list_corrections: list, list_fade: list,
                     output_location: str):
    # Load context
    logger = logging.getLogger(__name__)

    out_image = Frame()
    out_image.create_new(frame_base.width, frame_base.height)

    if not list_predictive and not list_differences:
        logger.info("list_predictive and not list_differences: true")
        logger.info("Saving inversion image..")
        out_image.copy_image(frame_inversion)
        out_image.save_image(output_location)
        return

    if list_predictive and not list_differences:
        logger.info("list_predictive and not list_differences")
        logger.info("saving last image..")
        out_image.copy_image(frame_base)
        out_image.save_image(output_location)
        return

    # by copying the image first as the first step, all the predictive elements like
    # (0,0) -> (0,0) are also coppied
    out_image.copy_image(frame_base)

    out_image = pframe_image(context, out_image, frame_base, frame_inversion, list_differences, list_predictive)
    out_image = fade_image(context, int(context.block_size), out_image, list_fade)
    out_image = correct_image(context, 2, out_image, list_corrections)

    out_image.save_image(output_location)



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

    for x in range(start_frame, frame_count):
        logger.info("Upscaling frame " + str(x))

        # load images required to merge this frame
        f1 = Frame()
        f1.load_from_string_wait(upscaled_dir + "output_" + get_lexicon_value(6, x) + ".png")

        base = Frame()
        base.load_from_string_wait(merged_dir + "merged_" + str(x) + extension_type)

        # load vectors needed to piece image back together
        prediction_data_list = get_list_from_file(pframe_data_dir + "pframe_" + str(x) + ".txt")
        difference_data_list = get_list_from_file(inversion_data_dir + "inversion_" + str(x) + ".txt")
        correction_data_list = get_list_from_file(correction_data_dir + "correction_" + str(x) + ".txt")
        fade_data_list = get_list_from_file(fade_data_dir + "fade_" + str(x) + ".txt")

        output_file = workspace + "merged/merged_" + str(x + 1) + extension_type

        make_merge_image(context, f1, base, prediction_data_list,
                         difference_data_list, correction_data_list, fade_data_list, output_file)


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


# For debugging
def main():
    pass


if __name__ == "__main__":
    main()
