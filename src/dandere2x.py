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
import sys
import threading
import time

from dandere2xlib.core.merge import Merge
from dandere2xlib.core.residual import Residual
from dandere2xlib.frame_compressor import CompressFrames
from dandere2xlib.mindiskusage import MinDiskUsage
from dandere2xlib.status import Status
from dandere2xlib.utils.dandere2x_utils import delete_directories, create_directories, rename_file
from dandere2xlib.utils.dandere2x_utils import valid_input_resolution, file_exists, wait_on_file
from dandere2xlib.utils.thread_utils import CancellationToken
from wrappers.dandere2x_cpp import Dandere2xCppWrapper
from wrappers.ffmpeg.ffmpeg import extract_frames, append_video_resize_filter, concat_two_videos, migrate_tracks
from wrappers.waifu2x.waifu2x_caffe import Waifu2xCaffe
from wrappers.waifu2x.waifu2x_converter_cpp import Waifu2xConverterCpp
from wrappers.waifu2x.waifu2x_vulkan import Waifu2xVulkan
from wrappers.waifu2x.waifu2x_vulkan_legacy import Waifu2xVulkanLegacy


class Dandere2x(threading.Thread):
    """
    The main driver that can be called in a various level of circumstances - for example, dandere2x can be started
    from dandere2x_gui_wrapper.py, raw_config_driver.py, or raw_config_gui_driver.py. In each scenario, this is the
    class that is called when Dandere2x ultimately needs to start.
    """

    def __init__(self, context):
        self.context = context
        self.min_disk_demon = None
        self.merge_thread = Merge(self.context)
        self.residual_thread = Residual(self.context)
        self.waifu2x = self._get_waifu2x_class(self.context.waifu2x_type)
        self.compress_frames_thread = CompressFrames(self.context)
        self.dandere2x_cpp_thread = Dandere2xCppWrapper(self.context)
        self.status_thread = Status(context)

        # session specific
        self.resume_session = False
        self.first_frame = 1

        if self.context.config_yaml['resume_settings']['resume_session']:
            print("is resume session")
            self.resume_session = True
            self.first_frame = int(self.context.config_yaml['resume_settings']['signal_merged_count'])
        else:
            print("is not resume session")

        # Threading Specific

        self.alive = True
        self.cancel_token = CancellationToken()
        self._stopevent = threading.Event()
        threading.Thread.__init__(self, name="dandere2x_thread")

    def __extract_frames(self):
        """Extract the initial frames needed for a dandere2x to run depending on session type."""

        if self.context.use_min_disk:
            if self.resume_session:
                self.min_disk_demon.progressive_frame_extractor.extract_frames_to(
                    int(self.context.config_yaml['resume_settings']['signal_merged_count']))

            self.min_disk_demon.extract_initial_frames()
        elif not self.context.use_min_disk:
            extract_frames(self.context, self.context.input_file)

    def __setup_jobs(self):
        """This method is somewhat deprecated, will be moved somewhere else in the future."""
        if self.context.use_min_disk:
            self.min_disk_demon = MinDiskUsage(self.context)

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
            logging.info("Could not upscale first file.. check logs file to see what's wrong")
            logging.info("Exiting Dandere2x...")
            sys.exit(1)

        print("\n Time to upscale an uncompressed frame: " + str(round(time.time() - one_frame_time, 2)))

    def join(self, timeout=None):

        start = time.time() # for printing out total runtime

        logging.info("dandere2x joined called")

        # due to a weird quirk, prevent dandere2x from being joined until nosound.mkv exists (at least).
        wait_on_file(self.context.nosound_file)

        logging.info("joining residual")
        self.residual_thread.join()

        if self.context.use_min_disk:
            logging.info("joining min disk demon")
            self.min_disk_demon.join()

        logging.info("joining merge")
        self.merge_thread.join()
        logging.info("joining waifu2x")
        self.waifu2x.join()
        logging.info("joining dandere2x")
        self.dandere2x_cpp_thread.join()
        logging.info("joining status")
        self.status_thread.join()
        logging.info("joining compress")
        self.compress_frames_thread.join()

        self.context.logger.info("All threaded processes have finished")
        print("All threaded processes have been finished")

        if self.resume_session:
            print("Session is a resume session, concatenating two videos")
            logging.info("Session is a resume session, concatenating two videos")
            file_to_be_concat = self.context.workspace + "file_to_be_concat.mp4"

            rename_file(self.context.nosound_file, file_to_be_concat)
            concat_two_videos(self.context, self.context.config_yaml['resume_settings']['nosound_file'],
                              file_to_be_concat,
                              self.context.nosound_file)

        # if this became a suspended dandere2x session, kill it.
        if not self.alive:
            logging.info("Invoking suspend exit conditions")
            self.__suspend_exit_conditions()

        elif self.alive:
            logging.info("Migrating tracks")
            migrate_tracks(self.context, self.context.nosound_file,
                           self.context.sound_file, self.context.output_file)

        print("Total runtime : ", time.time() - start)

    def __suspend_exit_conditions(self):
        """This is called when dandere2x session is suspended midway through completition, need to save
        meta data and needed files to be resumable."""

        suspended_file = self.context.workspace + str(self.context.signal_merged_count + 1) + ".mp4"
        os.rename(self.context.nosound_file, suspended_file)
        self.context.nosound_file = suspended_file
        self.__leave_killed_message()

    def __leave_killed_message(self):
        """
        write the yaml file for the next resume session. The next dandere2x will resume in the same folder
        where the previous one left off, but at at \last_upscaled_frame\ (\30\).
        :return:
        """
        import yaml
        file = open(self.context.workspace + "suspended_session_data.yaml", "a")

        config_file_unparsed = self.context.config_file_unparsed
        config_file_unparsed['resume_settings']['signal_merged_count'] = self.context.signal_merged_count
        config_file_unparsed['resume_settings']['nosound_file'] = self.context.nosound_file
        config_file_unparsed['resume_settings']['resume_session'] = True

        config_file_unparsed['dandere2x']['developer_settings']['workspace'] = \
            config_file_unparsed['dandere2x']['developer_settings']['workspace'] + \
            str(self.context.signal_merged_count + 1) + os.path.sep

        yaml.dump(config_file_unparsed, file, sort_keys=False)

    def kill(self):
        self.alive = False
        self.cancel_token.cancel()
        self._stopevent.set()

        self.merge_thread.kill()
        self.waifu2x.kill()
        self.residual_thread.kill()
        self.compress_frames_thread.kill()

        if self.context.use_min_disk:
            self.min_disk_demon.kill()
        self.dandere2x_cpp_thread.kill()
        self.status_thread.kill()

    def __set_first_frame(self):
        """
        Set the first frame for the relevent dandere2x threads when doing a resume session
        """
        self.compress_frames_thread.set_start_frame(self.first_frame)
        self.dandere2x_cpp_thread.set_start_frame(self.first_frame)
        self.merge_thread.set_start_frame(self.first_frame)
        self.residual_thread.set_start_frame(self.first_frame)
        self.waifu2x.set_start_frame(self.first_frame)
        self.status_thread.set_start_frame(self.first_frame)

        if self.context.use_min_disk:
            self.min_disk_demon.set_start_frame(self.first_frame)

    def run(self):
        """
        Starts the dandere2x_python process at large.
        """

        print("threading at start of runtime")
        print(threading.enumerate())

        # directories need to be created before we do anything
        create_directories(self.context.workspace, self.context.directories)

        # dandere2x needs the width and height to be a share a common factor with the block size,
        # so append a video filter if needed to make the size conform
        if not valid_input_resolution(self.context.width, self.context.height, self.context.block_size):
            append_video_resize_filter(self.context)

        # create the list of threads to use for dandere2x
        self.__setup_jobs()

        if self.resume_session:
            self.__set_first_frame()

        # extract the initial frames needed for execution depending on type (min_disk_usage / non min_disk_usage )
        self.__extract_frames()

        # first frame needs to be upscaled manually before dandere2x process starts.
        self.__upscale_first_frame()

        self.compress_frames_thread.start()
        self.dandere2x_cpp_thread.start()
        self.merge_thread.start()
        self.residual_thread.start()
        self.waifu2x.start()
        self.status_thread.start()

        if self.context.use_min_disk:
            self.min_disk_demon.start()

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
            logging.info("no valid waifu2x selected")
            print("no valid waifu2x selected")
            sys.exit(1)

    def delete_workspace_files(self):
        """
        Delete the files produced by dandere2x (beside logs) if this method is called.
        """
        delete_directories(self.context.directories)
        no_sound = os.path.join(self.context.workspace, "nosound.mkv")

        try:
            os.remove(no_sound)

        except OSError:
            print("Deletion of the file %s failed" % no_sound)
            print(OSError.strerror)
        else:
            print("Successfully deleted the file %s " % no_sound)
