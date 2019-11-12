import os
import sys
import time

from context import Context
from dandere2xlib.utils.dandere2x_utils import get_lexicon_value


# todo
# This could probably be improved visually for the user.. it's not the most pleasing to look at
# Also, in a very niche case the GUI didn't catch up with the deletion of files, so it ceased updating

def print_status(context: Context):
    workspace = context.workspace
    extension_type = context.extension_type
    frame_count = context.frame_count

    last_10 = [0]

    for x in range(1, frame_count - 1):
        percent = int((x / frame_count) * 100)

        average = 0
        for time_count in last_10:
            average = average + time_count

        average = round(average / len(last_10), 2)

        sys.stdout.write('\r')
        sys.stdout.write("Frame: [%s] %i%%    Average of Last 10 Frames: %s sec / frame" % (x, percent, average))

        if len(last_10) == 10:
            last_10.pop(0)

        now = time.time()

        while x >= context.signal_merged_count:
            time.sleep(.00001)

        later = time.time()
        difference = float(later - now)
        last_10.append(difference)
