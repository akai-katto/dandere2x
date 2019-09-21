from dandere2xlib.utils.dandere2x_utils import get_lexicon_value, wait_on_either_file, wait_on_file, get_operating_system
from termcolor import colored
from context import Context

import threading
import colorama
import datetime
import time
import sys
import os

colorama.init(convert=True)

# TODO
# ~This-could-probably-be-improved-visually-for-the-user..-it's-not-the-most-pleasing-to-look-at~ Fixed?
# Also, in a very niche case the GUI didn't catch up with the deletion of files, so it ceased updating


context = None
lexiconx = None
lexiconframe = None
percent = 0
runs_list_size = None
average_1 = 0
average_2 = 0
average_all = 0
estimated_finish = 0


class ClearScreen():
    def __init__(self):
        self.command = 'clear' if get_operating_system() == 'linux' else 'cls'

    def clear(self):
        os.system(self.command)


def watch_frame():
    global context, lexiconx, lexiconframe, percent, runs_list_size, average_1, average_2, average_all, estimated_finish

    runs_list_size = 20

    workspace = context.workspace
    extension_type = context.extension_type
    frame_count = context.frame_count

    frame_count_max_char = len(str(frame_count))

    # _ is a dummy var, creating a runs zeros list
    last_runs_1 = [0 for _ in range(runs_list_size)]
    last_runs_2 = [0 for _ in range(runs_list_size*5)]
    every_runs = [0.00001] # low value to don't get division by zero

    
    # Not sure why but "-1" is necessary for ffmpeg_pipe_encoding to work properly
    
    # makes sense tho, say we got a 1 frame video, range(2,0) returns nothing 
    # (only one frame, the first that gets upscaled when d2x starts running)

    # say we got a 2 frames file, the stats ought only print the second frame
    # when it's already a merged/upsacaled file

    # and for a N video file, we'll print N - 1 updates frames since we're starting from the number 1 
    
    # don't start in one, will mess up some printings before starting status thread
    for x in range(1, frame_count - 1):

        percent = int((x / (frame_count - 2)) * 100)
        average_1 = round(sum(last_runs_1) / len(last_runs_1), 2)
        average_2 = round(sum(last_runs_2) / len(last_runs_2), 2)
        average_all = round(sum(every_runs) / len(every_runs), 2)

        estimated_finish = str(datetime.timedelta(seconds=round((frame_count-x-1)*average_all)))

        lexiconx = get_lexicon_value(frame_count_max_char, x + 2) # + 2 because we ignore frame 2 and 1 is upscaled separately
        lexiconframe = get_lexicon_value(frame_count_max_char, frame_count)

        merged_file = workspace + "merged/merged_" + str(x + 1) + extension_type
        upscaled_file = workspace + "residual_upscaled/output_" + get_lexicon_value(6, x) + ".png"

        start = time.time()

        wait_on_either_file(merged_file, upscaled_file)

        # smart loop to store new values, loops from 0 to runs_file_size - 1     
        last_runs_1[x % runs_list_size] = time.time() - start
        last_runs_2[x % (runs_list_size*5)] = time.time() - start
        every_runs.append(time.time() - start)


def print_status(ctx: Context, d2x_main):
    global context, lexiconx, lexiconframe, percent, runs_list_size, average_1, average_2, average_all, estimated_finish

    started = time.strftime('%X %x')

    context = ctx

    WF = threading.Thread(target=watch_frame)
    WF.start() # Watch Frame thread
    
    clearscreen = ClearScreen()

    running = no = ' '
    finished = yes = 'x'

    ffmpeg_pipe_encoding = yes if context.ffmpeg_pipe_encoding else no
    
    ffmpeg_pipe_encoding_type = context.ffmpeg_pipe_encoding_type if context.ffmpeg_pipe_encoding else "-"

    #                     merge thread
    while WF.isAlive() or d2x_main.jobs[2].is_alive():

        time.sleep(1)

        waifu2xthread = running if d2x_main.waifu2x.is_alive() else finished
        compress = running if d2x_main.jobs[0].is_alive() else finished
        dandere2xcpp_thread = running if d2x_main.jobs[1].running() else finished
        merge_thread = running if d2x_main.jobs[2].is_alive() else finished
        residual_thread = running if d2x_main.jobs[3].is_alive() else finished

        module_header = """
      [ # ] Dandere2x Work in Progress Status CLI [ # ]
                                              v. [1.0.2]

"""
        module_general = """
  General::
      Frame:  [{}/{}] {} %
      Finish: [{}] est.


""".format(lexiconx, lexiconframe, percent,
           estimated_finish)



        module_average = """
  Averages::
      Last {} frames: [{}] sec/frame
      Last {} frames: [{}] sec/frame
      Total runtime:   [{}] sec/frame


""".format(get_lexicon_value(3, runs_list_size),   average_1,
           get_lexicon_value(3, runs_list_size*5), average_2,
           average_all)

    
    
        module_main_monitor = """
  Dandere2x Main Monitor::
      Compress Thread Finished: [{}]
      Dandere2x CPP Finished:   [{}]
      Residual Thread Finished: [{}]
      Waifu2x Thread Finished:  [{}]
      Merge & Encode Finished:  [{}]


""".format(compress,
           dandere2xcpp_thread,
           residual_thread,
           waifu2xthread,
           merge_thread)

    
    
        module_modules = """
  Modules enabled::
      Experimental/FFmpeg pipe encode: [{}]    Type: [{}]


""".format(ffmpeg_pipe_encoding, ffmpeg_pipe_encoding_type)

    
    
        module_time = """
  Started: [{}]    Now: [{}]
""".format(started, time.strftime('%X %x'))
        


        statement = module_header + module_general + module_average

        if True: # if minimal_disk enabled         # shhh! future thing
            statement += module_main_monitor
        
        statement += module_modules + module_time


        clearscreen.clear()
        print(statement, end='\r')


    #print("\n\n Finishing up Dandere2x stuff like migrating audio track, finishing encoding if ffmpeg_pipe_encoding is enabled / final concatenation if not.\n")
