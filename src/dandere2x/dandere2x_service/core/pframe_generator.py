import multiprocessing.pool
import random
import time

import numpy
import numpy as np

from dandere2x.dandere2xlib.wrappers.frame.frame import Frame, copy_from
from multiprocessing.pool import ThreadPool, Pool

count = 0

f1 = Frame()
f1.load_from_string(
    "C:\\Users\\windw0z\\Documents\\GitHub\\dandere2x\\src\\workspace\\gui\\subworkspace\\inputs\\frame39.png")

f2 = Frame()
f2.load_from_string(
    "C:\\Users\\windw0z\\Documents\\GitHub\\dandere2x\\src\\workspace\\gui\\subworkspace\\inputs\\frame40.png")

f2_compressed = Frame()
f2_compressed.load_from_string(
    "C:\\Users\\windw0z\\Documents\\GitHub\\dandere2x\\src\\workspace\\gui\\subworkspace\\inputs\\frame41.png")

array_subtracted_squared: np.array = (f2.frame - f1.frame) ** 2

compressed_subtracted_squared: np.array = (f2_compressed.frame - f2.frame) ** 2


def process_mse_blocks(block_size: int):
    list_of_args = []
    start = time.time()
    for x in range(int(1920 / block_size)):
        for y in range(int(1080 / block_size)):
            some_block = np.zeros([block_size, block_size, 3], dtype=np.uint8)
            copy_from(array_subtracted_squared, some_block, (y, x), (0, 0), (block_size - 1, block_size - 1))

    print(time.time() - start)


def process_block(pos, block_size, image):
    x, y = pos

    some_block = np.zeros([block_size, block_size, 3], dtype=np.uint8)
    copy_from(image, some_block, (y, x), (0, 0), (block_size - 1, block_size - 1))
    return np.mean(some_block)


def divide_frame(xy_tupe, block, matched_blocks, missing_blocks):
    x, y = xy_tupe

    f1f2_mse = process_block((x, y), block, array_subtracted_squared)
    f2compressed_mse = process_block((x, y), block, compressed_subtracted_squared)

    if f1f2_mse <= f2compressed_mse:
        matched_blocks.append((x, y, block))
        return
    else:
        missing_blocks.append((x, y, block))

    smaller_block = int(block / 2)
    if smaller_block < 15:
        return

    first_start = (x, y)
    third_start = (x, y + smaller_block)
    forth_start = (x + smaller_block, y)
    second_start = (x + smaller_block, y + smaller_block)

    divide_frame(first_start, smaller_block, matched_blocks, missing_blocks)
    divide_frame(second_start, smaller_block, matched_blocks, missing_blocks)
    divide_frame(third_start, smaller_block, matched_blocks, missing_blocks)
    divide_frame(forth_start, smaller_block, matched_blocks, missing_blocks)


def divide_frame_driver():
    pass


def main():
    matched_blocks = []
    missing_blocks = []

    start = time.time()

    for x in range(0, 1920, 120):
        for y in range(0, 1080, 120):
            divide_frame((x, y), 120, matched_blocks, missing_blocks)

    print(time.time() - start)
    print(len(matched_blocks))

    copied_image = np.zeros([1080, 1920, 3], dtype=np.uint8)

    for mb in matched_blocks:
        x, y, block = mb
        copy_from(f2.frame, copied_image, (y, x), (y, x), (y + block - 1, x + block - 1))

    from PIL import Image as im
    data = im.fromarray(copied_image)
    data.save('gfg_dummy_pic.png')


if __name__ == "__main__":
    main()
