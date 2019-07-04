#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: Dandere2X Frame
Author: CardinalPanda
Date Created: March 22, 2019
Last Modified: 6-3-19

Description: Simplify the Dandere2x by not having to interact with numpy itself.
             All operations on images ideally should be done through the functions here.

             Current Tools:
             - New Image
             - Load Image (can wait on file)
             - Copy Block
             - Copy Image
             - Saving (can overwrite)
"""
import logging
import os
import time
from dataclasses import dataclass

import numpy
import numpy as np
from PIL import Image
from scipy import misc  # pip install Pillow

from dandere2x_core.dandere2x_utils import rename_file
from dandere2x_core.dandere2x_utils import wait_on_file


# fuck this function, lmao. Credits to
# https://stackoverflow.com/questions/52702809/copy-array-into-part-of-another-array-in-numpy
def copy_from(A, B, A_start, B_start, B_end):
    """
    A_start is the index with respect to A of the upper left corner of the overlap
    B_start is the index with respect to B of the upper left corner of the overlap
    B_end is the index of with respect to B of the lower right corner of the overlap
    """
    try:
        A_start, B_start, B_end = map(np.asarray, [A_start, B_start, B_end])
        shape = B_end - B_start
        B_slices = tuple(map(slice, B_start, B_end + 1))
        A_slices = tuple(map(slice, A_start, A_start + shape + 1))
        B[B_slices] = A[A_slices]

    except ValueError:
        logging.info("fatal error copying block")
        raise ValueError


# we need to parse the new input into a non uint8 format so it doesnt overflow,
# then parse it back to an integer using np.clip to make it fit within [0,255]
# If we don't do this,  numpy will overflow it for us and give us bad results.

def copy_from_fade(A, B, A_start, B_start, B_end, scalar):
    """
    A_start is the index with respect to A of the upper left corner of the overlap
    B_start is the index with respect to B of the upper left corner of the overlap
    B_end is the index of with respect to B of the lower right corner of the overlap
    """
    try:
        A_start, B_start, B_end = map(np.asarray, [A_start, B_start, B_end])
        shape = B_end - B_start
        B_slices = tuple(map(slice, B_start, B_end + 1))
        A_slices = tuple(map(slice, A_start, A_start + shape + 1))

        copy = numpy.copy(A[A_slices]).astype(int)
        B[B_slices] = numpy.clip(copy + scalar, 0, 255).astype(np.uint8)

    except ValueError:
        logging.info("fatal error copying block")
        raise ValueError


# A vector class
@dataclass
class DisplacementVector:
    x_1: int
    y_1: int
    x_2: int
    y_2: int


# usage:
# frame = Frame()
# frame.load_from_string("input.png")
# frame2 = Frame()
# frame2.copy_image(frame)
# frame3 = frame()
# frame3.create_new(1920,1080)

class Frame:
    def __init__(self):
        self.frame = ''
        self.width = ''
        self.height = ''
        self.string_name = ''
        self.logger = logging.getLogger(__name__)

    def create_new(self, width, height):
        self.frame = np.zeros([height, width, 3], dtype=np.uint8)
        self.width = width
        self.height = height
        self.string_name = ''

    def load_from_string(self, input_string):
        self.frame = misc.imread(input_string).astype(np.uint8)
        self.height = self.frame.shape[0]
        self.width = self.frame.shape[1]
        self.string_name = input_string

    # Wait on a file if it does not exist yet.

    def load_from_string_wait(self, input_string):
        logger = logging.getLogger(__name__)
        exists = exists = os.path.isfile(input_string)
        count = 0
        while not exists:
            if count % 10000 == 0:
                logger.info(input_string + " dne")
            exists = os.path.isfile(input_string)
            count += 1
            time.sleep(.2)

        loaded = False
        while not loaded:
            try:
                self.load_from_string(input_string)
                loaded = True
            except PermissionError:
                logger.info("Permission Error")
                loaded = False

    # Save an image, then rename it. This prevents other parts of Dandere2x
    # from accessing an image file that hasn't finished saving.
    # Have to convert image using Pillow before saving to get Quality = 100
    # for jpeg output
    def save_image(self, out_location):
        extension = os.path.splitext(os.path.basename(out_location))[1]

        if 'jpg' in extension:
            jpegsave = Image.fromarray(self.frame.astype(np.uint8))
            jpegsave.save(out_location + "temp" + extension, format='JPEG', subsampling=0, quality=100)
            wait_on_file(out_location + "temp" + extension)
            rename_file(out_location + "temp" + extension, out_location)

        else:
            misc.imsave(out_location + "temp" + extension, self.frame)
            wait_on_file(out_location + "temp" + extension)
            rename_file(out_location + "temp" + extension, out_location)

    # save the picture given a specific quality setting

    def save_image_quality(self, out_location, quality_per):
        extension = os.path.splitext(os.path.basename(out_location))[1]

        if 'jpg' in extension:
            jpegsave = Image.fromarray(self.frame.astype(np.uint8))
            jpegsave.save(out_location + "temp" + extension, format='JPEG', subsampling=0, quality=quality_per)
            wait_on_file(out_location + "temp" + extension)
            rename_file(out_location + "temp" + extension, out_location)
        else:
            misc.imsave(out_location + "temp" + extension, self.frame)
            wait_on_file(out_location + "temp" + extension)
            rename_file(out_location + "temp" + extension, out_location)

    # This function exists because the act of numpy processing an image
    # changes the overall look of an image. (I guess?). In the case
    # where Dandere2x needs to just load an image and save it somewhere else,
    # Dandere2x needs to copy the image using numpy to maintain visual aesthetic.

    def copy_image(self, frame_other):
        if self.height != frame_other.height or self.width != frame_other.width:
            self.logger.error('copy images are not equal')
            self.logger.error(str(self.width) + ' !=? ' + str(frame_other.width))
            self.logger.error(str(self.height) + ' !=? ' + str(frame_other.height))
            raise ValueError('invalid copy image')

        copy_from(frame_other.frame, self.frame, (0, 0), (0, 0),
                  (frame_other.frame.shape[1], frame_other.frame[1].shape[0]))

    # this uses the 'copy_from' function I found on stackoverflow.
    # We have to use this function because using ' for x in range(...) ' is too
    # slow for python, so we have to use specialized functions to copy blocks en masse.

    # This function exists as a wrapper mostly to give detailed errors if something goes wrong,
    # as copy_from won't give any meaningful errors.

    def copy_block(self, frame_other, block_size, other_x, other_y, this_x, this_y):

        # Check if inputs are valid before calling numpy copy_from
        self.check_if_valid(frame_other, block_size, other_x, other_y, this_x, this_y)

        copy_from(frame_other.frame, self.frame,
                  (other_y, other_x), (this_y, this_x),
                  (this_y + block_size - 1, this_x + block_size - 1))

    # Similar to copy_block, fade_block applies some scalar value to every
    # pixel within a block range.

    def fade_block(self, this_x, this_y, block_size, scalar):

        #temp = numpy.copy(self.frame).astype(int)

        copy_from_fade(self.frame, self.frame,
                       (this_y, this_x), (this_y, this_x),
                       (this_y + block_size - 1, this_x + block_size - 1), scalar)

        # temp = np.clip(temp, 0, 255).astype(np.uint8)
        #
        # self.frame = temp



    # For the sake of code maintance, do the error checking to ensure numpy copy will work here.
    # Numpy won't give detailed errors, so this is my custom errors for debugging!

    def check_if_valid(self, frame_other, block_size, other_x, other_y, this_x, this_y):

        if this_x + block_size - 1 > self.width or this_y + block_size - 1 > self.height:
            self.logger.error('Input Dimensions Invalid for Copy Block Function, printing variables. Send Tyler this!')

            # Print Out Degenerate Values
            self.logger.error('this_x + block_size - 1 > self.width')
            self.logger.error(str(this_x + block_size - 1) + '?>' + str(self.width))

            self.logger.error('this_y + block_size - 1 > self.height')
            self.logger.error(str(this_y + block_size - 1) + '?>' + str(self.height))

            raise ValueError('Invalid Dimensions for Dandere2x Image, See Log. ')

        if other_x + block_size - 1 > frame_other.width or other_y + block_size - 1 > frame_other.height:
            self.logger.error('Input Dimensions Invalid for Copy Block Function, printing variables. Send Tyler this!')

            # Print Out Degenerate Values
            self.logger.error('other_x + block_size - 1 > frame_other.width')
            self.logger.error(str(other_x + block_size - 1) + '?>' + str(frame_other.width))

            self.logger.error('other_y + block_size - 1 > frame_other.height')
            self.logger.error(str(other_y + block_size - 1) + '?>' + str(frame_other.height))

            raise ValueError('Invalid Dimensions for Dandere2x Image, See Log. ')

        if this_x < 0 or this_y < 0:
            self.logger.error('Negative Input for \"this\" image')
            self.logger.error('x' + this_x)
            self.logger.error('y' + this_y)

            raise ValueError('Input dimensions invalid for copy block')

        if other_x < 0 or other_y < 0:
            raise ValueError('Input dimensions invalid for copy block')

    # Sometimes we need to copy a block + some bleed as a result of Waifu2x Bleeding. (see documentation).
    # Sometimes this bleed may or may not actually exist, in which case just put a color like black or something.
    # This function creates an image 'bleed' pixels larger than the original image, as to avoid
    # accessing pixels that may not exist.

    def create_bleeded_image(self, bleed):
        shape = self.frame.shape
        x = shape[0] + bleed + bleed
        y = shape[1] + bleed + bleed
        out_image = np.zeros([x, y, 3], dtype=np.uint8)
        copy_from(self.frame, out_image, (0, 0), (bleed, bleed), (shape[0] + bleed - 1, shape[1] + bleed - 1))

        im_out = Frame()
        im_out.frame = out_image
        im_out.width = out_image.shape[1]
        im_out.height = out_image.shape[0]

        return im_out

    def mean(self, other):
        return numpy.mean((self.frame - other.frame) ** 2)
