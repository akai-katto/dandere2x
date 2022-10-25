import time

import numpy
import numpy as np

from dandere2x.dandere2xlib.wrappers.frame.frame import Frame, copy_from
from multiprocessing.pool import ThreadPool, Pool

f1 = Frame()
f1.load_from_string(
    "C:\\Users\\windw0z\\Documents\\GitHub\\dandere2x\\src\\workspace\\gui\\subworkspace\\inputs\\frame44.png")

f2 = Frame()
f2.load_from_string(
    "C:\\Users\\windw0z\\Documents\\GitHub\\dandere2x\\src\\workspace\\gui\\subworkspace\\inputs\\frame50.png")

array_subtracted_squared: np.array = (f2.frame - f1.frame) ** 2

def process_mse_blocks(block_size: int):

    for x in range(int(1920 / block_size)):
        for y in range(int(1080 / block_size)):
            some_block = np.zeros([block_size, block_size, 3], dtype=np.uint8)
            copy_from(array_subtracted_squared, some_block, (y, x), (0, 0), (block_size - 1, block_size - 1))


def main():
    list_of_args = []

    for _ in range(10):
        start = time.time()

        with ThreadPool(16) as tp:
            tp.map(process_mse_blocks, [10,20,30,60])

        print(time.time() - start)


if __name__ == "__main__":
    main()
