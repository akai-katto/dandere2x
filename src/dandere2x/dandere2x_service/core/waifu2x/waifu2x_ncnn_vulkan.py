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
import os
import subprocess
from threading import Thread

from dandere2x.dandere2x_service.dandere2x_service_context import Dandere2xServiceContext
from dandere2x.dandere2x_service.dandere2x_service_controller import Dandere2xController

from dandere2x.dandere2xlib.utils.dandere2x_utils import rename_file_wait, get_lexicon_value, file_exists, \
    rename_file, wait_on_either_file, get_operating_system
from dandere2x.dandere2xlib.utils.yaml_utils import get_options_from_section, load_executable_paths_yaml
from ..waifu2x.abstract_upscaler import AbstractUpscaler


class Waifu2xNCNNVulkan(AbstractUpscaler, Thread):

    def __init__(self, context: Dandere2xServiceContext, controller: Dandere2xController):
        # implementation specific
        self.active_waifu2x_subprocess = None
        self.waifu2x_vulkan_path = load_executable_paths_yaml()['waifu2x_vulkan']

        assert get_operating_system() != "win32" or os.path.exists(self.waifu2x_vulkan_path), \
            "%s does not exist!" % self.waifu2x_vulkan_path

        super().__init__(context, controller)
        Thread.__init__(self, name="Waifu2x Thread")

    # override
    def run(self, timeout=None) -> None:
        fix_w2x_ncnn_vulkan_names = Thread(target=self.__fix_waifu2x_ncnn_vulkan_names,
                                           name="Waifu2xNCNNVulkan Fix Names")
        fix_w2x_ncnn_vulkan_names.start()
        super().run()

    # override
    def repeated_call(self) -> None:
        exec_command = copy.copy(self.upscale_command)
        console_output = open(self.context.console_output_dir + "vulkan_upscale_frames.txt", "w")

        # replace the exec command with the files we're concerned with
        for x in range(len(exec_command)):
            if exec_command[x] == "[input_file]":
                exec_command[x] = self.context.residual_images_dir

            if exec_command[x] == "[output_file]":
                exec_command[x] = self.context.residual_upscaled_dir

        console_output.write(str(exec_command))
        self.active_waifu2x_subprocess = subprocess.Popen(args=exec_command, shell=False,
                                                          stderr=console_output, stdout=console_output,
                                                          cwd=os.path.dirname(self.waifu2x_vulkan_path))
        self.active_waifu2x_subprocess.wait()

    # override
    def upscale_file(self, input_image: str, output_image: str) -> None:
        exec_command = copy.copy(self.upscale_command)
        console_output_path = self.context.console_output_dir + "vulkan_upscale_frames.txt"

        with open(console_output_path, "w") as console_output:
            """  
            note: 
            so waifu2x-ncnn-vulkan actually doesn't allow jpg outputs. We have to work around this by
            simply renaming it as png here, then changing it to jpg (for consistency elsewhere) 
            """

            output_image = output_image.replace(".jpg", ".png")

            # replace the exec command with the files we're concerned with
            for x in range(len(exec_command)):
                if exec_command[x] == "[input_file]":
                    exec_command[x] = input_image

                if exec_command[x] == "[output_file]":
                    exec_command[x] = output_image

            console_output.write(str(exec_command))
            self.active_waifu2x_subprocess = subprocess.Popen(exec_command,
                                                              shell=False, stderr=console_output, stdout=console_output,
                                                              cwd=os.path.dirname(self.waifu2x_vulkan_path))
            self.active_waifu2x_subprocess.wait()

            if not os.path.exists(output_image):
                self.log.info("Could not upscale first frame: printing %s console log" % __name__)

                with open(console_output_path) as f:
                    for line in f:
                        self.log.critical("%s", str(line))

                raise Exception("Could not upscale file %s" % input_image)

            rename_file_wait(output_image, output_image.replace(".png", ".jpg"))

    # override
    def _construct_upscale_command(self) -> list:
        waifu2x_vulkan_upscale_frame_command = [self.waifu2x_vulkan_path,
                                                "-i", "[input_file]",
                                                "-n", str(self.context.service_request.denoise_level),
                                                "-s", str(self.context.service_request.scale_factor)]

        waifu2x_vulkan_options = get_options_from_section(
            self.context.service_request.output_options["waifu2x_ncnn_vulkan"]["output_options"])

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
        for x in range(1, self.context.frame_count):
            file_names.append("output_" + get_lexicon_value(6, x))

        for file in file_names:
            dirty_name = self.context.residual_upscaled_dir + file + ".jpg.png"
            clean_name = self.context.residual_upscaled_dir + file + ".png"

            wait_on_either_file(clean_name, dirty_name)

            if file_exists(clean_name):
                pass

            elif file_exists(dirty_name):
                while file_exists(dirty_name):
                    try:
                        rename_file(dirty_name, clean_name)
                    except PermissionError:
                        pass
