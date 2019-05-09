#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: Dandere2X Merge
Author: CardinalPanda
Date Created: March 22, 2019
Last Modified: April 2, 2019
"""
from dandere2x_core.context import Context
from dandere2x_core.dandere2x_utils import get_lexicon_value
from dandere2x_core.dandere2x_utils import wait_on_text
from wrappers.frame import DisplacementVector
from wrappers.frame import Frame
from dandere2x_core.correction import correct_image
import logging
import os


def make_merge_image(context: Context, frame_inversion: Frame, frame_base: Frame,
                     list_predictive: list, list_differences: list, list_corrections: list,
                     output_location: str):

    # Load context
    block_size = context.block_size
    scale_factor = context.scale_factor
    bleed = context.bleed

    logger = logging.getLogger(__name__)

    predictive_vectors = []
    difference_vectors = []
    out_image = Frame()
    out_image.create_new(frame_base.width, frame_base.height)
    scale_factor = int(scale_factor)

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

    # load list into vector displacements
    for x in range(int(len(list_differences) / 4)):
        difference_vectors.append(DisplacementVector(int(list_differences[x * 4]),
                                                     int(list_differences[x * 4 + 1]),
                                                     int(list_differences[x * 4 + 2]),
                                                     int(list_differences[x * 4 + 3])))
    for x in range(int(len(list_predictive) / 4)):
        predictive_vectors.append(DisplacementVector(int(list_predictive[x * 4]),
                                                     int(list_predictive[x * 4 + 1]),
                                                     int(list_predictive[x * 4 + 2]),
                                                     int(list_predictive[x * 4 + 3])))
    # copy over predictive vectors into new image
    for vector in predictive_vectors:
        out_image.copy_block(frame_base, block_size * scale_factor,
                             vector.x_2 * scale_factor,
                             vector.y_2 * scale_factor,
                             vector.x_1 * scale_factor,
                             vector.y_1 * scale_factor)

    # copy over inversion vectors (the difference images) into new image
    for vector in difference_vectors:
        out_image.copy_block(frame_inversion, block_size * scale_factor,
                             (vector.x_2 * (block_size + bleed * 2)) * scale_factor + (bleed * scale_factor),
                             (vector.y_2 * (block_size + bleed * 2)) * scale_factor + (bleed * scale_factor),
                             vector.x_1 * scale_factor,
                             vector.y_1 * scale_factor)

    out_image = correct_image(context, 5, out_image, list_corrections)
    out_image.save_image(output_location)


def merge_loop(context: Context, start_frame: int):

    # load variables from context
    workspace = context.workspace
    upscaled_dir = context.upscaled_dir
    merged_dir = context.merged_dir
    inversion_data_dir = context.inversion_data_dir
    pframe_data_dir = context.pframe_data_dir
    correction_data_dir = context.correction_data_dir
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
        difference_data = wait_on_text(inversion_data_dir + "inversion_" + str(x) + ".txt")
        prediction_data = wait_on_text(pframe_data_dir + "pframe_" + str(x) + ".txt")
        correction_data = wait_on_text(correction_data_dir + "correction_" + str(x) + ".txt")
        output_file = workspace + "merged/merged_" + str(x + 1) + extension_type

        make_merge_image(context, f1, base, prediction_data,
                         difference_data, correction_data, output_file)


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

def main():
    # merge_loop("/home/linux/Videos/testrun/testrun2/", 120)
    merge_loop_resume("C:\\Users\\windwoz\\Desktop\\workspace\\stealpython\\",
                      "C:\\Users\\windwoz\\Desktop\\workspace\\stealpython\\upscaled\\",
                      "C:\\Users\\windwoz\\Desktop\\workspace\\stealpython\\merged\\",
                      "C:\\Users\\windwoz\\Desktop\\workspace\\stealpython\\inversion_data\\",
                      "C:\\Users\\windwoz\\Desktop\\workspace\\stealpython\\pframe_data\\",
                      120, 30, ".jpg")


if __name__ == "__main__":
    main()
