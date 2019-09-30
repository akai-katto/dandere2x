import copy
import logging
import os
import subprocess
import threading
import time

from context import Context
from dandere2xlib.utils.dandere2x_utils import file_exists, get_lexicon_value, rename_file, wait_on_either_file
from dandere2xlib.utils.yaml_utils import get_options_from_section


class Waifu2xVulkan(threading.Thread):
    """
    The waifu2x-vulkan wrapper, with custom functions written that are specific for dandere2x to work.
    """

    def __init__(self, context: Context):
        # load context
        self.frame_count = context.frame_count
        self.waifu2x_ncnn_vulkan_file_path = context.waifu2x_ncnn_vulkan_legacy_file_name
        self.waifu2x_ncnn_vulkan_path = context.waifu2x_ncnn_vulkan_path
        self.residual_images_dir = context.residual_images_dir
        self.residual_upscaled_dir = context.residual_upscaled_dir
        self.noise_level = context.noise_level
        self.scale_factor = context.scale_factor
        self.workspace = context.workspace
        self.context = context
        self.signal_upscale = True

        self.waifu2x_vulkan_upscale_frame = [self.waifu2x_ncnn_vulkan_file_path,
                                             "-i", "[input_file]",
                                             "-n", str(self.noise_level),
                                             "-s", str(self.scale_factor)]

        waifu2x_vulkan_options = get_options_from_section(
            self.context.config_yaml["waifu2x_ncnn_vulkan"]["output_options"])

        # add custom options to waifu2x_vulkan
        for element in waifu2x_vulkan_options:
            self.waifu2x_vulkan_upscale_frame.append(element)

        self.waifu2x_vulkan_upscale_frame.extend(["-o", "[output_file]"])

        threading.Thread.__init__(self)
        logging.basicConfig(filename=self.workspace + 'waifu2x.log', level=logging.INFO)

    def run(self):
        """
        Input:
            - Files made by residuals.py appearing in the /residual_images/ folder.

        Output:
            - Files upscaled in /residual_upscaled/

        Code Description:

        The current Dandere2x implementation requires files to be removed from the 'residual_images' folder
        during runtime. When waifu2x-ncnn-vulkan calls 'upscale folder', it will only upscale what's in the folder
        at that moment, and it'll re-upscale the images that it already upscaled in a previous iteration.

        Considering that residual_images produced by Dandere2x don't all exist during the initial
        Waifu2x call, we need to call the 'upscale folder' command multiple times. To prevent waifu2x from re-upscaling
        the same image twice, various work arounds are in place to allow Dandere2x and Waifu2x to work in real time.

        Briefly, 1) Create a list of names that will be upscaled by waifu2x,
                 2) Call waifu2x to upscale whatever images are in 'differences' folder
                 3) After waifu2x call is finished, delete whatever files were upscaled, and remove those names from list.
                   (this is to prevent Waifu2x from re-upscaling the same image again)
                 4) Repeat this process until all the names are removed.
        """

        logger = logging.getLogger(__name__)

        residual_images_dir = self.context.residual_images_dir
        residual_upscaled_dir = self.context.residual_upscaled_dir
        exec_command = copy.copy(self.waifu2x_vulkan_upscale_frame)

        console_output = open(self.context.log_dir + "vulkan_upscale_frames.txt", "w")

        # replace the exec command with the files we're concerned with
        for x in range(len(exec_command)):
            if exec_command[x] == "[input_file]":
                exec_command[x] = residual_images_dir

            if exec_command[x] == "[output_file]":
                exec_command[x] = residual_upscaled_dir

        # we need to os.chdir to set the directory or else waifu2x-vulkan won't work.
        os.chdir(self.waifu2x_ncnn_vulkan_path)

        logger.info("waifu2x_vulkan session")
        logger.info(exec_command)

        fix_names_forever_thread = threading.Thread(target=self.__fix_names_all)
        fix_names_forever_thread.start()

        remove_when_upscaled_thread = threading.Thread(target=self.__remove_once_upscaled_then_stop)
        remove_when_upscaled_thread.start()

        # while there are pictures that have yet to be upscaled, keep calling the upscale command
        while self.signal_upscale:
            console_output.write(str(exec_command))
            subprocess.call(exec_command, shell=False, stderr=console_output, stdout=console_output)

        console_output.close()


    def upscale_file(self, input_file: str, output_file: str):
        """
        Manually upscale a file using the wrapper.
        """

        # load context
        waifu2x_ncnn_vulkan_path = self.context.waifu2x_ncnn_vulkan_path
        exec_command = copy.copy(self.waifu2x_vulkan_upscale_frame)

        # replace the exec command with the files we're concerned with
        for x in range(len(exec_command)):
            if exec_command[x] == "[input_file]":
                exec_command[x] = input_file

            if exec_command[x] == "[output_file]":
                exec_command[x] = output_file

        # waifu2x-ncnn-vulkan requires the directory to be local when running, so use os.chir to work out of that dir.
        os.chdir(waifu2x_ncnn_vulkan_path)

        console_output = open(self.context.log_dir + "vulkan_upscale_frame.txt", "w")
        console_output.write(str(exec_command))
        subprocess.call(exec_command, shell=False, stderr=console_output, stdout=console_output)
        console_output.close()

    def __remove_once_upscaled_then_stop(self):
        self.__remove_once_upscaled()
        self.signal_upscale = False

    def __remove_once_upscaled(self):

        # make a list of names that will eventually (past or future) be upscaled
        list_of_names = []
        for x in range(1, self.frame_count):
            list_of_names.append("output_" + get_lexicon_value(6, x) + ".png")

        for x in range(len(list_of_names)):

            name = list_of_names[x]

            residual_file = self.residual_images_dir + name.replace(".png", ".jpg")
            residual_upscaled_file = self.residual_upscaled_dir + name

            while not file_exists(residual_upscaled_file):
                time.sleep(.00001)

            if os.path.exists(residual_file):
                os.remove(residual_file)
            else:
                pass

    def __fix_names_all(self):
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
        for x in range(1, self.frame_count):
            file_names.append("output_" + get_lexicon_value(6, x))

        for file in file_names:
            dirty_name = self.residual_upscaled_dir + file + ".jpg.png"
            clean_name = self.residual_upscaled_dir + file + ".png"

            wait_on_either_file(clean_name, dirty_name)

            if file_exists(clean_name):
                pass

            elif file_exists(dirty_name):
                while file_exists(dirty_name):
                    try:
                        rename_file(dirty_name, clean_name)
                    except PermissionError:
                        pass
