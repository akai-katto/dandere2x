#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os
import time
from dataclasses import dataclass

import imageio
import numpy
import numpy as np
from PIL import Image
from scipy import misc  # pip install Pillow

from dandere2xlib.utils.dandere2x_utils import rename_file, wait_on_file


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

        int_copy = numpy.copy(A[A_slices]).astype(int)  # use 'int_copy' instead of raw array to prevent overflow
        B[B_slices] = numpy.clip(int_copy + scalar, 0, 255).astype(np.uint8)

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


class Frame:
    """
    An image class for Dandere2x that wraps around the numpy library.

    usage:
    frame = Frame()
    frame.load_from_string("input.png")
    frame2 = Frame()
    frame2.copy_image(frame)
    frame3 = frame()
    frame3.create_new(1920,1080)
    """

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

        self.frame = imageio.imread(input_string).astype(np.uint8)
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
            except ValueError:
                logger.info("Value Error")
                loaded = False

    def save_image(self, out_location):
        """
        Save an image with specific instructions depending on it's extension type.
        """
        extension = os.path.splitext(os.path.basename(out_location))[1]

        if 'jpg' in extension:
            jpegsave = self.get_pil_image()
            jpegsave.save(out_location + "temp" + extension, format='JPEG', subsampling=0, quality=100)
            wait_on_file(out_location + "temp" + extension)
            rename_file(out_location + "temp" + extension, out_location)

        else:
            save_image = self.get_pil_image()
            save_image.save(out_location + "temp" + extension, format='PNG')
            wait_on_file(out_location + "temp" + extension)
            rename_file(out_location + "temp" + extension, out_location)

    def get_res(self):
        return (self.width, self.height)

    def get_pil_image(self):
        return Image.fromarray(self.frame.astype(np.uint8))

    def save_image_temp(self, out_location, temp_location):
        """
        Save an image in the "temp_location" folder to prevent another program from accessing the file
        until it's done writing.

        This is done to prevent other parts from using an image until it's entirely done writing.
        """

        self.save_image(temp_location)
        wait_on_file(temp_location)
        rename_file(temp_location, out_location)

    def save_image_quality(self, out_location, quality_per):
        """
        Save an image with JPEG using the JPEG quality-compression ratio. 100 will be the best, while 0 will
        be the worst.
        """

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

    def copy_image(self, frame_other):
        """
        Copy another image into this image using the copy_from numpy command. It seems that numpy affects
        the RGB contents of an image, so when another image needs to be copied, rather than copying the file itself,
        load it into a Frame, copy the Frame, then save the Frame, as opposed to copying the file itself.

        This ensure the images stay consistent temporally.

        """

        if self.height != frame_other.height or self.width != frame_other.width:
            self.logger.error('copy images are not equal')
            self.logger.error(str(self.width) + ' !=? ' + str(frame_other.width))
            self.logger.error(str(self.height) + ' !=? ' + str(frame_other.height))
            raise ValueError('invalid copy image')

        copy_from(frame_other.frame, self.frame, (0, 0), (0, 0),
                  (frame_other.frame.shape[1], frame_other.frame[1].shape[0]))

    def copy_block(self, frame_other, block_size, other_x, other_y, this_x, this_y):
        """
        Check that we can validly copy a block before calling the numpy copy_from method. This way, detailed
        errors are given, rather than numpy just throwing an un-informative error.
        """
        # Check if inputs are valid before calling numpy copy_from
        self.check_if_valid(frame_other, block_size, other_x, other_y, this_x, this_y)

        copy_from(frame_other.frame, self.frame,
                  (other_y, other_x), (this_y, this_x),
                  (this_y + block_size - 1, this_x + block_size - 1))

    def fade_block(self, this_x, this_y, block_size, scalar):
        """
        Apply a scalar value to the RGB values for a given block. The values are then clipped to ensure
        they don't overflow.
        """

        copy_from_fade(self.frame, self.frame,
                       (this_y, this_x), (this_y, this_x),
                       (this_y + block_size - 1, this_x + block_size - 1), scalar)

    def check_if_valid(self, frame_other, block_size, other_x, other_y, this_x, this_y):
        """
        Provide detailed reasons why a copy_block will not work before it's called. This method should access
        every edge case that could prevent copy_block from successfully working.
        """

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

    def create_bleeded_image(self, bleed):
        """
        For residuals processing, pixels may or may not exist when trying to create an residual image based
        off the residual blocks, because of padding. This function will make a larger image, and place the same image
        within the larger image, effectively creating a black bleed around the image itself.

        For example, pretend the series of 1's is a static image

        111
        111
        111

        And we need to get the top left most block, with image padding of one pixel. However, no pixels exist. So we
        create a bleeded image,

        00000
        01110
        01110
        01110
        00000

        Then we can create a residual image of the top left pixel with a padding of one pixel, which would yield

        000
        011
        011

        """

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
