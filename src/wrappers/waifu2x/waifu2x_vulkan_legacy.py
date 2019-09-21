from dandere2xlib.utils.dandere2x_utils import file_exists, get_lexicon_value, rename_file, wait_on_either_file, wait_on_file
from dandere2xlib.utils.json_utils import get_options_from_section
from context import Context

import subprocess
import threading
import logging
import copy
import os


class Waifu2xVulkanLegacy(threading.Thread):
    """
    A wrapper for the legacy implementation of waifu2x-ncnn-vulkan from the snap package. The main difference with
    this wrapper when compared to the vulkan and caffe wrappers is that the legacy snap package does not offer
    support for upscaling an entire folder, so instead this wrapper needs to upscale each file individually.

    This file isn't maintained too much, as once the snap is updated, this class will be obsolete.
    """
    def __init__(self, context: Context):
        # load context
        self.frame_count = context.frame_count
        self.waifu2x_ncnn_vulkan_legacy_file_path = context.waifu2x_ncnn_vulkan_legacy_file_path
        self.waifu2x_vulkan_legacy_path = context.waifu2x_ncnn_vulkan_legacy_path
        self.differences_dir = context.residual_images_dir
        self.upscaled_dir = context.residual_upscaled_dir
        self.noise_level = context.noise_level
        self.scale_factor = context.scale_factor
        self.workspace = context.workspace
        self.context = context

        self.waifu2x_vulkan_legacy_upscale_frame = [self.waifu2x_ncnn_vulkan_legacy_file_path,
                                             "[input_file]",
                                             "[output_file]",
                                             str(self.noise_level),
                                             str(self.scale_factor),
                                             str(200)]

        threading.Thread.__init__(self)
        logging.basicConfig(filename=self.workspace + 'waifu2x.log', level=logging.INFO)

    def upscale_file(self, input_file: str, output_file: str):
        # load context
        waifu2x_ncnn_vulkan_legacy_path = self.context.waifu2x_ncnn_vulkan_legacy_path
        exec_command = copy.copy(self.waifu2x_vulkan_legacy_upscale_frame)
        logger = logging.getLogger(__name__)

        # replace the exec command withthe files we're concerned with
        for x in range(len(exec_command)):
            if exec_command[x] == "[input_file]":
                exec_command[x] = input_file

            if exec_command[x] == "[output_file]":
                exec_command[x] = output_file

        logger.info("Vulkan Exec")
        logger.info(str(exec_command))

        logger.info("Changind Dirs")
        logger.info(str(waifu2x_ncnn_vulkan_legacy_path))

        os.chdir(waifu2x_ncnn_vulkan_legacy_path)

        logger.info("manually upscaling file")
        logger.info(exec_command)

        console_output = open(self.context.log_dir + "vulkan_legacy_upscale_frame.txt", "w")
        console_output.write(str(exec_command))
        subprocess.call(exec_command, shell=False, stderr=console_output, stdout=console_output)
        console_output.close()

    def run(self):
        """
        Upscale every image that will *eventually* appear in the residuals_dir folder by waifu2x.
        """
        logger = logging.getLogger(__name__)

        differences_dir = self.context.residual_images_dir
        upscaled_dir = self.context.residual_upscaled_dir
        exec = copy.copy(self.waifu2x_vulkan_legacy_upscale_frame)

        for x in range(1, self.frame_count):
            
            # The 2x2 block hack might not work here.
            # Will fix this next time I boot up a Linux machine and erase this comment.

            diff_file = differences_dir + "output_" + get_lexicon_value(6, x) + ".jpg"
            upscaled_file = upscaled_dir +    "output_" + get_lexicon_value(6, x) + ".png"
            
            wait_on_either_file(diff_file, upscaled_file)

            if not os.path.exists(upscaled_file):
                self.upscale_file(diff_file, upscaled_file)


