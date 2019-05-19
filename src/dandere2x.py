#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: Dandere2X
Author: CardinalPanda
Date Created: March 22, 2019
Last Modified: April 2, 2019

Licensed under the GNU General Public License Version 3 (GNU GPL v3),
    available at: https://www.gnu.org/licenses/gpl-3.0.txt

(C) 2018-2019 CardinalPanda

Dandere2X is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Dandere2X is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Description: Dandere2X is an automation software based on waifu2x image
enlarging engine. It extracts frames from a video, enlarge it by a
number of times without losing any details or quality, keeping lines
smooth and edges sharp.
"""

from context import Context

from dandere2x_core.difference import difference_loop
from dandere2x_core.difference import difference_loop_resume
from dandere2x_core.merge import merge_loop
from dandere2x_core.merge import merge_loop_resume
from dandere2x_core.status import print_status
from dandere2x_core.mse_computer import compress_frames

from dandere2x_core.dandere2x_utils import verify_user_settings

from wrappers.dandere2x_cpp import Dandere2xCppWrapper
from wrappers.ffmpeg import extract_audio as ffmpeg_extract_audio
from wrappers.ffmpeg import extract_frames as ffmpeg_extract_frames
from wrappers.waifu2x_caffe import Waifu2xCaffe
from wrappers.waifu2x_conv import Waifu2xConv

import logging
import os
import threading
import sys
import time

# logger doesnt operate out of workspace, but thats ok I guess

def make_logger(path=""):

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # create a file handler
    fh = logging.FileHandler(f'{path}dandere2x.log')
    fh.setLevel(logging.INFO)

    # create a print(stdout) handler
    ph = logging.StreamHandler(sys.stdout)
    ph.setLevel(logging.INFO)

    # create a logging format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ph.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ph)
    return logger


class Dandere2x:

    def __init__(self, config_file: str):
        self.context = Context(config_file)
        self.logger = make_logger()

    # Order matters here in command calls.
    def pre_setup(self):
        self.context.logger.info("Starting new dandere2x session")
        self.create_dirs()
        ffmpeg_extract_audio(self.context)
        ffmpeg_extract_frames(self.context)
        self.create_waifu2x_script()
        self.write_frames()
        self.write_merge_commands()

    # create a series of threads and external processes
    # to run in real time with each other for the dandere2x session.
    # the code is self documenting here.
    def run_concurrent(self):
        self.pre_setup()
        self.context.update_frame_count()
        verify_user_settings(self.context)

        start = time.time()# This timer prints out how long it takes to upscale one frame

        # set waifu2x to be whatever waifu2x type we are using
        if self.context.waifu2x_type == "caffe":
            waifu2x = Waifu2xCaffe(self.context)

            Waifu2xCaffe.upscale_file(self.context,
                                      input_file=self.context.input_frames_dir + "frame1" + self.context.extension_type,
                                      output_file=self.context.merged_dir + "merged_1" + self.context.extension_type)

        elif self.context.waifu2x_type == "conv":
            waifu2x = Waifu2xConv(self.context)

            Waifu2xConv.upscale_file(self.context,
                                     input_file=self.context.input_frames_dir + "frame1" + self.context.extension_type,
                                     output_file=self.context.merged_dir + "merged_1" + self.context.extension_type)

        print("\nTime to upscale an uncompressed frame: " + str(round(time.time() - start, 2)))

        # start all the threads needed for running 
        compress_frames_thread = threading.Thread(target=compress_frames, args=(self.context,))
        dandere2xcpp_thread = Dandere2xCppWrapper(self.context, resume=False)
        merge_thread = threading.Thread(target=merge_loop, args=(self.context, 1))
        difference_thread = threading.Thread(target=difference_loop, args=(self.context, 1))
        status_thread = threading.Thread(target=print_status, args=(self.context,))

        self.context.logger.info("Starting Threaded Processes..")

        waifu2x.start()
        merge_thread.start()
        difference_thread.start()
        dandere2xcpp_thread.start()
        status_thread.start()
        compress_frames_thread.start()

        compress_frames_thread.join()
        merge_thread.join()
        dandere2xcpp_thread.join()
        difference_thread.join()
        waifu2x.join()
        status_thread.join()

        self.context.logger.info("Threaded Processes Finished succcesfully")

    # Resume a Dandere2x Session
    # Consider merging this into one function, but for the time being I prefer it seperate
    def resume_concurrent(self):
        self.context.update_frame_count() # we need to count how many outputs there are after ffmpeg extracted stuff
        verify_user_settings(self.context)

        if self.context.waifu2x_type == "caffe":
            waifu2x = Waifu2xCaffe(self.context)
            Waifu2xCaffe.upscale_file(self.context,
                                      input_file=self.context.input_frames_dir + "frame1" + self.context.extension_type,
                                      output_file=self.context.merged_dir + "merged_1" + self.context.extension_type)

        elif self.context.waifu2x_type == "conv":
            waifu2x = Waifu2xConv(self.context)
            Waifu2xConv.upscale_file(self.context,
                                     input_file=self.context.input_frames_dir + "frame1" + self.context.extension_type,
                                     output_file=self.context.merged_dir + "merged_1" + self.context.extension_type)

        dandere2xcpp_thread = Dandere2xCppWrapper(self.context, resume=True)
        merge_thread = threading.Thread(target=merge_loop_resume, args=(self.context,))
        difference_thread = threading.Thread(target=difference_loop_resume, args=(self.context,))
        status_thread = threading.Thread(target=print_status, args=(self.context,))

        self.context.logger.info("Starting Threaded Processes..")

        waifu2x.start()
        merge_thread.start()
        difference_thread.start()
        dandere2xcpp_thread.start()
        status_thread.start()

        merge_thread.join()
        dandere2xcpp_thread.join()
        difference_thread.join()
        waifu2x.join()
        status_thread.join()

        self.context.logger.info("Threaded Processes Finished successfully")

    # only calculate the differences. To be implemented in video2x / converter-cpp
    def difference_only(self):
        self.pre_setup()

        dandere2xcpp_thread = Dandere2xCppWrapper(self.context, resume=False)
        difference_thread = threading.Thread(target=difference_loop, args=(self.context, 1))

        self.context.logger.info("Starting Threaded Processes..")

        difference_thread.start()
        dandere2xcpp_thread.start()

        dandere2xcpp_thread.join()
        difference_thread.join()

    def merge_only(self):
        merge_thread = threading.Thread(target=merge_loop, args=(self.context, 1))
        merge_thread.start()
        merge_thread.join()

    def create_dirs(self):
        # create a list of directories we need to create
        directories = {self.context.input_frames_dir,
                       self.context.correction_data_dir,
                       self.context.differences_dir,
                       self.context.upscaled_dir,
                       self.context.merged_dir,
                       self.context.upscaled_dir,
                       self.context.merged_dir,
                       self.context.inversion_data_dir,
                       self.context.pframe_data_dir,
                       self.context.debug_dir,
                       self.context.log_dir,
                       self.context.compressed_dir}

        # need to create workspace before anything else
        try:
            os.mkdir(self.context.workspace)
        except OSError:
            print("Creation of the directory %s failed" % self.context.workspace)
        else:
            print("Successfully created the directory %s " % self.context.workspace)

        # create each directory
        for subdirectory in directories:
            try:
                os.mkdir(subdirectory)
            except OSError:
                print("Creation of the directory %s failed" % subdirectory)
            else:
                print("Successfully created the directory %s " % subdirectory)

    # for linux. Currently deprecated as Linux development has stopped for a bit.
    def create_waifu2x_script(self):
        input_list = []
        input_list.append("cd /home/linux/Documents/waifu2x/")

        input_list.append(
            "th " + self.context.dandere_dir + " -m noise_scale -noise_level 3 -i " +
            self.context.input_frames_dir + "frame1" + self.context.extension_type +
            " -o " + self.context.merged_dir + "merged_1" + self.context.extension_type + "\n")

        input_list.append("th " + self.context.dandere_dir + " -m noise_scale -noise_level 3 -resume 1 -l " +
                          self.context.workspace + "frames.txt -o " + self.context.upscaled_dir + "output_%d.png")

        with open(self.context.workspace + os.path.sep + 'waifu2x_script.sh', 'w') as f:
            for item in input_list:
                f.write("%s\n" % item)

        os.chmod(self.context.workspace + os.path.sep + 'waifu2x_script.sh', 0o777)

    # for linux
    def write_frames(self):
        with open(self.context.workspace + os.path.sep + 'frames.txt', 'w') as f:
            for x in range(1, self.context.frame_count):
                f.write(self.context.differences_dir + "output_" + str(x) + ".png\n")

    # for re-merging the files after runtime is done
    def write_merge_commands(self):
        with open(self.context.workspace + os.path.sep + 'commands.txt', 'w') as f:
            f.write(
                self.context.ffmpeg_dir + " -f image2 -framerate " + self.context.frame_rate + " -i " + self.context.merged_dir + "merged_%d.jpg -r " + self.context.frame_rate + " -vf deband " + self.context.workspace + "nosound.mp4\n\n")
            f.write(
                self.context.ffmpeg_dir + " -i " + self.context.workspace + "nosound.mp4" + " -i " + self.context.workspace + "audio" + self.context.audio_type + " -c copy " +
                self.context.workspace + "sound.mp4\n\n")
