import logging
import os
import sys
import threading
import time
from typing import Type

from dandere2x.dandere2x_service_request import Dandere2xServiceRequest, UpscalingEngineType
from dandere2x.dandere2x_logger import set_dandere2x_logger
from dandere2x.dandere2x_service.core.dandere2x_cpp import Dandere2xCppWrapper
from dandere2x.dandere2x_service.core.merge import Merge
from dandere2x.dandere2x_service.core.min_disk_usage import MinDiskUsage
from dandere2x.dandere2x_service.core.residual import Residual
from dandere2x.dandere2x_service.core.status_thread import Status
from dandere2x.dandere2x_service.core.waifu2x.abstract_upscaler import AbstractUpscaler
from dandere2x.dandere2x_service.core.waifu2x.waifu2x_caffe import Waifu2xCaffe
from dandere2x.dandere2x_service.core.waifu2x.waifu2x_converter_cpp import Waifu2xConverterCpp
from dandere2x.dandere2x_service.core.waifu2x.waifu2x_ncnn_vulkan import Waifu2xNCNNVulkan
from dandere2x.dandere2x_service.core.waifu2x.realsr_ncnn_vulkan import RealSRNCNNVulkan
from dandere2x.dandere2x_service.dandere2x_service_context import Dandere2xServiceContext
from dandere2x.dandere2x_service.dandere2x_service_controller import Dandere2xController
from dandere2x.dandere2xlib.utils.dandere2x_utils import file_exists


def _get_upscale_engine(selected_engine: UpscalingEngineType) -> Type[AbstractUpscaler]:

    if selected_engine == UpscalingEngineType.CONVERTER_CPP:
        return Waifu2xConverterCpp

    if selected_engine == UpscalingEngineType.VULKAN:
        return Waifu2xNCNNVulkan

    if selected_engine == UpscalingEngineType.CAFFE:
        return Waifu2xCaffe
    
    if selected_engine == UpscalingEngineType.REALSR:
        return RealSRNCNNVulkan

    else:
        log.error("no valid waifu2x selected: %s", selected_engine)
        raise Exception


class Dandere2xServiceThread(threading.Thread):

    def __init__(self, service_request: Dandere2xServiceRequest):
        """
        A thread that will produce service_request.output_file's video. This is the lowest-level dandere2x-related
        object, and handles all the core-logic associated with dandere2x.

        This assume's that service_request.workspace is empty, and may throw unexpected behaviour if it is not.
        Args:

            service_request: Dandere2xServiceRequest object.
        """
        super().__init__(name=service_request.name)

        # Set logger format
        set_dandere2x_logger(input_file_path=service_request.input_file)
        self.log = logging.getLogger(name=service_request.input_file)

        # Class Specific
        self.context = Dandere2xServiceContext(service_request)
        self.controller = Dandere2xController()
        self.threads_active = False

        # Child-threads
        self.min_disk_demon = MinDiskUsage(self.context, self.controller)
        self.status_thread = Status(self.context, self.controller)
        self.dandere2x_cpp_thread = Dandere2xCppWrapper(self.context, self.controller)

        selected_waifu2x = _get_upscale_engine(service_request.upscale_engine)
        self.waifu2x = selected_waifu2x(context=self.context, controller=self.controller)

        self.residual_thread = Residual(self.context, self.controller)
        self.merge_thread = Merge(context=self.context, controller=self.controller)

    def run(self):
        """
        Creates a series of child-threads that are used to create an upscaled folder.
        Returns:

        """
        self.log.info("called.")
        self.__create_directories(workspace=self.context.service_request.workspace,
                                  directories_list=self.context.directories)

        self.log.info("Dandere2x Threads Set.. going live with the following context file.")
        self.context.log_all_variables()

        self.min_disk_demon.extract_initial_frames()
        self.__upscale_first_frame()

        self.min_disk_demon.start()
        self.dandere2x_cpp_thread.start()
        self.merge_thread.start()
        self.residual_thread.start()
        self.waifu2x.start()
        self.status_thread.start()

        while self.controller.get_current_frame() < self.context.frame_count - 1:
            time.sleep(1)

        self.min_disk_demon.join()
        self.dandere2x_cpp_thread.join()
        self.merge_thread.join()
        self.residual_thread.join()
        self.waifu2x.join()
        self.status_thread.join()

    # todo, remove this dependency.

    def __upscale_first_frame(self):
        """
        The first frame of any dandere2x session needs to be upscaled fully, and this is done as it's own
        process. Ensuring the first frame can get upscaled also provides a source of error checking for the user.
        """

        # measure the time to upscale a single frame for printing purposes
        one_frame_time = time.time()
        self.waifu2x.upscale_file(
            input_image=self.context.input_frames_dir + "frame" + str(1) + ".png",
            output_image=self.context.merged_dir + "merged_" + str(1) + ".png")

        if not file_exists(
                self.context.merged_dir + "merged_" + str(1) + ".png"):
            """ 
            Ensure the first file was able to get upscaled. We literally cannot continue if it doesn't. 
            """
            self.log.error("Could not upscale first file. Dandere2x CANNOT continue.")
            self.log.error("Have you tried making sure your waifu2x works?")

            raise Exception("Could not upscale first file.. check logs file to see what's wrong")

        self.log.info("Time to upscale a single frame: %s ", str(round(time.time() - one_frame_time, 2)))

    def __create_directories(self, workspace: str, directories_list: list):
        """
        In dandere2x's context file, there's a list of directories.
        """

        self.log.info("Creating directories. Starting with %s first" % workspace)

        if os.path.exists(workspace):
            self.log.error("Workspace '%s' already exists - fatal error. Exiting" % workspace)
            raise Exception

        # need to create workspace first or else subdirectories wont get made correctly
        try:
            os.makedirs(workspace)
        except:
            self.log.warning("Creation of directory %s failed.. dandere2x may still work but be advised. " % workspace)

        for subdirectory in directories_list:
            try:
                os.makedirs(subdirectory)
            except OSError:
                self.log.warning(
                    "Creation of the directory %s failed.. dandere2x may still work but be advised. " % workspace)
            else:
                self.log.info("Successfully created the directory %s " % subdirectory)
