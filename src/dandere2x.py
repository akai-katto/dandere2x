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
import shutil
import sys
import threading
import time

from dandere2xlib.core.difference import difference_loop, difference_loop_resume
from dandere2xlib.core.merge import merge_loop,  merge_loop_resume
from dandere2xlib.status import print_status

from dandere2xlib.utils.dandere2x_utils import valid_input_resolution,get_a_valid_input_resolution, file_exists
from wrappers.frame.frame_compressor import compress_frames

from wrappers.dandere2x_cpp import Dandere2xCppWrapper

from wrappers.ffmpeg.ffmpeg import extract_frames, trim_video
from dandere2xlib.realtime_encoding import run_realtime_encoding

from wrappers.waifu2x.waifu2x_caffe import Waifu2xCaffe
from wrappers.waifu2x.waifu2x_converter_cpp import Waifu2xConverterCpp
from wrappers.waifu2x.waifu2x_vulkan import Waifu2xVulkan


class Dandere2x:

    def __init__(self, context):
        self.context = context

    # This is the main driver for Dandere2x_Python.
    # Essentially we need to call a bunch of different subprocesses to run concurrent with one another
    # To achieve maximum performance.

    def run_concurrent(self):
        # load context
        output_file = self.context.output_file

        # The first thing to do is create the dirs we will need during runtime
        self.create_dirs()
        self.context.set_logger()
        self.write_merge_commands()

        # If the user wishes to trim the video, trim the video, then rename the file_dir to point to the trimmed video
        if self.context.user_trim_video:
            trimed_video = os.path.join(self.context.workspace, "trimmed.mkv")
            trim_video(self.context, trimed_video)
            self.context.file_dir = trimed_video

        # Before we extract all the frames, we need to ensure the settings are valid. If not, resize the video
        # To make the settings valid somehow.
        if not valid_input_resolution(self.context.width, self.context.height, self.context.block_size):
            self.append_video_resize_filter()

        # Extract all the frames
        print("extracting frames from video... this might take a while..")
        extract_frames(self.context, self.context.input_file)
        self.context.update_frame_count()

        # Assign the waifu2x object to whatever waifu2x we're using
        waifu2x = self.get_waifu2x_class(self.context.waifu2x_type)

        # Upscale the first file (the genesis file is treated different in Dandere2x)
        one_frame_time = time.time()  # This timer prints out how long it takes to upscale one frame
        waifu2x.upscale_file(input_file=self.context.input_frames_dir + "frame1" + self.context.extension_type,
                             output_file=self.context.merged_dir + "merged_1" + self.context.extension_type)

        # Ensure the first file was able to get upscaled. We literally cannot continue if it doesn't.
        if not file_exists(self.context.merged_dir + "merged_1" + self.context.extension_type):
            print("Could not upscale first file.. check logs file to see what's wrong")
            logging.info("Could not upscale first file.. check logs file to see what's wrong")
            logging.info("Exiting Dandere2x...")
            sys.exit(1)

        print("\n Time to upscale an uncompressed frame: " + str(round(time.time() - one_frame_time, 2)))

        # This is where Dandere2x's core functions start. Each core function is divided into a series of threads,
        # All with their own segregated tasks and goals. Dandere2x starts all the threads, and lets it go from there.
        compress_frames_thread = threading.Thread(target=compress_frames, args=(self.context,))
        dandere2xcpp_thread = Dandere2xCppWrapper(self.context, resume=False)
        merge_thread = threading.Thread(target=merge_loop, args=(self.context, 1))
        difference_thread = threading.Thread(target=difference_loop, args=(self.context, 1))
        status_thread = threading.Thread(target=print_status, args=(self.context,))
        realtime_encode_thread = threading.Thread(target=run_realtime_encoding, args=(self.context, output_file))

        logging.info("starting new d2x process")
        waifu2x.start()

        merge_thread.start()
        difference_thread.start()
        dandere2xcpp_thread.start()
        status_thread.start()
        compress_frames_thread.start()

        if self.context.realtime_encoding:
            realtime_encode_thread.start()

        compress_frames_thread.join()
        merge_thread.join()
        dandere2xcpp_thread.join()
        difference_thread.join()
        waifu2x.join()
        status_thread.join()

        if self.context.realtime_encoding:
            realtime_encode_thread.join()

        self.context.logger.info("Threaded Processes Finished succcesfully")

    # Resume a Dandere2x Session
    # Consider merging this into one function, but for the time being I prefer it seperate
    # to-do this this work?

    def resume_concurrent(self):
        self.context.update_frame_count()  # we need to count how many outputs there are after ffmpeg extracted stuff
        self.context.set_logger()

        if self.context.realtime_encoding_delete_files:
            print("CANNOT RESUME RUN ON DELETE FILES TYPED SESSION")
            sys.exit(1)

        if self.context.user_trim_video:
            trimed_video = os.path.join(self.context.workspace, "trimmed.mkv")
            self.context.file_dir = trimed_video

        # get whatever waifu2x class we're using
        waifu2x = self.get_waifu2x_class(self.context.waifu2x_type)

        dandere2xcpp_thread = Dandere2xCppWrapper(self.context, resume=True)
        merge_thread = threading.Thread(target=merge_loop_resume, args=(self.context,))
        difference_thread = threading.Thread(target=difference_loop_resume, args=(self.context,))
        status_thread = threading.Thread(target=print_status, args=(self.context,))
        compress_frames_thread = threading.Thread(target=compress_frames, args=(self.context,))

        output_file = self.context.workspace + 'output.mkv'
        realtime_encode_thread = threading.Thread(target=run_realtime_encoding, args=(self.context, output_file))

        self.context.logger.info("Starting Threaded Processes..")

        waifu2x.start()
        merge_thread.start()
        difference_thread.start()
        dandere2xcpp_thread.start()
        status_thread.start()
        compress_frames_thread.start()

        # these can obviously be combined  but leaving them separate for readiability
        if self.context.realtime_encoding == 1:
            realtime_encode_thread.start()

        if self.context.realtime_encoding == 1:
            realtime_encode_thread.join()

        compress_frames_thread.join()
        merge_thread.join()
        dandere2xcpp_thread.join()
        difference_thread.join()
        waifu2x.join()
        status_thread.join()

        self.context.logger.info("Threaded Processes Finished successfully")

    # We could just get the name from self.context, but for readibility it's easier to know
    # What the function does based off what it's passed.
    def get_waifu2x_class(self, name: str):

        if name == "caffe":
            return Waifu2xCaffe(self.context)

        elif name == "converter_cpp":
            return Waifu2xConverterCpp(self.context)

        elif name == "vulkan":
            return Waifu2xVulkan(self.context)

        else:
            logging.info("no valid waifu2x selected")
            print("no valid waifu2x selected")
            exit(1)

    def append_video_resize_filter(self):
        print("Forcing Resizing to match blocksize..")
        width, height = get_a_valid_input_resolution(self.context.width, self.context.height, self.context.block_size)

        print("New width -> " + str(width))
        print("New height -> " + str(height))

        self.context.width = width
        self.context.height = height

        self.context.config_json['ffmpeg']['video_to_frames']['output_options']['-vf'] \
            .append("scale=" + str(self.context.width) + ":" + str(self.context.height))


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

    # delete every folder except the log file in the workspace
    # This because the log file doesn't want to get deleted + having the log
    # stay alive even after everything finishes is useful to know
    def delete_workspace_files(self):
        # create each directory
        for subdirectory in self.directories:
            try:
                shutil.rmtree(subdirectory)
            except OSError:
                print("Deletion of the directory %s failed" % subdirectory)
            else:
                print("Successfully deleted the directory %s " % subdirectory)

        no_sound = os.path.join(self.context.workspace, "nosound.mkv")

        try:
            os.remove(no_sound)

        except OSError:
            print("Deletion of the file %s failed" % no_sound)
            print(OSError.strerror)
        else:
            print("Successfully deleted the file %s " % no_sound)

    def create_dirs(self):
        # create a list of directories we need to create
        self.directories = {self.context.input_frames_dir,
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
                            self.context.compressed_dir,
                            self.context.fade_data_dir,
                            self.context.encoded_dir,
                            self.context.temp_image_folder}

        # need to create workspace before anything else
        try:
            os.mkdir(self.context.workspace)
        except OSError:
            print("Creation of the directory %s failed" % self.context.workspace)
        else:
            print("Successfully created the directory %s " % self.context.workspace)

        # create each directory
        for subdirectory in self.directories:
            try:
                os.mkdir(subdirectory)
            except OSError:
                print("Creation of the directory %s failed" % subdirectory)
            else:
                print("Successfully created the directory %s " % subdirectory)

    # This is almost legacy code and is being left in for
    # A very small demographic of people who want to manually encode the video after runtime

    def write_merge_commands(self):

        no_audio_video = self.context.workspace + "nosound.mkv"
        finished_video = self.context.workspace + "finished.mkv"

        merged_frames = self.context.merged_dir + "merged_%d.jpg"

        migrate_tracks_command = "[ffmpeg_dir] -i [no_audio] -i [file_dir]" \
                                 " -t 00:00:10 -map 0:v:0 -map 1? -c copy -map -1:v? [output_file]"

        migrate_tracks_command = migrate_tracks_command.replace("[ffmpeg_dir]", self.context.ffmpeg_dir)
        migrate_tracks_command = migrate_tracks_command.replace("[no_audio]", no_audio_video)
        migrate_tracks_command = migrate_tracks_command.replace("[file_dir]", self.context.input_file)
        migrate_tracks_command = migrate_tracks_command.replace("[output_file]", finished_video)

        video_from_frames_command = "[ffmpeg_dir] -loglevel 0 -nostats -framerate [frame_rate]" \
                                    " -start_number [start_number] -i [input_frames] -vframes [end_number]" \
                                    " -vf deband=blur=false:range=22 [output_file]"

        video_from_frames_command = video_from_frames_command.replace("[ffmpeg_dir]", self.context.ffmpeg_dir)
        video_from_frames_command = video_from_frames_command.replace("[frame_rate]", str(self.context.frame_rate))
        video_from_frames_command = video_from_frames_command.replace("[start_number]", str(0))
        video_from_frames_command = video_from_frames_command.replace("[input_frames]", merged_frames)
        video_from_frames_command = video_from_frames_command.replace("[end_number]", "")
        video_from_frames_command = video_from_frames_command.replace("-vframes", "")
        video_from_frames_command = video_from_frames_command.replace("[output_file]", no_audio_video)

        with open(self.context.workspace + os.path.sep + 'commands.txt', 'w') as f:
            f.write(video_from_frames_command + "\n")
            f.write(migrate_tracks_command + "\n")

        f.close()
