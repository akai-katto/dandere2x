"""
Name: Dandere2X Frame
Author: CardinalPanda
Date Created: 5-4-2019
Last Modified: 5-4-2019

Description:

Have all the variables used in Dandere2x stored in here
and have this class be passed to scripts
rather than passing like 8-9 variables
"""

import json
import logging
import os
import sys

from dandere2x_core.dandere2x_utils import get_options_from_section
from wrappers.videosettings import VideoSettings


# init is pretty messy at the moment. I'll look into
# cleaning this up in the future ;-;
class Context:

    def __init__(self, config_json: json):

        # load 'this folder' in a pyinstaller friendly way
        self.this_folder = ''

        if getattr(sys, 'frozen', False):
            self.this_folder = os.path.dirname(sys.executable) + os.path.sep
        elif __file__:
            self.this_folder = os.path.dirname(__file__) + os.path.sep

        # in this section right here, we need to absolutify the
        # json paths in the json file. Meaning, ../ -> C:\stuff\
        # We do this by creating a string representation of the json, changing the hard codings,
        # then renaming the variables from python styled json to normal json, then
        # parsing it back.

        current_folder_json = ''

        if getattr(sys, 'frozen', False):
            current_folder_json = os.path.dirname(sys.executable)
        elif __file__:
            current_folder_json = os.path.dirname(__file__)

        current_folder_json = current_folder_json.replace("\\", "\\\\")

        config_json_string = str(config_json)

        # turn python's string'd json into a normal json
        config_json_string = config_json_string.replace("\'", "\"")
        config_json_string = config_json_string.replace("True", "true")
        config_json_string = config_json_string.replace("False", "true")
        config_json_string = config_json_string.replace("None", "null")
        config_json_string = config_json_string.replace("..", current_folder_json)

        #load the json back into the config
        config_json = json.loads(config_json_string)
        self.config_json = config_json

        # directories
        self.waifu2x_caffe_cui_dir = config_json['waifu2x_caffe']['waifu2x_caffe_path']

        self.workspace = config_json['dandere2x']['workspace']
        self.file_dir = config_json['dandere2x']['file_dir']
        self.output_file = config_json['dandere2x']['output_file']

        self.dandere2x_cpp_dir = config_json['dandere2x']['dandere2x_cpp_dir']

        self.ffmpeg_dir = config_json['ffmpeg']['ffmpeg_path'] + "ffmpeg.exe"
        self.ffprobe_dir = config_json['ffmpeg']['ffmpeg_path'] + "ffprobe.exe"

        self.waifu2x_type = config_json['dandere2x']['waifu2x_type']

        self.waifu2x_converter_cpp_dir = os.path.join(config_json['waifu2x_converter']['waifu2x_converter_path'],
                                             "waifu2x-converter-cpp.exe")

        self.waifu2x_converter_cpp_dir_dir = config_json['waifu2x_converter']['waifu2x_converter_path']

        self.waifu2x_vulkan_dir = os.path.join(config_json['waifu2x_ncnn_vulkan']['waifu2x_ncnn_vulkan_path'],
                                               "waifu2x-ncnn-vulkan.exe")

        self.waifu2x_vulkan_dir_dir = config_json['waifu2x_ncnn_vulkan']['waifu2x_ncnn_vulkan_path']

        self.video_settings = VideoSettings(self.ffprobe_dir, self.file_dir)

        self.frame_rate = self.video_settings.frame_rate
        self.width = self.video_settings.width
        self.height = self.video_settings.height

        # find out if the user trimmed a video by checking the time part of the json. IF theres nothing there,
        # then the user didn't trim anything
        self.user_trim_video = False
        find_out_if_trim = get_options_from_section(config_json["ffmpeg"]["trim_video"]['time'])

        if find_out_if_trim:
            self.user_trim_video = True

        # linux
        self.dandere_dir = 'lol what linux'

        # D2x Settings
        self.block_size = config_json['dandere2x']['block_size']
        self.step_size = config_json['dandere2x']['step_size']
        self.bleed = config_json['dandere2x']['bleed']
        self.quality_low = config_json['dandere2x']['quality_low']
        self.realtime_encoding = config_json['dandere2x']['realtime_encoding']
        self.realtime_encoding_delete_files = config_json['dandere2x']['realtime_encoding_delete_files']

        # todo idunno if theres a better way to figure out how many frames will be used.
        self.frame_count = 0

        # waifu2x settings
        self.noise_level = config_json['dandere2x']['noise_level']
        self.scale_factor = config_json['dandere2x']['scale_factor']
        self.extension_type = config_json['dandere2x']['extension_type']

        # setup directories
        self.input_frames_dir = self.workspace + "inputs" + os.path.sep
        self.differences_dir = self.workspace + "differences" + os.path.sep
        self.upscaled_dir = self.workspace + "upscaled" + os.path.sep
        self.correction_data_dir = self.workspace + "correction_data" + os.path.sep
        self.merged_dir = self.workspace + "merged" + os.path.sep
        self.inversion_data_dir = self.workspace + "inversion_data" + os.path.sep
        self.pframe_data_dir = self.workspace + "pframe_data" + os.path.sep
        self.fade_data_dir = self.workspace + "fade_data" + os.path.sep
        self.debug_dir = self.workspace + "debug" + os.path.sep
        self.log_dir = self.workspace + "logs" + os.path.sep
        self.compressed_dir = self.workspace + "compressed" + os.path.sep
        self.encoded_dir = self.workspace + "encoded" + os.path.sep

        # Absoluteify Some stuff

        # Developer Settings #
        self.debug = config_json['dandere2x']['debug']

    # the workspace folder needs to exist before creating the log file, hence the method
    def set_logger(self):
        logging.basicConfig(filename=self.workspace + 'dandere2x.log', level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def close_logger(self):
        handlers = self.logger.handlers[:]
        for handler in handlers:
            handler.close()
            self.logger.removeHandler(handler)

    def update_frame_count(self):
        self.frame_count = len([name for name in os.listdir(self.input_frames_dir)
                                if os.path.isfile(os.path.join(self.input_frames_dir, name))])
