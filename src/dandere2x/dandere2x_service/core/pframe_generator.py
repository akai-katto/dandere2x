import multiprocessing.pool
import random
import time

import numpy
import numpy as np

from dandere2x.dandere2xlib.wrappers.frame.frame import Frame, copy_from
from multiprocessing.pool import ThreadPool, Pool

count = 0
block_size = 60

start = time.time()

f1 = Frame()
f1.load_from_string(
    "C:\\Users\\tylerpc\\Documents\\GitHub\\dandere2x\\src\\workspace\\gui\\subworkspace\\noised_inputs\\frame69.png")

f2 = Frame()
f2.load_from_string(
    "C:\\Users\\tylerpc\\Documents\\GitHub\\dandere2x\\src\\workspace\\gui\\subworkspace\\noised_inputs\\frame70.png")

f2_compressed = Frame()
f2_compressed.load_from_string(
    "C:\\Users\\tylerpc\\Documents\\GitHub\\dandere2x\\src\\workspace\\gui\\subworkspace\\noised_inputs\\frame70.png")

compression_time = time.time()
f2_compressed.compress_frame_for_computations(95)

print(compression_time - time.time())

array_subtracted_squared: np.array = (f2.frame - f1.frame) ** 2
compressed_subtracted_squared: np.array = (f2_compressed.frame - f2.frame) ** 2

matched_mean = np.einsum(
    "ijklm->ik",
    array_subtracted_squared.reshape(
        int(1080/block_size), block_size,
        int(1920/block_size), block_size,
        -1
    ),
    dtype=np.float32,
)

compressed_mean = np.einsum(
    "ijklm->ik",
    compressed_subtracted_squared.reshape(
        int(1080/block_size), block_size,
        int(1920/block_size), block_size,
        -1
    ),
    dtype=np.float32,
)

compared = matched_mean - compressed_mean


copied_image = np.zeros([1080, 1920, 3], dtype=np.uint8)
for y in range(int(1080/block_size)):
    for x in range(int(1920/block_size)):
        if compared[y][x] <= 0:
            copy_from(f1.frame, copied_image,
                      (y * block_size, x * block_size),
                      (y * block_size, x * block_size),
                      (y * block_size + block_size - 1, x * block_size + block_size - 1))

from PIL import Image as im
data = im.fromarray(copied_image)
data.save('gfg_dummy_pic.png')