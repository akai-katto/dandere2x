#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

from dandere2xlib.utils.dandere2x_utils import get_list_from_file_wait
from wrappers.frame.frame import DisplacementVector
from wrappers.frame.frame import Frame


# See "corrections.cpp" in dandere2x_cpp for more in depth documentation.

# todo- correction size needs to be added to config file

def correct_image(context, frame_base: Frame, list_correction: list):
    """
    Try and fix some artifact-residuals by using the same image as reference.


    Method Tasks:
        - Load all the vectors for blocks pointing to a block with lower MSE
        - Apply all the vectors to the image to produce a more 'correct' image
    """

    logger = logging.getLogger(__name__)

    # load context
    scale_factor = context.scale_factor

    out_image = Frame()
    out_image.create_new(frame_base.width, frame_base.height)
    out_image.copy_image(frame_base)
    scale_factor = int(scale_factor)
    block_size = context.correction_block_size

    for x in range(int(len(list_correction) / 4)):  # / 4 because each there's 4 data points per block

        # load vector
        vector = DisplacementVector(int(list_correction[x * 4 + 0]),
                                    int(list_correction[x * 4 + 1]),
                                    int(list_correction[x * 4 + 2]),
                                    int(list_correction[x * 4 + 3]))

        # apply vector
        out_image.copy_block(frame_base, block_size * scale_factor,
                             vector.x_2 * scale_factor,
                             vector.y_2 * scale_factor,
                             vector.x_1 * scale_factor,
                             vector.y_1 * scale_factor)

    return out_image


def main():
    block_size = 4
    scale_factor = 2

    frame_base = Frame()
    frame_base.load_from_string("C:\\Users\\windwoz\\Desktop\\image_research\\shelter\\merged2x.jpg")
    list_predictive = get_list_from_file_wait("C:\\Users\\windwoz\\Desktop\\image_research\\shelter\\correction.txt")
    out_location = ("C:\\Users\\windwoz\\Desktop\\image_research\\shelter\\new_correction.jpg")

    correct_image(block_size, scale_factor, frame_base, list_predictive, out_location)


if __name__ == "__main__":
    main()
