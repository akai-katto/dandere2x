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
import copy
import subprocess
import time
from threading import Thread

from context import Context
from dandere2xlib.utils.dandere2x_utils import rename_file_wait, get_lexicon_value, wait_on_either_file, file_exists, \
    rename_file
from dandere2xlib.utils.yaml_utils import get_options_from_section
from ..waifu2x.abstract_upscaler import AbstractUpscaler


class Waifu2xNCNNVulkan(AbstractUpscaler, Thread):

    def __init__(self, context: Context):
        super().__init__(context)

        # load context specific to implementation
        self.frame_count = context.frame_count
        self.waifu2x_ncnn_vulkan_file_path = context.waifu2x_ncnn_vulkan_legacy_file_name
        self.waifu2x_ncnn_vulkan_path = context.waifu2x_ncnn_vulkan_path
        self.residual_images_dir = context.residual_images_dir
        self.residual_upscaled_dir = context.residual_upscaled_dir
        self.noise_level = context.noise_level
        self.scale_factor = context.scale_factor
        self.workspace = context.workspace
        self.start_frame = context.start_frame
        self.context = context

        # implementation specific
        self.active_waifu2x_subprocess = None
        self.waifu2x_vulkan_upscale_frame_command = self._construct_upscale_command()

        fix_w2x_ncnn_vulkan_names = Thread(target=self.__fix_waifu2x_ncnn_vulkan_names,
                                           name="Waifu2xNCNNVulkan Fix Names")
        fix_w2x_ncnn_vulkan_names.start()

    def join(self, timeout=None) -> None:

        while self.controller.is_alive() and not self.check_if_done():
            time.sleep(0.05)

    def repeated_call(self) -> None:
        """ Call the "upscale folder" command. """
        exec_command = copy.copy(self.waifu2x_vulkan_upscale_frame_command)
        console_output = open(self.context.console_output_dir + "vulkan_upscale_frames.txt", "w")

        # replace the exec command with the files we're concerned with
        for x in range(len(exec_command)):
            if exec_command[x] == "[input_file]":
                exec_command[x] = self.residual_images_dir

            if exec_command[x] == "[output_file]":
                exec_command[x] = self.residual_upscaled_dir

        console_output.write(str(exec_command))
        self.active_waifu2x_subprocess = subprocess.Popen(exec_command, shell=False, stderr=console_output,
                                                          stdout=console_output)
        self.active_waifu2x_subprocess.wait()

    def upscale_file(self, input_image: str, output_image: str) -> None:
        """ Upscale a single file using the implemented upscaling program. """

        exec_command = copy.copy(self.waifu2x_vulkan_upscale_frame_command)
        console_output = open(self.context.console_output_dir + "vulkan_upscale_frames.txt", "w")

        # notes - so waifu2x-ncnn-vulkan actually doesn't allow jpg outputs. We have to work around this by
        #         simply renaming it as png here, then changing it to jpg (for consistency elsewhere)
        output_image = output_image.replace(".jpg", ".png")

        # replace the exec command with the files we're concerned with
        for x in range(len(exec_command)):
            if exec_command[x] == "[input_file]":
                exec_command[x] = input_image

            if exec_command[x] == "[output_file]":
                exec_command[x] = output_image

        console_output.write(str(exec_command))
        self.active_waifu2x_subprocess = subprocess.Popen(exec_command, shell=False, stderr=console_output,
                                                          stdout=console_output)
        self.active_waifu2x_subprocess.wait()

        rename_file_wait(output_image, output_image.replace(".png", ".jpg"))

    # Private Methods

    def _construct_upscale_command(self) -> list:
        """ A generic, recyclable upscale command that can be used for single-file upscaling or batch upscaling. """
        waifu2x_vulkan_upscale_frame_command = [self.waifu2x_ncnn_vulkan_file_path,
                                                "-i", "[input_file]",
                                                "-n", str(self.noise_level),
                                                "-s", str(self.scale_factor)]

        waifu2x_vulkan_options = get_options_from_section(
            self.context.config_yaml["waifu2x_ncnn_vulkan"]["output_options"])

        # add custom options to waifu2x_vulkan
        for element in waifu2x_vulkan_options:
            waifu2x_vulkan_upscale_frame_command.append(element)

        waifu2x_vulkan_upscale_frame_command.extend(["-o", "[output_file]"])
        return waifu2x_vulkan_upscale_frame_command

    def __fix_waifu2x_ncnn_vulkan_names(self):
        """
        Waifu2x-ncnn-vulkan will accept a file as "file.jpg" and output as "file.jpg.png".

        Unfortunately, dandere2x wouldn't recognize this, so this function renames each name to the correct naming
        convention. This function will iteratiate through every file needing to be upscaled waifu2x-ncnn-vulkan,
        and change it's name after it's done saving

        Comments:

        - There's a really complicated try / except that exists because, even though a file may exist,
          the file handle may still be used by waifu2x-ncnn-vulkan (it hasn't released it yet). As a result,
          we need to try / except it until it's released, allowing us to rename it.

        """

        file_names = []
        for x in range(self.start_frame, self.frame_count):
            file_names.append("output_" + get_lexicon_value(6, x))

        for file in file_names:
            dirty_name = self.residual_upscaled_dir + file + ".jpg.png"
            clean_name = self.residual_upscaled_dir + file + ".png"

            # TODO - IMPLEMENT WITH CONTROLLER
            wait_on_either_file(clean_name, dirty_name)

            if not self.controller.is_alive():
                return

            if file_exists(clean_name):
                pass

            elif file_exists(dirty_name):
                while file_exists(dirty_name):
                    try:
                        rename_file(dirty_name, clean_name)
                    except PermissionError:
                        pass
