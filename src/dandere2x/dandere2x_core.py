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
Purpose: The 'dandere2x thread' for dandere2x, which is largely a 
         controller for starting and ending all the sub-threads dandere2x
         uses during it's runtime. 
         
         If you're looking to understand how dandere2x works, this is
         the starting point.
====================================================================="""
import logging
import os
import sys
import threading
import time

import colorlog
from colorlog import ColoredFormatter

from dandere2x.context import Context
from dandere2xlib.core.merge import Merge
from dandere2xlib.core.residual import Residual
from dandere2xlib.mindiskusage import MinDiskUsage
from dandere2xlib.status import Status
from dandere2xlib.utils.dandere2x_utils import show_exception_and_exit, file_exists, rename_file, force_delete_directory
from wrappers.dandere2x_cpp import Dandere2xCppWrapper
from wrappers.ffmpeg.ffmpeg import migrate_tracks, concat_two_videos
from wrappers.waifu2x.realsr_ncnn_vulkan import RealSRNCNNVulkan
from wrappers.waifu2x.waifu2x_caffe import Waifu2xCaffe
from wrappers.waifu2x.waifu2x_converter_cpp import Waifu2xConverterCpp
from wrappers.waifu2x.waifu2x_ncnn_vulkan import Waifu2xNCNNVulkan


class Dandere2xCore(threading.Thread):

    def __init__(self, context: Context):
        # Administrative Stuff
        import sys
        sys.excepthook = show_exception_and_exit  # set a custom except hook to prevent window from closing.
        threading.Thread.__init__(self, name="Dandere2x Thread")
        self.color_log_format = "%(log_color)s%(asctime)-8s%(reset)s %(log_color)s%(levelname)-8s%(reset)s %(log_color)s%(filename)-8s%(reset)s %(log_color)s%(funcName)-8s%(reset)s: %(log_color)s%(message)s"
        self.file_log_format = "%(asctime)s %(levelname)s %(filename)s %(funcName)s %(message)s"
        self.set_console_logger()
        self.fh = None  # File Handler for log

        # Class Specific
        self.context = context
        self.alive = False
        self.log = logging.getLogger()

        # Class Specific Future Declarations
        """ 
        These are re-set later, but due to lack of python member-variable declarations, they're initially set here so the IDE can 
        do autocomplete corrections / predictions. It's important they're correctly re-assigned when self.run() is called. 
        """
        self.min_disk_demon = MinDiskUsage(self.context)
        self.status_thread = Status(self.context)
        self.dandere2x_cpp_thread = Dandere2xCppWrapper(self.context)
        self.waifu2x = self._get_waifu2x_class(self.context.waifu2x_type)
        self.residual_thread = Residual(self.context)
        self.merge_thread = Merge(self.context)

    def run(self):
        self.log.info("Thread Started")

        # Assigning classes now that context is properly set.
        self.min_disk_demon = MinDiskUsage(self.context)
        self.status_thread = Status(self.context)
        self.dandere2x_cpp_thread = Dandere2xCppWrapper(self.context)
        self.waifu2x = self._get_waifu2x_class(self.context.waifu2x_type)
        self.residual_thread = Residual(self.context)
        self.merge_thread = Merge(self.context)

        self.log.info("Dandere2x Threads Set.. going live with the following context file.")
        self.context.log_all_variables()

        self.__extract_frames()
        self.__upscale_first_frame()

        self.min_disk_demon.start()
        self.dandere2x_cpp_thread.start()
        self.merge_thread.start()
        self.residual_thread.start()
        self.waifu2x.start()
        self.status_thread.start()


    def kill(self):
        """
        Kill Dandere2x entirely. Everything started as a thread within the scope of dandere2x_core.py can be killed with
        controller.kill() except for d2x_cpp, since that runs as a subprocess.

        As an analogy, imagine `controller` is a fishline that is passed to all threads, and we can `pull the cord` on
        all the threads back at once, eliminating the need to chase after all N threads.
        """
        self.log.warning("Dandere2x Killed - Standby")
        self.dandere2x_cpp_thread.kill()
        self.context.controller.kill()

    def join(self, timeout=None):
        self.log.info("Joined called.")

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

        self.log.info("Join finished.")

    def _successful_completion(self):
        """
        This is called when Dandere2x 'finishes' successfully, and the finishing conditions (such as making sure
        subtitles get migrated, merging videos (if necessary), and deleting the workspace.
        """
        self.log.info("It seems Dandere2x has finished successfully. Starting the final steps to complete your video.")

        if self.context.resume_session:
            """
            In the event if Dandere2x is resuming a session, it'll need to merge `incomplete_video` (see yaml) with
            the current session's video, in order to make a complete video. 
            """

            self.log.info("This session is a resume session. Dandere2x will need to merge the two videos. ")
            file_to_be_concat = self.context.workspace + "file_to_be_concat.mp4"

            rename_file(self.context.nosound_file, file_to_be_concat)
            concat_two_videos(self.context, self.context.incomplete_video, file_to_be_concat, self.context.nosound_file)
            self.log.info("Merging the two videos is done. ")

        migrate_tracks(self.context, self.context.nosound_file, self.context.sound_file, self.context.output_file)
        """
        At this point, dandere2x is "done" with the video, and all there is left is to clean up the files we used
        during runtime.
        """

        # Close the file handler for log (since it's going to get deleted).
        self.log.info("Release log file... ")
        self.fh.close()
        self.log.removeHandler(self.fh)
        del self.fh

        if self.context.delete_workspace_after:
            self.log.info("Dandere2x will now delete the workspace it used.")
            force_delete_directory(self.context.workspace)

    def _kill_conditions(self):
        """ Begin a series of kill conditions that will prepare dandere2x to resume the session once suspended.
        For the most part, this involves documenting all the variables needed for dandere2x to know where the last
        session left off at. """
        import yaml

        self.log.warning("Starting Kill Conditions...")
        self.log.warning("Dandere2x is saving the meta-data needed to resume this session later.")

        suspended_file = self.context.workspace + str(self.context.controller.get_current_frame() + 1) + ".mp4"
        os.rename(self.context.nosound_file, suspended_file)
        self.context.nosound_file = suspended_file

        saved_session = self.context.workspace + "suspended_session_data.yaml"
        file = open(saved_session, "a")

        config_file_unparsed = self.context.config_file_unparsed
        config_file_unparsed['resume_settings']['last_saved_frame'] = self.context.controller.get_current_frame() + 1
        config_file_unparsed['resume_settings']['incomplete_video'] = self.context.nosound_file
        config_file_unparsed['resume_settings']['resume_session'] = True

        config_file_unparsed['dandere2x']['developer_settings']['workspace'] = \
            config_file_unparsed['dandere2x']['developer_settings']['workspace'] + \
            str(self.context.controller.get_current_frame() + 1) + os.path.sep

        yaml.dump(config_file_unparsed, file, sort_keys=False)

        self.log.warning("The current metadata for this session is saved in %s." % saved_session)

    # todo, remove this dependency.
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
            self.log.info("This is a resume session, extracting frames to where you left off.")
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
            self.log.error("Could not upscale first file. Dandere2x CANNOT continue.")
            self.log.error("Have you tried making sure your waifu2x works?")

            raise Exception("Could not upscale first file.. check logs file to see what's wrong")

        self.log.info("Time to upscale a single frame: %s " % str(round(time.time() - one_frame_time, 2)))

    def set_file_logger(self, file: str):
        self.log.info("Writing log-file at %s" % file)
        formatter = logging.Formatter(self.file_log_format)
        self.fh = logging.FileHandler(file, "w", "utf-8")
        self.fh.setFormatter(formatter)
        self.log.addHandler(self.fh)
        self.log.info("Log-file set.")

    def set_console_logger(self):
        """
        Create the logging class to be format print statements the dandere2x way.

        The formatted output resembles the following (roughly):
            2020-08-01 16:03:39,455 INFO     dandere2x_core.py : Hewwooo
            2020-08-01 16:03:39,456 WARNING  dandere2x_core.py : jeeez fuck this warning
            2020-08-01 16:03:39,456 ERROR    dandere2x_core.py : oh fuck fuck fuck stop the program an error occurred
        """

        formatter = ColoredFormatter(
            self.color_log_format,
            datefmt=None,
            reset=True,
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            },
            secondary_log_colors={},
            style='%'
        )

        self.handler = colorlog.StreamHandler()
        self.handler.setFormatter(formatter)

        logger = colorlog.getLogger()
        logger.setLevel(logging.INFO)
        logger.addHandler(self.handler)
        logging.info("Dandere2x Console Logger Set")
