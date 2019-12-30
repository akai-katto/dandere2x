import time

import yaml

from context import Context
from dandere2x import Dandere2x
from dandere2xlib.utils.dandere2x_utils import get_operating_system
from wrappers.ffmpeg.ffmpeg import concat_two_videos

start = time.time()

# get config based on OS
configfile = "dandere2x_%s.yaml" % get_operating_system()

# load yaml

with open(configfile, "r") as read_file:
    config = yaml.safe_load(read_file)

# load the context with yaml stuff
context = Context(config)

video_1 = "C:\\Users\\windwoz\\Documents\\GitHub\\dandere2x\\src\\workspace\\default\\nosound.mp4"
video_2 = "C:\\Users\\windwoz\\Documents\\GitHub\\dandere2x\\src\\workspace\\default\\32\\nosound.mp4"
output = "C:\\Users\\windwoz\\Documents\\GitHub\\dandere2x\\src\\workspace\\default\\32\\python_test.mp4"

concat_two_videos(context, video_1, video_2, output)

