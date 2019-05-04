#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: Dandere2X Differences
Author: CardinalPanda
Date Created: March 22, 2019
Last Modified: April 2, 2019
"""
from dandere2x_core.context import Context
from dandere2x_core.dandere2x_utils import get_lexicon_value
from dandere2x_core.dandere2x_utils import wait_on_text
from wrappers.frame import DisplacementVector
from wrappers.frame import Frame
import logging
import math
import os


def make_difference_image(context: Context, raw_frame, list_difference, list_predictive, out_location):
    difference_vectors = []
    buffer = 5
    block_size = context.block_size
    bleed = context.bleed

    # first make a 'bleeded' version of input_frame
    # so we can preform numpy calculations w.o having to catch
    bleed_frame = raw_frame.create_bleeded_image(buffer)

    # if there are no items in 'differences' but have list_predictives
    # then the two frames are identical, so no differences image needed.
    if not list_difference and list_predictive:
        out_image = Frame()
        out_image.create_new(1, 1)
        out_image.save_image(out_location)
        return

    # if there are neither any predictive or inversions
    # then the frame is a brand new frame with no resemblence to previous frame.
    # in this case copy the entire frame over
    if not list_difference and not list_predictive:
        out_image = Frame()
        out_image.create_new(raw_frame.width, raw_frame.height)
        out_image.copy_image(raw_frame)
        out_image.save_image(out_location)
        return

    # turn the list of differences into a list of vectors
    for x in range(int(len(list_difference) / 4)):
        difference_vectors.append(DisplacementVector(int(list_difference[x * 4]), int(list_difference[x * 4 + 1]),
                                                     int(list_difference[x * 4 + 2]), int(list_difference[x * 4 + 3])))

    # size of image is determined based off how many differences there are
    image_size = int(math.sqrt(len(list_difference) / 4) + 1) * (block_size + bleed * 2)
    out_image = Frame()
    out_image.create_new(image_size, image_size)

    # move every block from the complete frame to the differences frame using vectors.
    for vector in difference_vectors:
        out_image.copy_block(bleed_frame, block_size + bleed * 2, vector.x_1 + buffer - bleed,
                             vector.y_1 + buffer + - bleed,
                             vector.x_2 * (block_size + bleed * 2), vector.y_2 * (block_size + bleed * 2))

    out_image.save_image(out_location)


# for printing out what Dandere2x predictive frames are doing
def debug(block_size, frame_base, list_predictive, list_differences, output_location):

    logger = logging.getLogger(__name__)

    predictive_vectors = []
    out_image = Frame()
    out_image.create_new(frame_base.width, frame_base.height)

    if not list_predictive and not list_differences:
        logger.info("list_predictive and not list_differences: true")
        logger.info("Saving inversion image..")

        out_image.save_image(output_location)
        return

    if list_predictive and not list_differences:
        logger.info("list_predictive and not list_differences")
        logger.info("saving last image..")

        out_image.copy_image(frame_base)
        out_image.save_image(output_location)
        return

    # load list into vector displacements
    for x in range(int(len(list_predictive) / 4)):
        predictive_vectors.append(DisplacementVector(int(list_predictive[x * 4]),
                                                     int(list_predictive[x * 4 + 1]),
                                                     int(list_predictive[x * 4 + 2]),
                                                     int(list_predictive[x * 4 + 3])))

    # copy over predictive vectors into new image
    for vector in predictive_vectors:
        out_image.copy_block(frame_base, block_size,
                             vector.x_2, vector.y_2,
                             vector.x_1, vector.y_1)

    out_image.save_image(output_location)


def difference_loop(context, start_frame):

    # load variables from context
    workspace = context.workspace
    differences_dir = context.differences_dir
    inversion_data_dir = context.inversion_data_dir
    pframe_data_dir = context.pframe_data_dir
    input_frames_dir = context.input_frames_dir
    frame_count = context.frame_count
    block_size = context.block_size
    extension_type = context.extension_type
    bleed = context.bleed

    logger = logging.getLogger(__name__)
    logger.info((workspace, start_frame, frame_count, block_size))

    for x in range(start_frame, frame_count):
        f1 = Frame()
        f1.load_from_string_wait(input_frames_dir + "frame" + str(x + 1) + extension_type)
        logger.info("waiting on text")
        logger.info(f1)

        difference_data = wait_on_text(inversion_data_dir + "inversion_" + str(x) + ".txt")
        prediction_data = wait_on_text(pframe_data_dir + "pframe_" + str(x) + ".txt")

        make_difference_image(context, f1, difference_data, prediction_data,
                              differences_dir + "output_" + get_lexicon_value(6, x) + ".png")

        output_file = workspace + "debug/debug" + str(x + 1) + extension_type

        debug(block_size, f1, prediction_data, difference_data, output_file)


def difference_loop_resume(context):
    # load variables from context
    workspace = context.workspace
    differences_dir = context.differences_dir
    inversion_data_dir = context.inversion_data_dir
    pframe_data_dir = context.pframe_data_dir
    input_frames_dir = context.input_frames_dir
    frame_count = context.frame_count
    block_size = context.block_size
    extension_type = context.extension_type
    upscaled_dir = context.upscaled_dir

    logger = logging.getLogger(__name__)

    last_found = frame_count
    while last_found > 1:
        exists = os.path.isfile(
            upscaled_dir + "output_" + get_lexicon_value(6, last_found) + ".png")

        if not exists:
            last_found -= 1

        elif exists:
            break

    last_found -= 1
    logger.info("difference loop last frame found: " + str(last_found))

    difference_loop(context, start_frame=last_found)


def main():
    difference_loop_resume("C:\\Users\\windwoz\\Desktop\\workspace\\stealpython\\",
                           "C:\\Users\\windwoz\\Desktop\\workspace\\stealpython\\differences\\",
                           "C:\\Users\\windwoz\\Desktop\\workspace\\stealpython\\inversion_data\\",
                           "C:\\Users\\windwoz\\Desktop\\workspace\\stealpython\\pframe_data\\",
                           "C:\\Users\\windwoz\\Desktop\\workspace\\stealpython\\inputs\\",
                           120,
                           30,
                           ".jpg")


if __name__ == "__main__":
    main()
