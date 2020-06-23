import cv2

from wrappers.cv2.progressive_frame_extractor_cv2 import ProgressiveFramesExtractorCV2
import yaml
from context import Context
from dandere2x import Dandere2x

configfile = "dandere2x_win32.yaml"

# load yaml

with open(configfile, "r") as read_file:
    config = yaml.safe_load(read_file)


cap = cv2.VideoCapture("C:\\Users\\windwoz\\Documents\\GitHub\\dandere2x\\src\\workspace\\test2.mkv")


print("frame count: " + str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))
context = Context(config)
extractor = ProgressiveFramesExtractorCV2(context)

for x in range(0, 2158):
    #print("On frame: %d" , x)
    extractor.next_frame()