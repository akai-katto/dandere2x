import time
import sys
from wrappers.frame import Frame

before = time.time()

raw = Frame()
raw.load_from_string("C:\\Users\\windwoz\\Desktop\\workspace\\yn7\\inputs\\frame1.jpg")

comp = Frame()
comp.load_from_string("C:\\Users\\windwoz\\Desktop\\workspace\\yn7\\time\\1.jpg")

before = time.time()

print(((raw.frame - comp.frame)**2).mean(axis=None))
# for x in range (1920/30):
#     for y in range(1080/30):
#         raw.frame

print(time.time() - before)