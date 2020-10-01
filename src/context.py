"""
    This file is part of the Dandere2x project.
    Dandere2x is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    Dandere2x is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with Dandere2x.  If not, see <https://www.gnu.org/licenses/>.
""""""
========= Copyright aka_katto 2018, All rights reserved. ============
Original Author: aka_katto 
Purpose: 'Context' serves as a controller-class wherein variables
          are all stored in here, and passed to dandere2x objects
          to avoid needing to pass a million variables. Each variable
          is assumed to be static (with exception to video_settings, 
          which is loaded during runtime), as well as 
====================================================================="""

import logging
import os
import pathlib
import sys

import yaml

from dandere2x.controller import Controller
from dandere2xlib.utils.yaml_utils import absolutify_yaml
from wrappers.ffmpeg.videosettings import VideoSettings


class Context:
    """
    This class is a mega-structure like file to house all the variables and directories needed for dandere2x to work.
    Rather than passing around the needed variables for dandere2x related functions, we simply put everything
    Dandere2x related in here and are loaded in various methods. You'll see this class become used a lot during
    D2x's development - keep this file clean and nice, as it'll be used more than anything else!
    """

    def __init__(self, config_file_unparsed: yaml):
        """
        Create all the needed values that will be used in various parts of dandere2x. A lot of these values
        are derived from external files, such as the json, ffmpeg and ffprobe, or are joined from directories.

        Having all the variables here allows dandere2x the values needed to be global, but at the same time not really.
        """

        self.this_folder = None

        # load 'this_folder' in a pyinstaller friendly way
        if getattr(sys, 'frozen', False):
            self.this_folder = os.path.dirname(sys.executable)
        elif __file__:
            self.this_folder = os.path.dirname(__file__)

        self.this_folder = pathlib.Path(self.this_folder)
        self.config_file_unparsed = config_file_unparsed

        # Parse the unparsed config into a parsed (../externals -> C:/this_folder/externals)
        self.config_yaml = absolutify_yaml(config_file_unparsed, str(self.this_folder.absolute()), absolutify_key="..")

        ################################
        #  setup all the directories.. #
        ################################
        self.waifu2x_converter_cpp_path = self.config_yaml['waifu2x_converter']['waifu2x_converter_path']
        self.waifu2x_converter_file_name = self.config_yaml['waifu2x_converter']['waifu2x_converter_file_name']
        self.waifu2x_converter_cpp_file_path = os.path.join(self.waifu2x_converter_cpp_path,
                                                            self.waifu2x_converter_file_name)

        self.waifu2x_ncnn_vulkan_path = self.config_yaml['waifu2x_ncnn_vulkan']['waifu2x_ncnn_vulkan_path']
        self.waifu2x_ncnn_vulkan_file_name = self.config_yaml['waifu2x_ncnn_vulkan']['waifu2x_ncnn_vulkan_file_name']
        self.waifu2x_ncnn_vulkan_legacy_file_name = os.path.join(self.waifu2x_ncnn_vulkan_path,
                                                                 self.waifu2x_ncnn_vulkan_file_name)

        self.realsr_ncnn_vulkan_path = self.config_yaml['realsr_ncnn_vulkan']['realsr_ncnn_vulkan_path']
        self.realsr_ncnn_vulkan_file_name = self.config_yaml['realsr_ncnn_vulkan']['realsr_ncnn_vulkan_file_name']
        self.realsr_ncnn_vulkan_file_path = os.path.join(self.realsr_ncnn_vulkan_path,
                                                         self.realsr_ncnn_vulkan_file_name)

        self.waifu2x_caffe_cui_dir = self.config_yaml['waifu2x_caffe']['waifu2x_caffe_path']

        self.workspace = self.config_yaml['dandere2x']['developer_settings']['workspace']

        # setup directories
        self.log_folder_dir = self.config_yaml['dandere2x']['usersettings']['log_folder']
        self.input_frames_dir = self.workspace + "inputs" + os.path.sep
        self.residual_images_dir = self.workspace + "residual_images" + os.path.sep
        self.residual_upscaled_dir = self.workspace + "residual_upscaled" + os.path.sep
        self.residual_data_dir = self.workspace + "residual_data" + os.path.sep
        self.pframe_data_dir = self.workspace + "pframe_data" + os.path.sep
        self.correction_data_dir = self.workspace + "correction_data" + os.path.sep
        self.merged_dir = self.workspace + "merged" + os.path.sep
        self.fade_data_dir = self.workspace + "fade_data" + os.path.sep
        self.debug_dir = self.workspace + "debug" + os.path.sep
        self.console_output_dir = self.workspace + "console_output" + os.path.sep
        self.compressed_static_dir = self.workspace + "compressed_static" + os.path.sep
        self.encoded_dir = self.workspace + "encoded" + os.path.sep
        self.temp_image_folder = self.workspace + "temp_image_folder" + os.path.sep

        # put all the directories that need to be created into a list for creation / deleting.
        self.directories = {self.input_frames_dir,
                            self.correction_data_dir,
                            self.residual_images_dir,
                            self.residual_upscaled_dir,
                            self.merged_dir,
                            self.residual_data_dir,
                            self.pframe_data_dir,
                            self.debug_dir,
                            self.console_output_dir,
                            self.compressed_static_dir, 
                            self.fade_data_dir,
                            self.encoded_dir,
                            self.temp_image_folder}

        self.ffmpeg_dir = self.config_yaml['ffmpeg']['ffmpeg_path']
        self.ffprobe_dir = self.config_yaml['ffmpeg']['ffprobe_path']
        self.hwaccel = self.config_yaml['ffmpeg']['-hwaccel']

        ################################
        # Load Dandere2x User Settings #
        ################################

        # User Settings
        self.block_size = self.config_yaml['dandere2x']['usersettings']['block_size']
        self.quality_minimum = self.config_yaml['dandere2x']['usersettings']['quality_minimum']
        self.waifu2x_type = self.config_yaml['dandere2x']['usersettings']['waifu2x_type']
        self.noise_level = self.config_yaml['dandere2x']['usersettings']['denoise_level']
        self.scale_factor = self.config_yaml['dandere2x']['usersettings']['scale_factor']
        self.input_file = self.config_yaml['dandere2x']['usersettings']['input_file']
        self.output_file = self.config_yaml['dandere2x']['usersettings']['output_file']
        self.preserve_frames = self.config_yaml['dandere2x']['usersettings']['preserve_frames']
        self.input_folder = self.config_yaml['dandere2x']['usersettings']['input_folder']
        self.output_folder = self.config_yaml['dandere2x']['usersettings']['output_folder']
        self.output_extension = os.path.splitext(self.output_file)[1]

        # Developer Settings
        self.pre_process = self.config_yaml['dandere2x']['developer_settings']['pre_process']
        self.step_size = self.config_yaml['dandere2x']['developer_settings']['step_size']
        self.bleed = self.config_yaml['dandere2x']['developer_settings']['bleed']
        self.extension_type = self.config_yaml['dandere2x']['developer_settings']['extension_type']
        self.debug = self.config_yaml['dandere2x']['developer_settings']['debug']
        self.dandere2x_cpp_dir = self.config_yaml['dandere2x']['developer_settings']['dandere2x_cpp_dir']
        self.correction_block_size = 2
        self.delete_workspace_after = self.config_yaml['dandere2x']['developer_settings']['delete_workspace_after']
        self.max_frames_ahead = self.config_yaml['dandere2x']['developer_settings']['max_frames_ahead']
        self.sound_file = self.config_yaml['dandere2x']['usersettings']['input_file']

        # Session Related Variables
        self.nosound_file = os.path.join(self.workspace, "nosound" + self.output_extension)
        self.pre_processed_video = self.workspace + "pre_processed" + self.output_extension
        self.start_frame = self.config_yaml['resume_settings']['last_saved_frame']
        self.controller = Controller()

        ##################
        # Video Settings #
        ##################

        # ffprobe video settings
        self.width, self.height = None, None
        self.dar = None
        self.rotate = None
        self.frame_rate = None

        # cv2 video settings
        self.frame_count = None

        ###################
        # Resume Settings #
        ###################
        self.resume_session = self.config_yaml['resume_settings']['resume_session']
        self.last_saved_frame = self.config_yaml['resume_settings']['last_saved_frame']
        self.incomplete_video = self.config_yaml['resume_settings']['incomplete_video']

    def load_video_settings_ffprobe(self, file: str):
        """
        file: what to video file to load
        load_type: whether to load video settings with cv2 or ffprobe
        """
        video_settings = VideoSettings(self.ffprobe_dir, file)
        self.width, self.height = video_settings.width, video_settings.height
        self.dar = video_settings.dar
        self.rotate = video_settings.rotate
        self.frame_rate = video_settings.frame_rate

    def load_pre_processed_video(self, file: str):
        video_settings = VideoSettings(self.ffprobe_dir, file)
        self.width, self.height = video_settings.width, video_settings.height
        self.frame_rate = video_settings.frame_rate
        self.frame_count = video_settings.frame_count


    def log_all_variables(self):
        log = logging.getLogger()

        log.info("Context Settings:")
        for item in self.__dict__:
            log.info("%s : %s" % (item, self.__dict__[item]))

    def update_frame_count(self):
        """
        Count how many frames exist in the 'inputs_frames_dir' to signal to dandere2x how many frames
        will be needed during runtime. Observe that we don't use ffprobe's 'frame_count' function,
        as we we apply various filters which may affect total frame count.
        """
        self.frame_count = len([name for name in os.listdir(self.input_frames_dir)
                                if os.path.isfile(os.path.join(self.input_frames_dir, name))])
