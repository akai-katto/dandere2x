import argparse
import os
import shutil
import sys
import time
import random
import yaml

from context import Context
from dandere2x import Dandere2x
from dandere2xlib.utils.dandere2x_utils import get_operating_system, dir_exists, file_exists
from wrappers.dandere2x_wrappers.dandere2x_gui_upscale_folder_wrapper import Dandere2xUpscaleFolder

from wrappers.ffmpeg.ffmpeg import re_encode_video, migrate_tracks, append_video_resize_filter, concat_two_videos

skip = True

random_words = ["help", "me", "im", "stuck", "in","a","bad","dream","i","want","to","wake","up","help"]
intro_paragraph = "Welcome to the Dandere2x stuck at 99 bug fixer!"
intro_paragraph = intro_paragraph.lower()

if not skip:
    print("< program starting noises > ")
    time.sleep(.5)
    print("hello?")
    time.sleep(1)
    print("can you hear me?")
    time.sleep(1.2)

    for x  in range(0, int(len(random_words) / 2)):

        w1 = random_words[x*2]
        w2 = random_words[x*2+1]

        intro_paragraph_split = intro_paragraph.split(" ")
        random_swap_pos = random.randint(int (len(intro_paragraph_split) / 2) - 3, int (len(intro_paragraph_split) / 2) + 3)
        intro_paragraph_split[random_swap_pos] = "%s"
        intro_paragraph_split[random_swap_pos + 1] = "%s"

        re_constructed = ""
        for item in intro_paragraph_split:
            re_constructed += (item + " ")

        sys.stdout.write('\r')
        sys.stdout.write(re_constructed % ('"' + w1.upper() + '"', '"' + w2.upper() + '"'))
        time.sleep(.45)

sys.stdout.write('\r')
sys.stdout.write(intro_paragraph)
time.sleep(1)
print("\n")
print("-----------------------------------------------------------------------------------------------------------------------------")
print("This program will attempt to fix your video by manually completing the dandere2x process, what it should of done at 99%.")
print("I've been unable to replicate this bug on any of my window's versions (i've gone through 3 different versions of windows over the past year).")
print("What we're going to do is manually try to migrate the audio tracks using what I know (I being the developer)")
print("Be sure to be run this program as administrator by the way. ")
print("----------------------------------------------------------------------------------------------------------------------------")

dandere2x_config_file =  "dandere2x_%s.yaml" % get_operating_system()
print(" > Attempting to read %s" % dandere2x_config_file)

config = None

try:
    with open(dandere2x_config_file, "r") as read_file:
        config = yaml.safe_load(read_file)
        print("File read!")
except:
    print("Couldn't open %s, exiting" % dandere2x_config_file)
    exit(1)

print(" > Attempting to load context / dandere2x with this file...")

import logging
dandere2x = None

try:
    context = Context(config)
    dandere2x = Dandere2x(context=context)
except:
    print("Loading %s failed!" % dandere2x_config_file)

log = logging.getLogger()
log.info("Hellllllooo ok *taps mic* is this thing on")
log.warning("*cough* *cough* this is a warning message")
log.error("BOO ERROR im an error")
log.info("Haha gotcha")

time.sleep(0.1)
print("----------------------------------------------------")

log.info("Ok first things first I'm going to make sure your workspace exists, the one found in %s" %dandere2x_config_file)
log.info("It is %s, is this what you want? (Exit the program if not) " % dandere2x.context.workspace)
log.info("(If it is not, you can always change it manually to point to the workspace you would like to fix)")

time.sleep(.1)
input("Press Enter to continue...")

log.info("Searching directory....")

import glob

directory_files = glob.glob(os.path.join(dandere2x.context.workspace,"*"))

pre_processed_file = ""
for item in directory_files:
    if "pre_processed.mkv" in item:
        pre_processed_file = item

if pre_processed_file == "":
    log.error("Could not find pre_processed.mkv in %s! I cannot continue" % dandere2x.context.workspace)
    input("Press Enter to continue...")
    exit()

log.info("Found my pre_processed.mkv at %s" % pre_processed_file)

nosound_file = ""

for item in directory_files:
    if "nosound" in item:
        nosound_file = item

if nosound_file == "":
    log.error("Could not find `nosound` in %s! I cannot continue" % dandere2x.context.workspace)
    input("Press Enter to continue...")
    exit(1)

log.info("Found your nosound_file at %s" % nosound_file)
time.sleep(0.1)

print("-------------------------------------------------")
log.warning("Please verify that %s is your complete upscaled video, just has no audio" % nosound_file)
time.sleep(0.1)
input("Press Enter to continue...")

output_extension = os.path.splitext(nosound_file)[1]
output_file = dandere2x.context.workspace + "outputfile" + output_extension
log.info("We will now begin to try to manually migrate the tracks... standby")
log.info("Output video will be at %s " % output_file)

migrate_tracks(context = dandere2x.context, no_audio=nosound_file, file_dir=pre_processed_file, output_file=output_file)

if file_exists(output_file):
    log.info("It seems migration succeeded? Check %s to see if it finished." % output_file)
else:
    log.warning("It seems the file is not there.. this is indicative of a migration failure somewhere")
    log.warning("You can try migrating yourself (above you should see an output called 'Migrate Command:' or something")
    log.warning("From ffmmpeg.py, and you can try changing the flags until it migrates correctly, but tbh beyond that")
    log.warning("You may need to goto forums to answer this problem. ")

time.sleep(0.1)
input("Press Enter to continue...")