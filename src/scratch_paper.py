import time
import sys
from wrappers.frame import Frame

before = time.time()



f1 = Frame()
f1.load_from_string('C:\\Users\\windwoz\\Desktop\\workspace\\yn\\inputs\\frame1.jpg')

f1.save_image_quality('C:\\Users\\windwoz\\Desktop\\workspace\\yn\\quality.jpg', 100)

f2 = Frame()
f2.load_from_string('C:\\Users\\windwoz\\Desktop\\workspace\\yn\\quality.jpg')

print(time.time() - before)