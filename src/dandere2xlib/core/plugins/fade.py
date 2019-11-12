from dataclasses import dataclass

from wrappers.frame.frame import Frame


# A simple struct to hold the data to produce a fade.
@dataclass
class FadeData:
    x: int
    y: int
    scalar: int


def fade_image(context, frame_base: Frame, list_correction: list):
    """
    Apply a flat scalar to the respective blocks in the image. See "fade.cpp" in dandere2x_cpp for more in depth
    documentation. Roughly

        frame_next = frame_next + scalar

    Although frame_residuals needs to also be transformed

    Method Tasks:
        - Load all the vectors and their scalars into a list
        - Apply the scalar to all the vectors in the image
    """

    # load context
    scale_factor = int(context.scale_factor)
    block_size = int(context.block_size)

    fade_data_size = 3

    for x in range(int(len(list_correction) / fade_data_size)):
        # load vector
        vector = FadeData(int(list_correction[x * fade_data_size + 0]),
                          int(list_correction[x * fade_data_size + 1]),
                          int(list_correction[x * fade_data_size + 2]))
        # apply vector
        frame_base.fade_block(vector.x * scale_factor,
                              vector.y * scale_factor,
                              block_size * scale_factor,
                              vector.scalar)

    # out_image.frame = np.clip(out_image.frame, 0, 255)

    return frame_base
