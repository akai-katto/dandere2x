from abc import ABC
import sys
from os import path

from dandere2x.dandere2x_interface import Dandere2xInterface
from dandere2xlib.utils.dandere2x_utils import force_delete_directory, valid_input_resolution, create_directories
from wrappers.ffmpeg.ffmpeg import append_video_resize_filter

class Test:

    def __init__(self):
        self.test = "test"

    def print(self):
        print(path.abspath(sys.modules['__main__'].__file__))


# class Dandere2xSingleProcess(Dandere2xInterface):
#
#     def __init__(self):
#         super().__init__()
#
#     def pre_process(self):
#         """
#         This MUST be the first thing `run` calls, or else dandere2x_core.py will not work!
#
#         Description: This function is a series of instructions dandere2x MUST perform before the main threads
#                      are able to be called, and serves as a preliminary "health checker" for dandere2x to diagnose
#                      bugs before the main threads are called.
#         """
#
#         self.log.info("Beginning pre-processing stage.")
#         self.log.info("Dandere2x will process your video in a way that attempts to remove ambiguities caused by"
#                       " container formats.")
#
#         force_delete_directory(self.context.workspace)
#
#         try:
#             self.context.load_video_settings_ffprobe(file=self.context.input_file)
#         except FileNotFoundError as e:
#             from sys import exit
#             self.log.error("Caught FileNotFoundError. This is likeley caused by 'externals' missing a neccecary file.")
#             self.log.error("Are you sure you hit the 'download externals' button?")
#             exit(1)
#
#         if not valid_input_resolution(self.context.width, self.context.height, self.context.block_size):
#             """
#             Dandere2x needs the width and height to be a share a common factor with the block size so append a video
#             filter if needed to make the size conform. For example, 1921x1081 is not evenly divisalbe by 30, so we'd
#             need to resize the video in that scenario.
#             """
#
#             self.log.warning(
#                 "Input video needs to be resized to be compatible with block-size - this is expected behaviour.")
#             append_video_resize_filter(self.context)
#
#         self.set_file_logger(self.context.workspace + "log.txt")  # write to a log file in the workspace
#
#         self.waifu2x.verify_upscaling_works()
#
#         """
#         Re-encode the user input video. We do this because file container formats can be difficult to work with
#         and can cause Dandere2x to not function properly (some videos resolutions are different, variable frame rate
#         will cause video to have black spots, etc.
#         """
#         workspace = self.context.workspace
#         input_file = self.context.input_file
#         unmigrated = workspace + "d2x_input_video_nonmigrated.mkv"
#         pre_processed_video = self.context.pre_processed_video
#
#         # have dandere2x load up the pre-processed video and re-assign video settings to use that instead
#         re_encode_video(self.context, input_file, unmigrated, throw_exception=True)
#         migrate_tracks(self.context, unmigrated, input_file, pre_processed_video, copy_if_failed=True)
#         os.remove(unmigrated)
#         wait_on_file(pre_processed_video, controller=self.context.controller)
#         self.context.load_pre_processed_video(file=pre_processed_video)