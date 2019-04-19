#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: Dandere2X Frame
Author: CardinalPanda
Date Created: March 22, 2019
Last Modified: April 2, 2019

Description: Simplify the Dandere2x by not having to interact with numpy itself.
             All operations on images ideally should be done through the functions here.

             Current Tools:
             - New Image
             - Load Image (can wait on file)
             - Copy Block
             - Copy Image
             - Saving (can overwrite)
"""
from dandere2x_core.dandere2x_utils import rename_file
from dandere2x_core.dandere2x_utils import wait_on_file
from dataclasses import dataclass
from scipy import misc  # pip install Pillow
import logging
import numpy as np
import os
import time
import numpy
from PIL import Image

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
        self.frame = misc.imread(input_string).astype(float)
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

    #save the picture given a specific quality setting
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
        copy_from(frame_other.frame, self.frame, (0, 0), (0, 0),
                  (frame_other.frame.shape[1], frame_other.frame[1].shape[0]))

    # this uses the 'copy_from' function I found on stackoverflow.
    # We have to use this function because using ' for x in range(...) ' is too
    # slow for python, so we have to use specialized functions to copy
    # blocks en masse.

    # This function exists as a wrapper mostly to give detailed errors if something goes wrong,
    # as copy_from won't give any meaningful errors.

    def copy_block(self, frame_other, block_size, other_x, other_y, this_x, this_y):
        if this_x + block_size - 1 > self.width or this_y + block_size - 1 > self.height:
            raise ValueError('Input dimensions invalid for copy block self this too big')

        if other_x + block_size - 1 > frame_other.width or other_y + block_size - 1 > frame_other.height:
            print(int(other_x + block_size - 1), "greater than ", frame_other.width)
            print(int(other_y + block_size - 1), "greater than ", frame_other.height)
            raise ValueError('Input dimensions invalid for copy block other is too big')

        if this_x < 0 or this_y < 0:
            raise ValueError('Input dimensions invalid for copy block')

        if other_x < 0 or other_y < 0:
            raise ValueError('Input dimensions invalid for copy block')

        copy_from(frame_other.frame, self.frame, (other_y, other_x), (this_y, this_x),
                  (this_y + block_size - 1, this_x + block_size - 1))

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
        return numpy.mean( (self.frame - other.frame) ** 2 )

