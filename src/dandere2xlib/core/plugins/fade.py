import logging
from dataclasses import dataclass

from wrappers.frame.frame import Frame


# See "fade.cpp" in dandere2x_cpp for more in depth documentation.

# A simple struct to hold the data to produce a fade.
@dataclass
class FadeData:
    x: int
    y: int
    scalar: int


def fade_image(context, out_image: Frame, list_correction: list):
    # load context
    scale_factor = int(context.scale_factor)
    logger = logging.getLogger(__name__)

    fade_list = []
    block_size = int(context.block_size)

    fade_data_size = 3

    for x in range(int(len(list_correction) / fade_data_size)):
        fade_list.append(FadeData(int(list_correction[x * fade_data_size + 0]),
                                  int(list_correction[x * fade_data_size + 1]),
                                  int(list_correction[x * fade_data_size + 2])))

    # copy over predictive vectors into new image
    for vector in fade_list:
        out_image.fade_block(vector.x * scale_factor,
                             vector.y * scale_factor,
                             block_size * scale_factor,
                             vector.scalar)

    # out_image.frame = np.clip(out_image.frame, 0, 255)

    return out_image
