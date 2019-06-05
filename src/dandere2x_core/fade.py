from dandere2x_core.dandere2x_utils import wait_on_text
from wrappers.frame import Frame
import logging
from dataclasses import dataclass

# A simple struct to hold the data to produce a fade.
@dataclass
class FadeData:
    x: int
    y: int
    scalar: int


def fade_image(context, block_size, frame_base: Frame, list_correction: list):
    logger = logging.getLogger(__name__)

    # load context
    scale_factor = context.scale_factor

    fade_list = []
    out_image = Frame()
    out_image.create_new(frame_base.width, frame_base.height)
    out_image.copy_image(frame_base)
    scale_factor = int(scale_factor)

    for x in range(int(len(list_correction) / 3)):
        fade_list.append(FadeData(int(list_correction[x * 3]),
                                  int(list_correction[x * 3 + 1]),
                                  int(list_correction[x * 3 + 2])))

    # copy over predictive vectors into new image
    for vector in fade_list:
        out_image.fade_block(vector.x * scale_factor,
                             vector.y * scale_factor,
                             block_size * scale_factor,
                             vector.scalar)

    return out_image