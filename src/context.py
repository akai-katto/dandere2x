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
import tempfile
import pathlib

from dandere2xlib.utils.json_utils import get_options_from_section, absolutify_json
from dandere2xlib.utils.dandere2x_utils import valid_input_resolution, get_a_valid_input_resolution

from wrappers.videosettings import VideoSettings


# init is pretty messy at the moment. I'll look into
# cleaning this up in the future ;-;
class Context:


    # todo implement os.path.join for all directory stuff
    # to clean up the mess that I've made
    def __init__(self, config_json_unparsed: json):

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

        self.config_json = absolutify_json(config_json_unparsed, current_folder_json, absolutify_key="..")
        # directories
        self.waifu2x_caffe_cui_dir = self.config_json['waifu2x_caffe']['waifu2x_caffe_path']


        self.ffmpeg_dir = self.config_json['ffmpeg']['ffmpeg_path'] + "ffmpeg.exe"
        self.ffprobe_dir = self.config_json['ffmpeg']['ffmpeg_path'] + "ffprobe.exe"
        self.hwaccel = self.config_json['ffmpeg']['-hwaccel']


        self.waifu2x_converter_cpp_dir = os.path.join(self.config_json['waifu2x_converter']['waifu2x_converter_path'],
                                             "waifu2x-converter-cpp.exe")

        self.waifu2x_converter_cpp_dir_dir = self.config_json['waifu2x_converter']['waifu2x_converter_path']

        self.waifu2x_vulkan_dir = os.path.join(self.config_json['waifu2x_ncnn_vulkan']['waifu2x_ncnn_vulkan_path'],
                                               "waifu2x-ncnn-vulkan.exe")

        self.waifu2x_vulkan_dir_dir = self.config_json['waifu2x_ncnn_vulkan']['waifu2x_ncnn_vulkan_path']


        # find out if the user trimmed a video by checking the time part of the json. IF theres nothing there,
        # then the user didn't trim anything
        self.user_trim_video = False
        find_out_if_trim = get_options_from_section(self.config_json["ffmpeg"]["trim_video"]['time'])

        if find_out_if_trim:
            self.user_trim_video = True

        # linux
        self.dandere_dir = 'lol what linux'

        # User Settings
        self.block_size = self.config_json['dandere2x']['usersettings']['block_size']
        self.quality_low = self.config_json['dandere2x']['usersettings']['quality_low']
        self.waifu2x_type = self.config_json['dandere2x']['usersettings']['waifu2x_type']
        self.noise_level = self.config_json['dandere2x']['usersettings']['noise_level']
        self.scale_factor = self.config_json['dandere2x']['usersettings']['scale_factor']
        self.file_dir = self.config_json['dandere2x']['usersettings']['file_dir']
        self.output_file = self.config_json['dandere2x']['usersettings']['output_file']
        # Developer Settings

        self.step_size = self.config_json['dandere2x']['developer_settings']['step_size']
        self.bleed = self.config_json['dandere2x']['developer_settings']['bleed']
        self.extension_type = self.config_json['dandere2x']['developer_settings']['extension_type']
        self.debug = self.config_json['dandere2x']['developer_settings']['debug']
        self.realtime_encoding = self.config_json['dandere2x']['developer_settings']['realtime_encoding']
        self.realtime_encoding_delete_files = self.config_json['dandere2x']['developer_settings']['realtime_encoding_delete_files']
        self.workspace_use_temp = self.config_json['dandere2x']['developer_settings']['workspace_use_temp']
        self.workspace = self.config_json['dandere2x']['developer_settings']['workspace']
        self.dandere2x_cpp_dir = self.config_json['dandere2x']['developer_settings']['dandere2x_cpp_dir']

        # if we're using a temporary workspace, assign workspace to be in the temp folder

        if self.workspace_use_temp:
            self.workspace = os.path.join(pathlib.Path(tempfile.gettempdir()),  'dandere2x') + "\\"

        self.video_settings = VideoSettings(self.ffprobe_dir, self.file_dir)

        self.frame_rate = self.video_settings.frame_rate
        self.width = self.video_settings.width
        self.height = self.video_settings.height

        # todo idunno if theres a better way to figure out how many frames will be used.
        self.frame_count = 0

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
        self.temp_image_folder = self.workspace + "temp_image_folder" + os.path.sep

        # force a valid resolution
        if not valid_input_resolution(self.width, self.height, self.block_size):
            print("Forcing Resizing to match blocksize..")
            width, height = get_a_valid_input_resolution(self.width, self.height, self.block_size)

            print("New width -> " + str(width))
            print("New height -> " + str(height))

            self.width = width
            self.height = height

            self.config_json['ffmpeg']['video_to_frames']['output_options']['-vf']\
                .append("scale=" + str(self.width) + ":" + str(self.height))



    # the workspace folder needs to exist before creating the log file, hence the method
    def set_logger(self):
        logging.basicConfig(filename=os.path.join(self.workspace, 'dandere2x.log' ), level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def close_logger(self):
        logging.shutdown()

    # this can be done with fprobe I guess, but why change things, you feel
    def update_frame_count(self):
        self.frame_count = len([name for name in os.listdir(self.input_frames_dir)
                                if os.path.isfile(os.path.join(self.input_frames_dir, name))])
