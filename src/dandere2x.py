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
import shutil

from context import Context
from dandere2xlib.core.merge import Merge
from dandere2xlib.core.residual import Residual
from dandere2xlib.mindiskusage import MinDiskUsage
from dandere2xlib.status import Status
from wrappers.dandere2x_cpp import Dandere2xCppWrapper
from wrappers.ffmpeg.ffmpeg import re_encode_video, migrate_tracks
from dandere2xlib.utils.dandere2x_utils import show_exception_and_exit, file_exists, wait_on_file, create_directories

import threading
import time
import sys

from wrappers.waifu2x.waifu2x_caffe import Waifu2xCaffe
from wrappers.waifu2x.waifu2x_converter_cpp import Waifu2xConverterCpp
from wrappers.waifu2x.waifu2x_vulkan import Waifu2xVulkan
from wrappers.waifu2x.waifu2x_vulkan_legacy import Waifu2xVulkanLegacy


class Dandere2x(threading.Thread):

    def __init__(self, context: Context):
        self.context = context

        import sys
        sys.excepthook = show_exception_and_exit  # set a custom except hook to prevent window from closing.

    def pre_processing(self):

        self.first_frame = 1
        self._force_delete_workspace()
        self.context.load_video_settings()
        create_directories(self.context.workspace, self.context.directories)
        self._video_pre_processing()

        self.min_disk_demon = MinDiskUsage(self.context)
        self.status_thread = Status(self.context)
        self.dandere2x_cpp_thread = Dandere2xCppWrapper(self.context)
        self.waifu2x = self._get_waifu2x_class(self.context.waifu2x_type)
        self.residual_thread = Residual(self.context)
        self.merge_thread = Merge(self.context)

        self.__extract_frames()
        self.__upscale_first_frame()


    def start(self):

        self.pre_processing()

        self.min_disk_demon.start()
        self.dandere2x_cpp_thread.start()
        self.merge_thread.start()
        self.residual_thread.start()
        self.waifu2x.start()
        self.status_thread.start()

        wait_on_file(self.context.nosound_file)
        self.residual_thread.join()

        if self.context.use_min_disk:
            self.min_disk_demon.join()

        self.merge_thread.join()
        self.waifu2x.join()
        self.dandere2x_cpp_thread.join()
        self.status_thread.join()


    def rmtree_custom(self, top):
        import os
        import stat
        for root, dirs, files in os.walk(top, topdown=False):
            for name in files:
                filename = os.path.join(root, name)
                os.chmod(filename, stat.S_IWUSR)
                os.remove(filename)
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(top)

    def _force_delete_workspace(self):

        if os.path.isdir(self.context.workspace):
            try:
                os.system('rmdir /S /Q "{}"'.format(self.context.workspace))
                #self.rmtree_custom(self.context.workspace)
            except PermissionError:
                print("Trying to delete workspace with rmtree threw PermissionError - Dandere2x may not work.")
                print("Continuing along...")

            while file_exists(self.context.workspace):
                time.sleep(1)

    def _get_waifu2x_class(self, name: str):
        """
        Returns a waifu2x object depending on what the user selected
        """

        if name == "caffe":
            return Waifu2xCaffe(self.context)

        elif name == "converter_cpp":
            return Waifu2xConverterCpp(self.context)

        elif name == "vulkan":
            return Waifu2xVulkan(self.context)

        elif name == "vulkan_legacy":
            return Waifu2xVulkanLegacy(self.context)

        else:
            print("no valid waifu2x selected")
            sys.exit(1)

    def __extract_frames(self):
        """Extract the initial frames needed for a dandere2x to run depending on session type."""

        if self.context.use_min_disk:
            self.min_disk_demon.extract_initial_frames()

    def _video_pre_processing(self):
        """
        Re-encode the user input video (if applicable).
        :return:
        """
        workspace = self.context.workspace
        input_file = self.context.input_file
        unmigrated = workspace + "d2x_input_video_nonmigrated.mkv"
        pre_processed_video = self.context.pre_processed_video

        re_encode_video(self.context, input_file, unmigrated, throw_exception=True)
        migrate_tracks(self.context, unmigrated, input_file, pre_processed_video, copy_if_failed=True)
        os.remove(unmigrated)

    def __upscale_first_frame(self):
        """The first frame of any dandere2x session needs to be upscaled fully, and this is done as it's own
        process. Ensuring the first frame can get upscaled also provides a source of error checking for the user."""

        # measure the time to upscale a single frame for printing purposes
        one_frame_time = time.time()
        self.waifu2x.upscale_file(
            input_file=self.context.input_frames_dir + "frame" + str(self.first_frame) + self.context.extension_type,
            output_file=self.context.merged_dir + "merged_" + str(self.first_frame) + self.context.extension_type)

        if not file_exists(self.context.merged_dir + "merged_" + str(self.first_frame) + self.context.extension_type):
            """ 
            Ensure the first file was able to get upscaled. We literally cannot continue if it doesn't.
            """

            print("Could not upscale first file.. check logs file to see what's wrong")

            sys.exit(1)

        print("\n Time to upscale an uncompressed frame: " + str(round(time.time() - one_frame_time, 2)))
