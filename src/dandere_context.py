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

        # directories
        self.waifu2x_caffe_cui_dir = config_json['waifu2x_caffe']['waifu2x_caffe_path']

        self.workspace = config_json['dandere2x']['workspace']
        self.file_dir = config_json['dandere2x']['file_dir']

        self.dandere2x_cpp_dir = config_json['dandere2x']['dandere2x_cpp_dir']

        self.ffmpeg_dir = config_json['ffmpeg']['ffmpeg_path'] + "ffmpeg.exe"
        self.ffprobe_dir = config_json['ffmpeg']['ffmpeg_path'] + "ffprobe.exe"

        self.waifu2x_type = config_json['dandere2x']['waifu2x_type']

        self.waifu2x_conv_dir = config_json['waifu2x_converter']['waifu2x_converter_path']
        self.waifu2x_conv_dir_dir = config_json['waifu2x_converter']['waifu2x_converter_path'] + "missing.exe"

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

        # Developer Settings #
        self.debug = config_json['dandere2x']['debug']

        # Waifu2x-wrappers Commands

        # Create Vulkan Command
        self.waifu2x_vulkan_upscale_frame = [self.waifu2x_vulkan_dir,
                                             "-i", "[input_file]",
                                             "-n", str(self.noise_level),
                                             "-s", str(self.scale_factor)]

        waifu2x_vulkan_options = get_options_from_section(config_json["waifu2x_ncnn_vulkan"]["output_options"])

        # add custom options to waifu2x_vulkan
        for element in waifu2x_vulkan_options:
            self.waifu2x_vulkan_upscale_frame.append(element)

        self.waifu2x_vulkan_upscale_frame.extend(["-o", "[output_file]"])

        # Create Caffe Command
        self.waifu2x_caffe_upscale_frame = [self.waifu2x_caffe_cui_dir,
                                             "-i", "[input_file]",
                                             "-n", str(self.noise_level),
                                             "-s", str(self.scale_factor)]

        waifu2x_caffe_options = get_options_from_section(config_json["waifu2x_caffe"]["output_options"])

        for element in waifu2x_caffe_options:
            self.waifu2x_caffe_upscale_frame.append(element)

        self.waifu2x_caffe_upscale_frame.extend(["-o", "[output_file]"])

        ## FFMPEG Options ##

        self.trim_video_command = [self.ffmpeg_dir, "-i", "[input_file]"]

        trim_video_time = get_options_from_section(config_json["ffmpeg"]["trim_video"]["time"])

        for element in trim_video_time:
            self.trim_video_command.append(element)

        trim_video_options =  get_options_from_section(config_json["ffmpeg"]["trim_video"]["output_options"])

        for element in trim_video_options:
            self.trim_video_command.append(element)

        self.trim_video_command.append("[output_file]")

        print("Trim video command")
        print(self.trim_video_command)


        # Create extract frames command
        self.extract_frames_command = [self.ffmpeg_dir, "-i", "[input_file]"]


        extract_frames_options = get_options_from_section(config_json["ffmpeg"]["video_to_frames"]['output_options'])
        for element in extract_frames_options:
            self.extract_frames_command.append(element)

        self.extract_frames_command.extend(["[output_file]"])

        self.video_from_frames_command = [self.ffmpeg_dir,
                                          "-start_number", "[start_number]",
                                          "-i", "[input_file]",
                                          "-vframes", "[frames_per_video]",
                                          "-r", str(self.frame_rate)]

        frame_to_video_option = get_options_from_section(config_json["ffmpeg"]["frames_to_video"]['output_options'])

        for element in frame_to_video_option:
            self.video_from_frames_command.append(element)

        self.video_from_frames_command.extend(["[output_file]"])

        # MIGRATE TRACKS
        # comment - this is hard coded at the moment, I couldn't figure out how video2x was able to get
        # multiple key / dict pairs
        self.migrate_tracks_command = [self.ffmpeg_dir,
                                       "-i", "[no_audio]",
                                       "-i", "[video_sound]",
                                       "-map", "0:v:0?",
                                       "-map", "1?",
                                       "-c", "copy",
                                       "-map", "-1:v?"]

        migrate_tracks_options = get_options_from_section(config_json["ffmpeg"]["migrating_tracks"]['output_options'])

        for element in migrate_tracks_options:
            self.migrate_tracks_command.append(element)

        self.migrate_tracks_command.extend(["[output_file]"])

        self.merge_video_command = "[ffmpeg_dir] -f concat -safe 0 -i [text_file] -c:v libx264 -crf 17 [output_file]"

        try:
            os.mkdir(self.workspace)
        except:
            pass

        logging.basicConfig(filename=self.workspace + 'dandere2x.log', level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def update_frame_count(self):
        self.frame_count = len([name for name in os.listdir(self.input_frames_dir)
                                if os.path.isfile(os.path.join(self.input_frames_dir, name))])
