import threading
from multiprocessing import Process
from time import time

import numpy as np

from dandere2x.dandere2xlib.wrappers.frame.frame import Frame


class PframeGenerator:


    def thread1(self, frame_1, frame_2):

        subtracted_and_squared_frame = Frame()
        subtracted_and_squared_frame.create_new(width=frame_1.width, height=frame_1.height)
        subtracted_and_squared_frame.frame = (frame_2.frame - frame_1.frame) ** 2

        for x in range(0, int(1920/4), 10):
            for y in range(0, int(1080/4), 10):

                sub_block = Frame()
                sub_block.create_new(10,10)
                sub_block.copy_block(subtracted_and_squared_frame, 10, x, y, 0, 0)
                np.mean(sub_block.frame)


    def __init__(self,
                 frame_1: Frame,
                 frame_2: Frame,
                 block_size: int,
                 quality_setting: int
                 ):

        frames = []

        start = time()

        t1 = Process(target=self.thread1, args=(frame_1, frame_2,))
        t2 = Process(target=self.thread1, args=(frame_1, frame_2,))
        t3 = Process(target=self.thread1, args=(frame_1, frame_2,))
        t1.start()
        t2.start()
        t3.start()

        t1.join()
        t2.join()
        t3.join()

        end = time()
        print("end time")
        print(end-start)

if __name__ == "__main__":
    frame1 = Frame()
    frame1.load_from_string("C:\\Users\\windw0z\\Desktop\\3.6\\workspace\\gui\\subworkspace\\inputs\\frame1.png")

    frame2 = Frame()
    frame2.load_from_string("C:\\Users\\windw0z\\Desktop\\3.6\\workspace\\gui\\subworkspace\\inputs\\frame40.png")

    pframe = PframeGenerator(frame1, frame2, 30, 30)
