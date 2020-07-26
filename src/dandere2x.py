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
Purpose: 
 
====================================================================="""
import os
import sys
import threading
import time

from context import Context
from dandere2xlib.core.merge import Merge
from dandere2xlib.core.residual import Residual
from dandere2xlib.mindiskusage import MinDiskUsage
from dandere2xlib.status import Status
from dandere2xlib.utils.dandere2x_utils import show_exception_and_exit, file_exists, create_directories, \
    valid_input_resolution, rename_file, force_delete_directory, wait_on_file_controller
from wrappers.dandere2x_cpp import Dandere2xCppWrapper
from wrappers.ffmpeg.ffmpeg import re_encode_video, migrate_tracks, append_video_resize_filter, concat_two_videos
from wrappers.waifu2x.realsr_ncnn_vulkan import RealSRNCNNVulkan
from wrappers.waifu2x.waifu2x_caffe import Waifu2xCaffe
from wrappers.waifu2x.waifu2x_converter_cpp import Waifu2xConverterCpp
from wrappers.waifu2x.waifu2x_ncnn_vulkan import Waifu2xNCNNVulkan


class Dandere2x(threading.Thread):

    def __init__(self, context: Context):
        # Administrative Stuff
        import sys
        sys.excepthook = show_exception_and_exit  # set a custom except hook to prevent window from closing.
        threading.Thread.__init__(self, name="Dandere2x Thread")

        # Class Specific
        self.context = context
        self.alive = False

        # Declarations
        """ 
        These are re-set later, but due to lack of python member-variable declarations, they're initially set here so the IDE can 
        do autocomplete corrections / predictions. It's important they're correctly assigned when self.run() is called. 
        """
        self.min_disk_demon = MinDiskUsage(self.context)
        self.status_thread = Status(self.context)
        self.dandere2x_cpp_thread = Dandere2xCppWrapper(self.context)
        self.waifu2x = self._get_waifu2x_class(self.context.waifu2x_type)
        self.residual_thread = Residual(self.context)
        self.merge_thread = Merge(self.context)

    def _pre_processing(self):
        """ This MUST be the first thing `run` calls, or else dandere2x.py will not work! """

        force_delete_directory(self.context.workspace)
        self.context.load_video_settings(file=self.context.input_file)
        """ 
        Dandere2x needs the width and height to be a share a common factor with the block size so append a video
        filter if needed to make the size conform. 
        """
        if not valid_input_resolution(self.context.width, self.context.height, self.context.block_size):
            append_video_resize_filter(self.context)

        create_directories(self.context.workspace, self.context.directories)

        self.waifu2x.verify_upscaling_works()

        """ 
        Re-encode the user input video. We do this because file container formats can be difficult to work with
        and can cause Dandere2x to not function properly (some videos resolutions are different, variable frame rate
        will cause video to have black spots, etc. 
        """
        workspace = self.context.workspace
        input_file = self.context.input_file
        unmigrated = workspace + "d2x_input_video_nonmigrated.mkv"
        pre_processed_video = self.context.pre_processed_video

        re_encode_video(self.context, input_file, unmigrated, throw_exception=True)
        migrate_tracks(self.context, unmigrated, input_file, pre_processed_video, copy_if_failed=True)
        os.remove(unmigrated)
        wait_on_file_controller(pre_processed_video, controller=self.context.controller)
        self.context.load_video_settings(file=pre_processed_video)

    def run(self):
        self._pre_processing()

        # Assigning classes now that context is properly set.
        self.min_disk_demon = MinDiskUsage(self.context)
        self.status_thread = Status(self.context)
        self.dandere2x_cpp_thread = Dandere2xCppWrapper(self.context)
        self.waifu2x = self._get_waifu2x_class(self.context.waifu2x_type)
        self.residual_thread = Residual(self.context)
        self.merge_thread = Merge(self.context)

        self.__extract_frames()
        self.__upscale_first_frame()

        self.min_disk_demon.start()
        self.dandere2x_cpp_thread.start()
        self.merge_thread.start()
        self.residual_thread.start()
        self.waifu2x.start()
        self.status_thread.start()

        self.alive = True

    def kill(self):
        """
        Kill Dandere2x entirely. Everything started as a thread can be killed with controller.kill() except for
        d2x_cpp, since that runs as a subprocess.
        """

        self.dandere2x_cpp_thread.kill()
        self.context.controller.kill()

    def join(self, timeout=None):

        while not self.alive and self.context.controller.is_alive():
            time.sleep(1)

        self.min_disk_demon.join()
        self.dandere2x_cpp_thread.join()
        self.merge_thread.join()
        self.residual_thread.join()
        self.waifu2x.join()
        self.status_thread.join()

        if self.context.controller.is_alive():
            self._successful_completion()
        else:
            self._kill_conditions()

    def _successful_completion(self):
        if self.context.resume_session:
            print("Session is a resume session, concatenating two videos")
            file_to_be_concat = self.context.workspace + "file_to_be_concat.mp4"

            rename_file(self.context.nosound_file, file_to_be_concat)
            concat_two_videos(self.context, self.context.incomplete_video,
                              file_to_be_concat,
                              self.context.nosound_file)

        migrate_tracks(self.context, self.context.nosound_file,
                       self.context.sound_file, self.context.output_file)

        if self.context.delete_workspace_after:
            force_delete_directory(self.context.workspace)

    def _kill_conditions(self):
        """ Begin a series of kill conditions that will prepare dandere2x to resume the session once suspended.
        For the most part, this involves documenting all the variables needed for dandere2x to know where the last
        session left off at. """
        import yaml

        print("starting kill conditions")
        suspended_file = self.context.workspace + str(self.context.controller.get_current_frame() + 1) + ".mp4"
        os.rename(self.context.nosound_file, suspended_file)
        self.context.nosound_file = suspended_file

        file = open(self.context.workspace + "suspended_session_data.yaml", "a")

        config_file_unparsed = self.context.config_file_unparsed
        config_file_unparsed['resume_settings']['last_saved_frame'] = self.context.controller.get_current_frame() + 1
        config_file_unparsed['resume_settings']['incomplete_video'] = self.context.nosound_file
        config_file_unparsed['resume_settings']['resume_session'] = True

        config_file_unparsed['dandere2x']['developer_settings']['workspace'] = \
            config_file_unparsed['dandere2x']['developer_settings']['workspace'] + \
            str(self.context.controller.get_current_frame() + 1) + os.path.sep

        yaml.dump(config_file_unparsed, file, sort_keys=False)

    def _get_waifu2x_class(self, name: str):
        """ Returns a waifu2x object depending on what the user selected. """

        if name == "caffe":
            return Waifu2xCaffe(self.context)

        elif name == "converter_cpp":
            return Waifu2xConverterCpp(self.context)

        elif name == "vulkan":
            return Waifu2xNCNNVulkan(self.context)

        elif name == "realsr_ncnn_vulkan":
            return RealSRNCNNVulkan(self.context)

        else:
            print("no valid waifu2x selected")
            sys.exit(1)

    def __extract_frames(self):
        """ Extract the initial frames needed for a dandere2x to run depending on session type. """

        if self.context.start_frame != 1:
            self.min_disk_demon.progressive_frame_extractor.extract_frames_to(self.context.start_frame)

        self.min_disk_demon.extract_initial_frames()

    def __upscale_first_frame(self):
        """ The first frame of any dandere2x session needs to be upscaled fully, and this is done as it's own
        process. Ensuring the first frame can get upscaled also provides a source of error checking for the user. """

        # measure the time to upscale a single frame for printing purposes
        one_frame_time = time.time()
        self.waifu2x.upscale_file(
            input_image=self.context.input_frames_dir + "frame" + str(
                self.context.start_frame) + self.context.extension_type,
            output_image=self.context.merged_dir + "merged_" + str(
                self.context.start_frame) + self.context.extension_type)

        if not file_exists(
                self.context.merged_dir + "merged_" + str(self.context.start_frame) + self.context.extension_type):
            """ Ensure the first file was able to get upscaled. We literally cannot continue if it doesn't. """

            print("Could not upscale first file.. check logs file to see what's wrong")
            raise Exception("Could not upscale first file.. check logs file to see what's wrong")

        print("\n Time to upscale an uncompressed frame: " + str(round(time.time() - one_frame_time, 2)))
