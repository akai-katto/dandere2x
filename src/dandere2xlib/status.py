import os
import sys
import time

from context import Context

from dandere2xlib.utils.dandere2x_utils import get_lexicon_value, wait_on_either_file, wait_on_file

# TODO
# This could probably be improved visually for the user.. it's not the most pleasing to look at
# Also, in a very niche case the GUI didn't catch up with the deletion of files, so it ceased updating

def print_status(context: Context):

    runs_list_size = 20

    workspace = context.workspace
    extension_type = context.extension_type
    frame_count = context.frame_count

    last_runs = [0 for _ in range(runs_list_size)]

    for x in range(1, frame_count - 1): # Not sure why but "-1" is necessary for ffmpeg_pipe_encoding to work properly
        percent = int((x / (frame_count - 2)) * 100)

        average = round(sum(last_runs) / len(last_runs), 2)

        sys.stdout.write('\r')
        sys.stdout.write("Frame: [%s] %i%%    Average of Last %s Frames: %s sec / frame" % (x, percent, runs_list_size, average))

        merged_file = workspace + "merged/merged_" + str(x + 1) + extension_type
        upscaled_file = workspace + "residual_upscaled/output_" + get_lexicon_value(6, x) + ".png"

        start = time.time()

        wait_on_either_file(merged_file, upscaled_file)

        # insert new run times on remainder of the iteration and runs_list_size
        
        last_runs[x % runs_list_size] = time.time() - start
        
        #works like this:
        """
        >>> for i in range(20):
        >>>     print(i, i%10)
        
        0 0
        1 1
        2 2
        3 3
        4 4
        5 5
        6 6
        7 7
        8 8
        9 9
        10 0
        11 1
        12 2
        13 3
        ...
        
        """
        
    
    print("\n\n Finishing up Dandere2x stuff like migrating audio track or finishing encoding if ffmpeg_pipe_encoding is enabled\n")
