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

from dandere2x_core.dandere2x_utils import determine_sens
from dandere2x_core.dandere2x_utils import get_seconds_from_time
from dandere2x_core.difference import difference_loop
from dandere2x_core.difference import difference_loop_resume
from dandere2x_core.merge import merge_loop
from dandere2x_core.merge import merge_loop_resume
from wrappers.dandere2x_cpp import Dandere2xCppWrapper
from wrappers.ffmpeg import extract_audio as ffmpeg_extract_audio
from wrappers.ffmpeg import extract_frames as ffmpeg_extract_frames
from wrappers.waifu2x_caffe import Waifu2xCaffe
from wrappers.waifu2x_conv import Waifu2xConv
from wrappers.frame import Frame
import configparser
import logging
import os
import threading
import random

class Dandere2x:

    # init is pretty messy at the moment. I'll look into
    # cleaning this up in the future ;-;
    def __init__(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)

        self.this_folder = os.path.dirname(os.path.realpath(__file__)) + os.path.sep

        # directories
        self.waifu2x_caffe_cui_dir = config.get('dandere2x', 'waifu2x_caffe_cui_dir')
        self.model_dir = config.get('dandere2x', 'model_dir')

        self.workspace = config.get('dandere2x', 'workspace')
        self.dandere2x_cpp_dir = config.get('dandere2x', 'dandere2x_cpp_dir')
        self.ffmpeg_dir = config.get('dandere2x', 'ffmpeg_dir')
        self.file_dir = config.get('dandere2x', 'file_dir')
        self.waifu2x_type = config.get('dandere2x', 'waifu2x_type')

        self.waifu2x_conv_dir = config.get('dandere2x', 'waifu2x_conv_dir')
        self.waifu2x_conv_dir_dir = config.get('dandere2x', 'waifu2x_conv_dir_dir')

        if '[this]' in self.waifu2x_conv_dir:
            self.waifu2x_conv_dir = self.waifu2x_conv_dir.replace('[this]', self.this_folder)

        if '[this]' in self.waifu2x_conv_dir_dir:
            self.waifu2x_conv_dir_dir = self.waifu2x_conv_dir_dir.replace('[this]', self.this_folder)

        # parse [this] for release versions (removing this feature in the future, just for early testing.

        if '[this]' in self.waifu2x_caffe_cui_dir:
            self.waifu2x_caffe_cui_dir = self.waifu2x_caffe_cui_dir.replace('[this]', self.this_folder)

        if '[this]' in self.workspace:
            self.workspace = self.workspace.replace('[this]', self.this_folder)

        if '[this]' in self.dandere2x_cpp_dir:
            self.dandere2x_cpp_dir = self.dandere2x_cpp_dir.replace('[this]', self.this_folder)

        if '[this]' in self.ffmpeg_dir:
            self.ffmpeg_dir = self.ffmpeg_dir.replace('[this]', self.this_folder)

        if '[this]' in self.file_dir:
            self.file_dir = self.file_dir.replace('[this]', self.this_folder)

        if '[this]' in self.model_dir:
            self.model_dir = self.model_dir.replace('[this]', self.this_folder)
        # linux
        self.dandere_dir = config.get('dandere2x', 'dandere_dir')

        # User Settings
        self.time_frame = config.get('dandere2x', 'time_frame')
        self.duration = config.get('dandere2x', 'duration')
        self.audio_layer = config.get('dandere2x', 'audio_layer')
        self.frame_rate = config.get('dandere2x', 'frame_rate')
        self.width = config.get('dandere2x', 'width')
        self.height = config.get('dandere2x', 'height')
        self.block_size = int(config.get('dandere2x', 'block_size'))
        self.tolerance = config.get('dandere2x', 'tolerance')
        self.step_size = config.get('dandere2x', 'step_size')
        self.bleed = config.get('dandere2x', 'bleed')
        self.quality_low = int(config.get('dandere2x', 'quality_low'))
        self.quality_high = int(config.get('dandere2x', 'quality_high'))

        # waifu2x settings
        self.noise_level = config.get('dandere2x', 'noise_level')
        self.scale_factor = config.get('dandere2x', 'scale_factor')
        self.process_type = config.get('dandere2x', 'process_type')
        self.extension_type = config.get('dandere2x', 'extension_type')
        self.audio_type = config.get('dandere2x', 'audio_type')

        # setup directories
        self.input_frames_dir = self.workspace + "inputs" + os.path.sep
        self.differences_dir = self.workspace + "differences" + os.path.sep
        self.upscaled_dir = self.workspace + "upscaled" + os.path.sep
        self.correction_data_dir = self.workspace + "correction_data" + os.path.sep
        self.merged_dir = self.workspace + "merged" + os.path.sep
        self.inversion_data_dir = self.workspace + "inversion_data" + os.path.sep
        self.pframe_data_dir = self.workspace + "pframe_data" + os.path.sep
        self.debug_dir = self.workspace + "debug" + os.path.sep
        self.log_dir = self.workspace + "logs" + os.path.sep
        self.frame_count = get_seconds_from_time(self.duration) * int(self.frame_rate)

        logging.basicConfig(filename='dandere2x.log', level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        self.mse_min = 0
        self.mse_max = 0


    def pre_setup(self):
        self.logger.info("Starting new dandere2x session")
        self.create_dirs()
        self.extract_frames()
        self.extract_audio()
        self.create_waifu2x_script()
        self.write_frames()
        self.write_merge_commands()

        logging.basicConfig(filename=self.workspace + 'dandere2x.log', level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        self.set_mse()


    def set_mse(self):


        print("calculating mse")

        list = []
        for x in range(1, 15):
            num = random.randint(1, self.frame_count)
            f1 = Frame()
            f1.load_from_string(self.input_frames_dir + "frame" + str(num) + ".jpg")
            list.append(determine_sens(self.workspace, f1, self.quality_low, self.quality_high))

        output = [sum(y) / len(y) for y in zip(*list)]

        self.mse_max = output[0]
        self.mse_min = output[1]
        print("mse is ")
        print(output)


    # create a series of threads and external processes
    # to run in real time with each other for the dandere2x session.
    # the code is self documenting here.
    def run_concurrent(self):
        self.pre_setup()

        if self.waifu2x_type == "caffe":
            waifu2x = Waifu2xCaffe(self.workspace,
                                   self.frame_count,
                                   self.waifu2x_caffe_cui_dir,
                                   self.model_dir,
                                   self.differences_dir,
                                   self.upscaled_dir,
                                   self.process_type,
                                   self.noise_level,
                                   self.scale_factor)

            Waifu2xCaffe.upscale_file(self.workspace,
                                      self.waifu2x_caffe_cui_dir,
                                      self.model_dir,
                                      self.input_frames_dir + "frame1" + self.extension_type,
                                      self.merged_dir + "merged_1" + self.extension_type,
                                      self.process_type,
                                      self.noise_level,
                                      self.scale_factor)

        elif self.waifu2x_type == "conv":
            waifu2x = Waifu2xConv(self.workspace,
                                  self.frame_count,
                                  self.waifu2x_conv_dir,
                                  self.waifu2x_conv_dir_dir,
                                  self.differences_dir,
                                  self.upscaled_dir,
                                  self.noise_level,
                                  self.scale_factor)

            Waifu2xConv.upscale_file(self.workspace,
                                     self.waifu2x_conv_dir,
                                     self.waifu2x_conv_dir_dir,
                                     self.input_frames_dir + "frame1" + self.extension_type,
                                     self.merged_dir + "merged_1" + self.extension_type,
                                     self.noise_level,
                                     self.scale_factor)

        dandere2xcpp_thread = Dandere2xCppWrapper(self.workspace,
                                                  self.dandere2x_cpp_dir,
                                                  self.frame_count,
                                                  self.block_size,
                                                  self.tolerance,
                                                  self.mse_max,
                                                  self.mse_min,
                                                  self.step_size,
                                                  resume=False,
                                                  extension_type=self.extension_type)

        merge_thread = threading.Thread(target=merge_loop,
                                        args=(self.workspace,
                                              self.upscaled_dir,
                                              self.merged_dir,
                                              self.inversion_data_dir,
                                              self.pframe_data_dir,
                                              self.correction_data_dir,
                                              1,
                                              self.frame_count,
                                              self.block_size,
                                              self.scale_factor,
                                              self.extension_type))

        difference_thread = threading.Thread(target=difference_loop,
                                             args=(self.workspace,
                                                   self.differences_dir,
                                                   self.inversion_data_dir,
                                                   self.pframe_data_dir,
                                                   self.input_frames_dir,
                                                   1,
                                                   self.frame_count,
                                                   self.block_size,
                                                   self.extension_type))

        self.logger.info("Starting Threaded Processes..")

        waifu2x.start()
        merge_thread.start()
        difference_thread.start()
        dandere2xcpp_thread.start()

        merge_thread.join()
        dandere2xcpp_thread.join()
        difference_thread.join()
        waifu2x.join()

        self.logger.info("Threaded Processes Finished succcesfully")

    # Resume a Dandere2x Session
    def resume_concurrent(self):
        if self.waifu2x_type == "caffe":
            waifu2x = Waifu2xCaffe(self.workspace,
                                   self.frame_count,
                                   self.waifu2x_caffe_cui_dir,
                                   self.model_dir,
                                   self.differences_dir,
                                   self.upscaled_dir,
                                   self.process_type,
                                   self.noise_level,
                                   self.scale_factor)

        elif self.waifu2x_type == "conv":
            waifu2x = Waifu2xConv(self.workspace,
                                  self.frame_count,
                                  self.waifu2x_conv_dir,
                                  self.waifu2x_conv_dir_dir,
                                  self.differences_dir,
                                  self.upscaled_dir,
                                  self.noise_level,
                                  self.scale_factor)

        dandere2xcpp_thread = Dandere2xCppWrapper(self.workspace,
                                                  self.dandere2x_cpp_dir,
                                                  self.frame_count,
                                                  self.block_size,
                                                  self.tolerance,
                                                  self.mse_max,
                                                  self.mse_min,
                                                  self.step_size,
                                                  resume=True,
                                                  extension_type=self.extension_type)

        merge_thread = threading.Thread(target=merge_loop_resume,
                                        args=(self.workspace,
                                              self.upscaled_dir,
                                              self.merged_dir,
                                              self.inversion_data_dir,
                                              self.pframe_data_dir,
                                              self.correction_data_dir,
                                              self.frame_count,
                                              self.block_size,
                                              self.scale_factor,
                                              self.extension_type))

        difference_thread = threading.Thread(target=difference_loop_resume,
                                             args=(self.workspace,
                                                   self.upscaled_dir,
                                                   self.differences_dir,
                                                   self.inversion_data_dir,
                                                   self.pframe_data_dir,
                                                   self.input_frames_dir,
                                                   self.frame_count,
                                                   self.block_size,
                                                   self.extension_type))

        self.logger.info("Starting Threaded Processes..")
        waifu2x.start()
        merge_thread.start()
        difference_thread.start()
        dandere2xcpp_thread.start()

        merge_thread.join()
        dandere2xcpp_thread.join()
        difference_thread.join()
        waifu2x.join()

        self.logger.info("Threaded Processes Finished succcesfully")

    # only calculate the differences. To be implemented in video2x / converter-cpp
    def difference_only(self):
        self.pre_setup()

        dandere2xcpp_thread = Dandere2xCppWrapper(self.workspace,
                                                  self.dandere2x_cpp_dir,
                                                  self.frame_count,
                                                  self.block_size,
                                                  self.tolerance,
                                                  self.mse_max,
                                                  self.mse_min,
                                                  self.step_size,
                                                  resume=False,
                                                  extension_type=self.extension_type)

        difference_thread = threading.Thread(target=difference_loop,
                                             args=(self.workspace,
                                                   self.differences_dir,
                                                   self.inversion_data_dir,
                                                   self.pframe_data_dir,
                                                   self.input_frames_dir,
                                                   1,
                                                   self.frame_count,
                                                   self.block_size,
                                                   self.extension_type))

        self.logger.info("Starting Threaded Processes..")

        difference_thread.start()
        dandere2xcpp_thread.start()

        dandere2xcpp_thread.join()
        difference_thread.join()

    def merge_only(self):
        merge_thread = threading.Thread(target=merge_loop,
                                        args=(self.workspace,
                                              self.upscaled_dir,
                                              self.merged_dir,
                                              self.inversion_data_dir,
                                              self.pframe_data_dir,
                                              1,
                                              self.frame_count,
                                              self.block_size,
                                              self.scale_factor,
                                              self.extension_type))
        merge_thread.start()
        merge_thread.join()

    def create_dirs(self):
        directories = {self.input_frames_dir,
                       self.correction_data_dir,
                       self.differences_dir,
                       self.upscaled_dir,
                       self.merged_dir,
                       self.upscaled_dir,
                       self.merged_dir,
                       self.inversion_data_dir,
                       self.pframe_data_dir,
                       self.debug_dir,
                       self.log_dir}

        # need to create workspace befroe anything else
        try:
            os.mkdir(self.workspace)
        except OSError:
            print("Creation of the directory %s failed" % self.workspace)
        else:
            print("Successfully created the directory %s " % self.workspace)

        for subdirectory in directories:
            try:
                os.mkdir(subdirectory)
            except OSError:
                print("Creation of the directory %s failed" % subdirectory)
            else:
                print("Successfully created the directory %s " % subdirectory)


    def extract_frames(self):
        ffmpeg_extract_frames(self.ffmpeg_dir,
                              self.time_frame,
                              self.file_dir,
                              self.frame_rate,
                              self.duration,
                              self.input_frames_dir,
                              self.extension_type)

    def extract_audio(self):
        ffmpeg_extract_audio(self.ffmpeg_dir,
                             self.time_frame,
                             self.file_dir,
                             self.audio_layer,
                             self.duration,
                             self.workspace,
                             self.audio_type)

    # for linux
    def create_waifu2x_script(self):
        input_list = []
        input_list.append("cd /home/linux/Documents/waifu2x/")

        input_list.append(
            "th " + self.dandere_dir + " -m noise_scale -noise_level 3 -i " +
            self.input_frames_dir + "frame1" + self.extension_type +
            " -o " + self.merged_dir + "merged_1" + self.extension_type + "\n")

        input_list.append("th " + self.dandere_dir + " -m noise_scale -noise_level 3 -resume 1 -l " +
                          self.workspace + "frames.txt -o " + self.upscaled_dir + "output_%d.png")

        with open(self.workspace + os.path.sep + 'waifu2x_script.sh', 'w') as f:
            for item in input_list:
                f.write("%s\n" % item)

        os.chmod(self.workspace + os.path.sep + 'waifu2x_script.sh', 0o777)

    # for linux
    def write_frames(self):
        with open(self.workspace + os.path.sep + 'frames.txt', 'w') as f:
            for x in range(1, self.frame_count):
                f.write(self.differences_dir + "output_" + str(x) + ".png\n")

    # for re-merging the files after runtime is done
    def write_merge_commands(self):
        with open(self.workspace + os.path.sep + 'commands.txt', 'w') as f:
            f.write(
                self.ffmpeg_dir + " -f image2 -framerate " + self.frame_rate + " -i " + self.merged_dir + "merged_%d.jpg -r " + self.frame_rate + " -vf deband " + self.workspace + "nosound.mp4\n\n")
            f.write(
                self.ffmpeg_dir + " -i " + self.workspace + "nosound.mp4" + " -i " + self.workspace + "audio" + self.audio_type + " -c copy " +
                self.workspace + "sound.mp4\n\n")
