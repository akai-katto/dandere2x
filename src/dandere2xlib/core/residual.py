#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

import math

from context import Context
from dandere2xlib.utils.dandere2x_utils import get_lexicon_value, get_list_from_file
from wrappers.frame.frame import DisplacementVector, Frame


def residual_loop(context):
    """
    Call the 'make_residual_image' method for every image that needs to be made into a residual.

    Method Tasks:
        - Load and wait for the files needed to create a residual image.
        - Call 'make_residual_image' once the needed files exist
    """

    # load variables from context
    workspace = context.workspace
    residual_images_dir = context.residual_images_dir
    residual_data_dir = context.residual_data_dir
    pframe_data_dir = context.pframe_data_dir
    input_frames_dir = context.input_frames_dir
    frame_count = context.frame_count
    block_size = context.block_size
    extension_type = context.extension_type
    debug_dir = context.debug_dir
    debug = context.debug

    temp_image = context.temp_image_folder + "tempimage.jpg"

    logger = logging.getLogger(__name__)
    logger.info((workspace, 1, frame_count, block_size))

    # for every frame in the video, create a residual_frame given the text files.
    for x in range(1, frame_count):
        f1 = Frame()
        f1.load_from_string_wait(input_frames_dir + "frame" + str(x + 1) + extension_type)

        # Load the neccecary lists to compute this iteration of residual making
        residual_data = get_list_from_file(residual_data_dir + "residual_" + str(x) + ".txt")
        prediction_data = get_list_from_file(pframe_data_dir + "pframe_" + str(x) + ".txt")

        # Create the output files..
        debug_output_file = debug_dir + "debug" + str(x + 1) + extension_type
        output_file = residual_images_dir + "output_" + get_lexicon_value(6, x) + ".jpg"

        # Save to a temp folder so waifu2x-vulkan doesn't try reading it, then move it
        out_image = make_residual_image(context, f1, residual_data, prediction_data)
        out_image.save_image_temp(output_file, temp_image)

        if debug == 1:
            debug_image(block_size, f1, prediction_data, residual_data, debug_output_file)


def make_residual_image(context: Context, raw_frame: Frame, list_residual: list, list_predictive: list):
    """
    This section can best be explained through pictures. A visual way of expressing what 'make_residual_image'
    is doing is this section in the wiki.

    https://github.com/aka-katto/dandere2x/wiki/How-Dandere2x-Works#observation_3

    Inputs:
        - frame(x)
        - Residual vectors mapping frame(x)_residual -> frame(x)

    Output:
        - frame(x)_residual
    """

    residual_vectors = []
    buffer = 5
    block_size = context.block_size
    bleed = context.bleed

    # first make a 'bleeded' version of input_frame, as we need to create a buffer in the event the 'bleed'
    # ends up going out of bounds.
    bleed_frame = raw_frame.create_bleeded_image(buffer)

    # if there are no items in 'list_residuals' but have list_predictives
    # then the two frames are identical, so no residual image needed.
    if not list_residual and list_predictive:
        out_image = Frame()
        out_image.create_new(1, 1)
        return out_image

    # if there are neither any predictive or inversions
    # then the frame is a brand new frame with no resemblence to previous frame.
    # in this case copy the entire frame over
    if not list_residual and not list_predictive:
        out_image = Frame()
        out_image.create_new(raw_frame.width, raw_frame.height)
        out_image.copy_image(raw_frame)
        return out_image

    # size of output image is determined based off how many residuals there are
    image_size = int(math.sqrt(len(list_residual) / 4) + 1) * (block_size + bleed * 2)
    out_image = Frame()
    out_image.create_new(image_size, image_size)


    for x in range(int(len(list_residual) / 4)):
        vector = DisplacementVector(int(list_residual[x * 4 + 0]),
                                    int(list_residual[x * 4 + 1]),
                                    int(list_residual[x * 4 + 2]),
                                    int(list_residual[x * 4 + 3]))

        out_image.copy_block(bleed_frame, block_size + bleed * 2,
                             vector.x_1 + buffer - bleed, vector.y_1 + buffer + - bleed,
                             vector.x_2 * (block_size + bleed * 2), vector.y_2 * (block_size + bleed * 2))

    return out_image


def debug_image(block_size, frame_base, list_predictive, list_differences, output_location):
    """
    Note:
        I haven't made an effort to maintain this method, as it's only for debugging.

    This section can best be explained through pictures. A visual way of expressing what 'debug'
    is doing is this section in the wiki.

    https://github.com/aka-katto/dandere2x/wiki/How-Dandere2x-Works#part-1-identifying-what-needs-to-be-drawn

    In other words, this method shows where residuals are, and is useful for finding good settings to use for a video.

    Inputs:
        - frame(x)
        - Residual vectors mapping frame(x)_residual -> frame(x)

    Output:
        - frame(x) minus frame(x)_residuals = debug_image
    """
    logger = logging.getLogger(__name__)

    difference_vectors = []
    predictive_vectors = []
    out_image = Frame()
    out_image.create_new(frame_base.width, frame_base.height)
    out_image.copy_image(frame_base)

    black_image = Frame()
    black_image.create_new(frame_base.width, frame_base.height)

    if not list_predictive and not list_differences:
        out_image.save_image(output_location)
        return

    if list_predictive and not list_differences:
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
        if (int(list_predictive[x * 4 + 0]) != int(list_predictive[x * 4 + 1])) and \
                (int(list_predictive[x * 4 + 2]) != int(list_predictive[x * 4 + 3])):
            predictive_vectors.append(DisplacementVector(int(list_predictive[x * 4 + 0]),
                                                         int(list_predictive[x * 4 + 1]),
                                                         int(list_predictive[x * 4 + 2]),
                                                         int(list_predictive[x * 4 + 3])))

    # copy over predictive vectors into new image
    for vector in difference_vectors:
        out_image.copy_block(black_image, block_size,
                             vector.x_1, vector.y_1,
                             vector.x_1, vector.y_1)

    out_image.save_image_quality(output_location, 25)
