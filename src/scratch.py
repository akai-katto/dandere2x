import time

import numpy as np

from dandere2x.dandere2xlib.utils.yaml_utils import load_executable_paths_yaml
from dandere2x.dandere2xlib.wrappers.frame.frame import Frame, copy_from

if __name__ == "__main__":
    frame1 = Frame()
    frame1.load_from_string("C:\\Users\\windw0z\\Desktop\\3.6\\workspace\\gui\\subworkspace\\inputs\\frame1.png")

    frame2 = Frame()
    frame2.load_from_string("C:\\Users\\windw0z\\Desktop\\3.6\\workspace\\gui\\subworkspace\\inputs\\frame40.png")

    print((frame2.frame - frame1.frame) ** 2)

    start = time.time()
    block = np.zeros([30, 30, 3], dtype=np.uint8)
    copy_from(frame2.frame,block,(0,0), (0,0), (29,29) )

    print((block ** 2).mean())
    end = time.time()

    print(end-start)
    #print(frame._frame_array)
