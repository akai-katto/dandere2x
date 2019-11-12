#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import logging
import os
import subprocess
import threading

from context import Context
from dandere2xlib.utils.dandere2x_utils import file_exists, get_lexicon_value, wait_on_either_file


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
        self.waifu2x_ncnn_vulkan_legacy_file_name = context.waifu2x_ncnn_vulkan_legacy_file_name
        self.waifu2x_ncnn_vulkan_legacy_path = context.waifu2x_ncnn_vulkan_legacy_path
        self.residual_images_dir = context.residual_images_dir
        self.residual_upscaled_dir = context.residual_upscaled_dir
        self.noise_level = context.noise_level
        self.scale_factor = context.scale_factor
        self.workspace = context.workspace
        self.context = context

        self.waifu2x_vulkan_legacy_upscale_frame = [
            os.path.join(self.waifu2x_ncnn_vulkan_legacy_path,
                         self.waifu2x_ncnn_vulkan_legacy_file_name),
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

        console_output = open(self.context.log_dir + "vulkan_upscale_frame.txt", "w")
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
            wait_on_either_file(differences_dir + "output_" + get_lexicon_value(6, x) + ".jpg",
                                upscaled_dir + "output_" + get_lexicon_value(6, x) + ".png")

            if file_exists(differences_dir + "output_" + get_lexicon_value(6, x) + ".jpg") \
                    and not file_exists(upscaled_dir + "output_" + get_lexicon_value(6, x) + ".png"):
                self.upscale_file(differences_dir + "output_" + get_lexicon_value(6, x) + ".jpg",
                                  upscaled_dir + "output_" + get_lexicon_value(6, x) + ".png")

            elif not file_exists(differences_dir + "output_" + get_lexicon_value(6, x) + ".jpg") \
                    and file_exists(upscaled_dir + "output_" + get_lexicon_value(6, x) + ".png"):
                continue
