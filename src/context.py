"""

Description:

Rather than feed functions stuff like block_size, ffmpeg_dir each time, all the variables needed for every
Dandere2x sub-function call is within

"""

import json
import logging
import os
import pathlib
import sys
import tempfile

import math

from dandere2xlib.utils.json_utils import get_options_from_section, absolutify_json
from wrappers.ffmpeg.videosettings import VideoSettings


class Context:

    # This is probably the most disorganized part of Dandere2x - everything else is fine.
    # If you don't want to read through the init, essentially creates all the variables we need
    # from the json and puts them into an object we can pass around Dandere2x pretty liberally

    def __init__(self, config_json_unparsed: json):

        # load 'this folder' in a pyinstaller friendly way
        self.this_folder = None

        if getattr(sys, 'frozen', False):
            self.this_folder = os.path.dirname(sys.executable)
        elif __file__:
            self.this_folder = os.path.dirname(__file__)

        self.this_folder = pathlib.Path(self.this_folder)

        # We need the json to be absolute, meaning ".." --> this.folder
        # This allows Dandere2x to be somewhat portable on different systems

        self.config_json = absolutify_json(config_json_unparsed, str(self.this_folder.absolute()), absolutify_key="..")

        ################################
        #  setup all the directories.. #
        ################################

        # side note - for vulkan and converter, we need to know the path of the file in order for it to run correctly,
        # hence why we have two variables for them
        self.waifu2x_converter_cpp_path = self.config_json['waifu2x_converter']['waifu2x_converter_path']
        self.waifu2x_converter_cpp_dir = os.path.join(self.waifu2x_converter_cpp_path, "waifu2x-converter-cpp.exe")

        self.waifu2x_vulkan_path = self.config_json['waifu2x_ncnn_vulkan']['waifu2x_ncnn_vulkan_path']
        self.waifu2x_vulkan_dir = os.path.join(self.waifu2x_vulkan_path, "waifu2x-ncnn-vulkan.exe")

        self.waifu2x_caffe_cui_dir = pathlib.Path(self.config_json['waifu2x_caffe']['waifu2x_caffe_path'])

        self.workspace = self.config_json['dandere2x']['developer_settings']['workspace']
        self.workspace_use_temp = self.config_json['dandere2x']['developer_settings']['workspace_use_temp']

        # if we're using a temporary workspace, assign workspace to be in the temp folder
        if self.workspace_use_temp:
            self.workspace = os.path.join(pathlib.Path(tempfile.gettempdir()), 'dandere2x') + "\\"

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
        self.compressed_static_dir = self.workspace + "compressed_static" + os.path.sep
        self.compressed_moving_dir = self.workspace + "compressed_moving" + os.path.sep
        self.encoded_dir = self.workspace + "encoded" + os.path.sep
        self.temp_image_folder = self.workspace + "temp_image_folder" + os.path.sep

        self.ffmpeg_dir = self.config_json['ffmpeg']['ffmpeg_path']
        self.ffprobe_dir = self.config_json['ffmpeg']['ffprobe_path']
        self.hwaccel = self.config_json['ffmpeg']['-hwaccel']

        ################################
        # Load Dandere2x User Settings #
        ################################

        # User Settings
        self.block_size = self.config_json['dandere2x']['usersettings']['block_size']
        self.quality_minimum = self.config_json['dandere2x']['usersettings']['quality_minimum']
        self.waifu2x_type = self.config_json['dandere2x']['usersettings']['waifu2x_type']
        self.noise_level = self.config_json['dandere2x']['usersettings']['denoise_level']
        self.scale_factor = self.config_json['dandere2x']['usersettings']['scale_factor']
        self.input_file = self.config_json['dandere2x']['usersettings']['input_file']
        self.output_file = self.config_json['dandere2x']['usersettings']['output_file']

        # Developer Settings

        self.quality_moving_ratio = self.config_json['dandere2x']['developer_settings']['quality_moving_ratio']
        self.step_size = self.config_json['dandere2x']['developer_settings']['step_size']
        self.bleed = self.config_json['dandere2x']['developer_settings']['bleed']
        self.extension_type = self.config_json['dandere2x']['developer_settings']['extension_type']
        self.debug = self.config_json['dandere2x']['developer_settings']['debug']
        self.dandere2x_cpp_dir = self.config_json['dandere2x']['developer_settings']['dandere2x_cpp_dir']
        self.correction_block_size = 2

        # Real Time Encoding

        self.realtime_encoding_enabled = self.config_json['dandere2x']['developer_settings']['realtime_encoding'][
            'realtime_encoding_enabled']
        self.realtime_encoding_delete_files = self.config_json['dandere2x']['developer_settings']['realtime_encoding'][
            'realtime_encoding_delete_files']
        self.realtime_encoding_seconds_per_video = \
        self.config_json['dandere2x']['developer_settings']['realtime_encoding']['realtime_encoding_seconds_per_video']

        ################################
        #       Video Settings         #
        ################################

        # find out if the user trimmed a video by checking the time part of the json. IF theres nothing there,
        # then the user didn't trim anything
        self.user_trim_video = False
        find_out_if_trim = get_options_from_section(self.config_json["ffmpeg"]["trim_video"]['time'])

        if find_out_if_trim:
            self.user_trim_video = True

        self.video_settings = VideoSettings(self.ffprobe_dir, self.input_file)

        self.frame_rate = math.ceil(self.video_settings.frame_rate)
        self.width = self.video_settings.width
        self.height = self.video_settings.height
        self.frame_count = 0

    # the workspace folder needs to exist before creating the log file, hence the method
    def set_logger(self):
        logging.basicConfig(filename=os.path.join(self.workspace, 'dandere2x.log'), level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def close_logger(self):
        logging.shutdown()

    # this can be done with fprobe I guess, but why change things, you feel
    def update_frame_count(self):
        self.frame_count = len([name for name in os.listdir(self.input_frames_dir)
                                if os.path.isfile(os.path.join(self.input_frames_dir, name))])
