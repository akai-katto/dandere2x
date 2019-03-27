import os
import time

import numpy as np
from dataclasses import dataclass
from scipy import misc # pip install Pillow
from Dandere2xUtils import wait_on_file


# fuck this function, lmao
def copy_from(A, B, A_start, B_start, B_end):
    """
    A_start is the index with respect to A of the upper left corner of the overlap
    B_start is the index with respect to B of the upper left corner of the overlap
    B_end is the index of with respect to B of the lower right corner of the overlap
    """
    A_start, B_start, B_end = map(np.asarray, [A_start, B_start, B_end])
    shape = B_end - B_start
    B_slices = tuple(map(slice, B_start, B_end + 1))
    A_slices = tuple(map(slice, A_start, A_start + shape + 1))
    B[B_slices] = A[A_slices]


@dataclass
class DisplacementVector:
    x_1: int
    y_1: int
    x_2: int
    y_2: int


# Custom Wrapper for Numpy to better resemble Java's Image API
# Fuck using numpy for images, lmfao.

class Frame:
    def __init__(self):
        self.frame = ''
        self.width = ''
        self.height = ''
        self.string_name = ''

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

    def load_from_string_wait(self, input_string):
        exists = exists = os.path.isfile(input_string)
        count = 0
        while not exists:
            if count % 1000 == 0:
                print(input_string, " dne")
            exists = os.path.isfile(input_string)
            count += 1
            time.sleep(.2)

        self.load_from_string(input_string)


    # first save under a dif name, then rename
    # to prevent image from being read until finished
    def save_image(self, out_location):
        extension = os.path.splitext(os.path.basename(out_location))[1]

        misc.imsave(out_location + "temp" + extension, self.frame)
        wait_on_file(out_location + "temp" + extension)

        os.rename(out_location + "temp" + extension, out_location)

    def copy_image(self, frame_other):
        copy_from(frame_other.frame, self.frame, (0, 0), (0, 0),
                  (frame_other.frame.shape[1], frame_other.frame[1].shape[0]))

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

    def create_bleeded_image(self, bleed):
        shape = self.frame.shape
        x = shape[0] + bleed + bleed
        y = shape[1] + bleed + bleed

        print(shape[0])
        out_image = np.zeros([x, y, 3], dtype=np.uint8)
        copy_from(self.frame, out_image, (0, 0), (bleed, bleed), (shape[0] + bleed - 1, shape[1] + bleed - 1))

        im_out = Frame()
        im_out.frame = out_image
        im_out.width = out_image.shape[1]
        im_out.height = out_image.shape[0]

        return im_out
