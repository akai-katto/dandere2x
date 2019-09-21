#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Licensed under the GNU General Public License Version 3 (GNU GPL v3),
    available at: https://www.gnu.org/licenses/gpl-3.0.txt

(C) 2018-2019 aka_katto

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


# multiprocessing paths and running outside src dir workaround
# update: looks like we don't need this for multiprocessing working on the files they are called, that simple os.chdir fixed it
# import os, sys; sys.path.append("../" * (sum([os.path.dirname(os.path.abspath(__file__)).split("src")[-1:][0].count(c) for c in ["/", "\\"]])))
# this last line appends to path for every file the src directory of dandere2x
# if things don't work on paths we can use this on the file it got an error?

import os; os.chdir(os.path.dirname(os.path.abspath(__file__)))

from wrappers.waifu2x.waifu2x_converter_cpp import Waifu2xConverterCpp
from wrappers.waifu2x.waifu2x_vulkan_legacy import Waifu2xVulkanLegacy
from dandere2xlib.utils.dandere2x_utils import valid_input_resolution, get_a_valid_input_resolution, file_exists
from dandere2xlib.utils.dandere2x_utils import delete_directories, create_directories
from wrappers.waifu2x.waifu2x_vulkan import Waifu2xVulkan
from wrappers.waifu2x.waifu2x_caffe import Waifu2xCaffe
from dandere2xlib.realtime_encoding import run_realtime_encoding
from dandere2xlib.frame_compressor import compress_frames
from dandere2xlib.core.residual import residual_loop
from dandere2xlib.core.merge import merge_loop
from wrappers.ffmpeg.ffmpeg import extract_frames, trim_video
from wrappers.dandere2x_cpp import Dandere2xCppWrapper
from dandere2xlib.status import print_status

import multiprocessing
import threading
import logging
import time
import sys


class Dandere2x:
    """
    The main driver that can be called in a various level of circumstances - for example, dandere2x can be started
    from dandere2x_gui_wrapper.py, json_driver.py, or json_gui_driver.py. In each scenario, this is the
    class that is called when Dandere2x ultimately needs to start.
    """

    def __init__(self, context):
        self.context = context

    def run_concurrent(self):
        """
        Starts the dandere2x_python process at large.

        Inputs:
        - context

        Pre-Reqs:
        'This is all the stuff that needs to be done before dandere2x can officially start'

        - creates workspaces needed for dandere2x to work
        - edits the video if it's needed to be trimmed or needs resolution needs to be resized.
        - extracts all the frames in the video into it's own folder.
        - upscales the first frame using waifu2x and ensuring the genesis image upscaled correctly.

        Threading Area:

        - calls a series of threads for dandere2x_python to work
          (residuals, merging, waifu2x, dandere2xcpp, realtime-encoding)
        """

        # # LOAD CONTEXT # #
        
        output_file = self.context.output_file

        ############
        # PRE REQS #
        ############

        # The first thing to do is create the dirs we will need during runtime
        create_directories(self.context.directories)
        self.context.set_logger()

        # If the user wishes to trim the video, trim the video,
        # then rename the file_dir to point to the trimmed video
        if self.context.user_trim_video:
            trimed_video = os.path.join(self.context.workspace, "trimmed.mkv")
            trim_video(self.context, trimed_video)
            self.context.input_file = trimed_video

        # Before we extract all the frames, we need to ensure
        # the settings are valid. If not, resize the video
        # To make the settings valid somehow.
        if not valid_input_resolution(self.context.width, self.context.height, self.context.block_size):
            self.append_video_resize_filter()

        # TODO: check every setting valid? any waifu2x client configured?

        # Extract all the frames from source video
        print("\n  Extracting the frames from source video.. this might take a while..")
        extract_frames(self.context, self.context.input_file)
        self.context.update_frame_count()

        # Assign the waifu2x object to whatever waifu2x we're using
        self.waifu2x = self.get_waifu2x_class(self.context.waifu2x_type)

        # Upscale the first file (the genesis file is treated different in Dandere2x)
        print("\n  Upscaling the first frame.. We literally cannot continue if it doesn't")
        one_frame_time = time.time()
        self.waifu2x.upscale_file(input_file=self.context.input_frames_dir + "frame1" + self.context.extension_type,
                             output_file=self.context.merged_dir + "merged_1" + self.context.extension_type)

        # Ensure the first file was able to get upscaled. We literally cannot continue if it doesn't.
        if not file_exists(self.context.merged_dir + "merged_1" + self.context.extension_type):
            print("    ERROR: Could not upscale first file.. check logs file to see what's wrong")
            logging.info("Could not upscale first file.. check logs file to see what's wrong")
            logging.info("Exiting Dandere2x...")
            sys.exit(1)

        print("\n  Time to upscale an uncompressed frame:", str(round(time.time() - one_frame_time, 2)), "\n")
        

        ######################################
        #  THREADING / MULTIPROCESSING AREA  #
        ######################################

        # This is where Dandere2x's core functions start.
        # Each core function is divided into a series of threads and processes,
        # All with their own segregated tasks and goals.
        # Dandere2x starts all the threads, and lets it go from there.
 
        # the daemon=True is for quitting the process when the main thread quits
        # KeyboardInterrupt to be short

        # must not change this order or will mess up with stats thread
        # perhaps use a dictionary to store the threads by name?

        self.jobs = []

        self.jobs.append(multiprocessing.Process(target=compress_frames, args=(self.context,), daemon=True)) # compress_frames_thread
        self.jobs.append(Dandere2xCppWrapper(self.context)) # dandere2xcpp_thread
        self.jobs.append(multiprocessing.Process(target=merge_loop, args=(self.context,), daemon=True)) # merge_thread
        self.jobs.append(multiprocessing.Process(target=residual_loop, args=(self.context,), daemon=True)) # residual_thread
        self.jobs.append(threading.Thread(target=print_status, args=(self.context, self))) # status_thread

        if self.context.realtime_encoding_enabled:
            self.jobs.append(multiprocessing.Process(target=run_realtime_encoding, args=(self.context, output_file), daemon=True)) # realtime_encode_thread

        logging.info("starting new d2x process")

        self.waifu2x.start()

        for job in self.jobs:
            job.start()

        for job in self.jobs:
            job.join()

        self.waifu2x.join()

        self.context.logger.info("Threaded Processes Finished succcesfully")


    def get_waifu2x_class(self, name: str):

        if name == "caffe":
            return Waifu2xCaffe(self.context)

        elif name == "converter_cpp":
            return Waifu2xConverterCpp(self.context)

        elif name == "vulkan":
            return Waifu2xVulkan(self.context)

        elif name == "vulkan_legacy":
            return Waifu2xVulkanLegacy(self.context)

        else:
            logging.info("no valid waifu2x selected")
            print("\n  ERROR: No valid waifu2x selected")
            exit(1)

    def append_video_resize_filter(self):
        """
        For FFmpeg, there's a video filter to resize a video to a given resolution.
        For dandere2x, we need a very specific set of video resolutions to work with.  This method applies that filter
        to the video in order for it to work correctly.
        """

        print("\nForcing Resizing to match blocksize..\n")
        width, height = get_a_valid_input_resolution(self.context.width, self.context.height, self.context.block_size)

        print("  New width -> " + str(width))
        print("  New height -> " + str(height))

        self.context.width = width
        self.context.height = height

        self.context.config_file['ffmpeg']['video_to_frames']['output_options']['-vf'] \
            .append("scale=" + str(self.context.width) + ":" + str(self.context.height))

    def delete_workspace_files(self):
        """
        Delete the files produced by dandere2x (beside logs) if this method is called.
        """
        
        delete_directories(self.context.directories)
        no_sound = os.path.join(self.context.workspace, "nosound.mkv")

        try:
            os.remove(no_sound)

        except OSError:
            print("Deletion of the file %s failed" % no_sound)
            print(OSError.strerror)
        else:
            print("Successfully deleted the file %s " % no_sound)
