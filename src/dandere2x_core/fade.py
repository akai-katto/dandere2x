import logging
from dataclasses import dataclass

from wrappers.frame import Frame


# A simple struct to hold the data to produce a fade.
@dataclass
class FadeData:
    x: int
    y: int
    scalar: int


# comments: I'm not sure if we need to create a new frame, but it's not causing
# preformance issues so far, and this solution is easier for me to debug knowing that it creates
# a copy than reassigns. Perhaps someone can test if we can just edit the input rather than
# change the fade.

def fade_image(context, block_size, frame_base: Frame, list_correction: list):
    logger = logging.getLogger(__name__)

    # load context
    scale_factor = int(context.scale_factor)

    fade_list = []
    out_image = Frame()
    out_image.create_new(frame_base.width, frame_base.height)
    out_image.copy_image(frame_base)

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
