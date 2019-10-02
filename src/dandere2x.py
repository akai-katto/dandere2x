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

import logging
import os
import sys
import threading
import time

from context import Context
from dandere2xlib.status import print_status
from dandere2xlib.core.merge import merge_loop
from dandere2xlib.core.residual import residual_loop
from dandere2xlib.frame_compressor import compress_frames
from dandere2xlib.mindiskusage import MinDiskUsage
from dandere2xlib.utils.dandere2x_utils import delete_directories, create_directories
from dandere2xlib.utils.dandere2x_utils import valid_input_resolution, get_a_valid_input_resolution, file_exists
from wrappers.dandere2x_cpp import Dandere2xCppWrapper
from wrappers.ffmpeg.ffmpeg import extract_frames, trim_video, create_video_from_extract_frames, migrate_tracks
from wrappers.waifu2x.waifu2x_caffe import Waifu2xCaffe
from wrappers.waifu2x.waifu2x_converter_cpp import Waifu2xConverterCpp
from wrappers.waifu2x.waifu2x_vulkan import Waifu2xVulkan
from wrappers.waifu2x.waifu2x_vulkan_legacy import Waifu2xVulkanLegacy


class Dandere2x:
    """
    The main driver that can be called in a various level of circumstances - for example, dandere2x can be started
    from dandere2x_gui_wrapper.py, raw_config_driver.py, or raw_config_gui_driver.py. In each scenario, this is the
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

        # load context
        output_file = self.context.output_file

        ############
        # PRE REQS #
        ############

        # The first thing to do is create the dirs we will need during runtime
        create_directories(self.context.directories)
        self.context.set_logger()

        # If the user wishes to trim the video, trim the video, then rename the file_dir to point to the trimmed video
        if self.context.user_trim_video:
            trimed_video = os.path.join(self.context.workspace, "trimmed.mkv")
            trim_video(self.context, trimed_video)
            self.context.input_file = trimed_video

        # Before we extract all the frames, we need to ensure the settings are valid. If not, resize the video
        # To make the settings valid somehow.
        if not valid_input_resolution(self.context.width, self.context.height, self.context.block_size):
            self.append_video_resize_filter(self.context)

        self.jobs = {}

        self.jobs['compress_frames_thread'] = threading.Thread(target=compress_frames, args=([self.context]),
                                                               daemon=True)
        self.jobs['dandere2xcpp_thread'] = Dandere2xCppWrapper(self.context)
        self.jobs['merge_thread'] = threading.Thread(target=merge_loop, args=([self.context]),
                                                     daemon=True)
        self.jobs['residual_thread'] = threading.Thread(target=residual_loop, args=([self.context]), daemon=True)

        waifu2x = self.get_waifu2x_class(self.context.waifu2x_type)

        self.jobs['waifu2x_thread'] = waifu2x

        self.jobs['status_thread'] = threading.Thread(target=print_status, args=([self.context]), daemon=True)

        if self.context.use_min_disk:
            """
            Add min disk the series of threads to be run by the d2x program, and extract the initial set
            of "max_frames_ahead". 
            
            todo: We currently employ some work around where we apply the ffmpeg filters needed for dandere2x
                  run into it's own video, so that progressive frame extraction can have the same filters. 
            """

            noisy_video = self.context.workspace + "noisy.mkv"
            create_video_from_extract_frames(self.context, noisy_video)
            migrate_tracks(self.context, noisy_video, self.context.input_file, noisy_video)

            self.context.input_file = noisy_video

            min_disk_usage = MinDiskUsage(self.context)
            min_disk_usage.extract_initial_frames()
            self.jobs['min_disk_thread'] = threading.Thread(target=min_disk_usage.run, daemon=True)

        elif not self.context.use_min_disk:
            """
            If we're not using min disk, extract the frames all at once using ffmpeg
            """
            extract_frames(self.context, self.context.input_file)

        # Upscale the first file (the genesis file is treated different in Dandere2x)
        one_frame_time = time.time()  # This timer prints out how long it takes to upscale one frame
        waifu2x.upscale_file(input_file=self.context.input_frames_dir + "frame1" + self.context.extension_type,
                             output_file=self.context.merged_dir + "merged_1" + self.context.extension_type)

        if not file_exists(self.context.merged_dir + "merged_1" + self.context.extension_type):
            """ 
            Ensure the first file was able to get upscaled. We literally cannot continue if it doesn't.
            """

            print("Could not upscale first file.. check logs file to see what's wrong")
            logging.info("Could not upscale first file.. check logs file to see what's wrong")
            logging.info("Exiting Dandere2x...")
            sys.exit(1)

        print("\n Time to upscale an uncompressed frame: " + str(round(time.time() - one_frame_time, 2)))

        ######################################
        #  THREADING / MULTIPROCESSING AREA  #
        ######################################

        for job in self.jobs:
            self.jobs[job].start()
            logging.info("Starting new %s process" % job)

        for job in self.jobs:
            self.jobs[job].join()

            logging.info("%s process thread joined" % job)

        self.context.logger.info("All threaded processes have finished")

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
            print("no valid waifu2x selected")
            exit(1)

    @staticmethod
    def append_video_resize_filter(context: Context):
        """
        For ffmpeg, there's a video filter to resize a video to a given resolution.
        For dandere2x, we need a very specific set of video resolutions to work with.  This method applies that filter
        to the video in order for it to work correctly.
        """

        print("Forcing Resizing to match blocksize..")
        width, height = get_a_valid_input_resolution(context.width, context.height, context.block_size)

        print("New width -> " + str(width))
        print("New height -> " + str(height))

        context.width = width
        context.height = height

        context.config_json['ffmpeg']['video_to_frames']['output_options']['-vf'] \
                            .append("scale=" + str(context.width) + ":" + str(context.height))

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
