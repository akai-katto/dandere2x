import os

from context import Context
from wrappers.frame.frame import Frame


# starting from 1 to frame_count, compress each frame.
# if the frame already exists, don't compress it.

def compress_frames(context: Context):
    inputs_dir = context.input_frames_dir
    frame_count = context.frame_count
    compressed_dir = context.compressed_dir
    quality_low = context.quality_low
    extension_type = context.extension_type

    for x in range(1, frame_count + 1):
        if os.path.exists(compressed_dir + "compressed_" + str(x) + ".jpg"):
            continue

        frame = Frame()
        frame.load_from_string(inputs_dir + "frame" + str(x) + extension_type)
        frame.save_image_quality(compressed_dir + "compressed_" + str(x) + ".jpg", quality_low)
