import copy
import logging
import os
import subprocess
import threading
import time

from context import Context
from dandere2xlib.utils.dandere2x_utils import get_lexicon_value, wait_on_either_file, file_exists, rename_file
from dandere2xlib.utils.yaml_utils import get_options_from_section


class Waifu2xConverterCpp(threading.Thread):
    """
    Note: This is legacy at the moment, it may or may still work, but the class isn't up to standards.

    Let me know if you have intentions to use this so I can update it.
    """

    def __init__(self, context: Context):
        # load context
        self.frame_count = context.frame_count
        self.waifu2x_converter_cpp_file_path = context.waifu2x_converter_cpp_file_path
        self.waifu2x_converter_cpp_path = context.waifu2x_converter_cpp_path
        self.residual_images_dir = context.residual_images_dir
        self.residual_upscaled_dir = context.residual_upscaled_dir
        self.noise_level = context.noise_level
        self.scale_factor = context.scale_factor
        self.workspace = context.workspace
        self.context = context
        self.signal_upscale = True

        self.waifu2x_conv_upscale_frame = [self.waifu2x_converter_cpp_file_path,
                                           "-i", "[input_file]",
                                           "--noise-level", str(self.noise_level),
                                           "--scale-ratio", str(self.scale_factor)]

        waifu2x_conv_options = get_options_from_section(self.context.config_yaml["waifu2x_converter"]["output_options"])

        # add custom options to waifu2x_vulkan
        for element in waifu2x_conv_options:
            self.waifu2x_conv_upscale_frame.append(element)

        self.waifu2x_conv_upscale_frame.extend(["-o", "[output_file]"])

        threading.Thread.__init__(self)
        logging.basicConfig(filename=self.workspace + 'waifu2x.log', level=logging.INFO)

    # (description from waifu2x_caffe)
    # The current Dandere2x implementation requires files to be removed from the folder
    # During runtime. As files produced by Dandere2x don't all exist during the initial
    # Waifu2x call, various work arounds are in place to allow Dandere2x and Waifu2x to work in real time.

    # Briefly, 1) Create a list of names that will be upscaled by waifu2x,
    #          2) Call waifu2x to upscale whatever images are in 'differences' folder
    #          3) After waifu2x call is finished, delete whatever files were upscaled, and remove those names from list.
    #             (this is to prevent Waifu2x from re-upscaling the same image again)
    #          4) Repeat this process until all the names are removed.
    def run(self):
        console_output = open(self.context.log_dir + "waifu2x_upscale_frames_command.txt", "w")
        logger = logging.getLogger(__name__)
        # if there are pre-existing files, fix them (this occurs during a resume session)
        self.__fix_names()

        fix_names_forever_thread = threading.Thread(target=self.__fix_names_all)
        fix_names_forever_thread.start()

        # we need to os.chdir or else waifu2x-conveter won't work.
        os.chdir(self.waifu2x_converter_cpp_path)

        exec_command = copy.copy(self.waifu2x_conv_upscale_frame)

        # replace the exec command withthe files we're concerned with
        for x in range(len(exec_command)):
            if exec_command[x] == "[input_file]":
                exec_command[x] = self.residual_images_dir

            if exec_command[x] == "[output_file]":
                exec_command[x] = self.residual_upscaled_dir

        logger.info("waifu2xconv session")
        logger.info(exec_command)

        remove_when_upscaled_thread = threading.Thread(target=self.__remove_once_upscaled_then_stop)
        remove_when_upscaled_thread.start()

        # while there are pictures that have yet to be upscaled, keep calling the upscale command
        while self.signal_upscale:
            console_output.write(str(exec_command))
            subprocess.call(exec_command, shell=False, stderr=console_output, stdout=console_output)

    def upscale_file(self, input_file: str, output_file: str):
        # load context

        waifu2x_conv_dir_dir = self.context.waifu2x_converter_cpp_path
        logger = logging.getLogger(__name__)

        exec = copy.copy(self.waifu2x_conv_upscale_frame)

        # replace the exec command withthe files we're concerned with
        for x in range(len(exec)):
            if exec[x] == "[input_file]":
                exec[x] = input_file

            if exec[x] == "[output_file]":
                exec[x] = output_file

        os.chdir(waifu2x_conv_dir_dir)

        logger.info("manually upscaling file")
        logger.info(exec)

        console_output = open(self.context.log_dir + "waifu2x_conv_upscale_frame_single.txt", "w")
        console_output.write(str(exec))
        subprocess.call(exec, shell=False, stderr=console_output, stdout=console_output)

    # Waifu2x-Converter-Cpp adds this ugly '[NS-L3][x2.000000]' to files, so
    # this function just renames the files so Dandere2x can interpret them correctly.
    def __fix_names(self):

        list_of_names = os.listdir(self.residual_upscaled_dir)
        for name in list_of_names:
            if '[NS-L3][x' + self.scale_factor + '.000000]' in name:
                rename_file(self.residual_upscaled_dir + name,
                            self.residual_upscaled_dir + name.replace('_[NS-L3][x' + self.scale_factor + '.000000]',
                                                                      ''))

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

    # This function is tricky. Essentially we do multiple things in one function
    # Because of 'gotchas'

    # First, we make a list of prefixes. Both the desired file name and the produced file name
    # Will start with the same prefix (i.e all the stuff in file_names).

    # Then, we have to specify what the dirty name will end in. in Conv's it'll have a
    # '_[NS-L' + self.noise_level + '][x' + self.scale_factor + '.000000]' in the name we dont want
    # We then have to do a try / except to try to rename it back to it's clean name, since it may still be
    # being written / used by another program and not safe to edit yet.

    def __fix_names_all(self):

        file_names = []
        for x in range(1, self.frame_count):
            file_names.append("output_" + get_lexicon_value(6, x))

        for file in file_names:
            dirty_name = self.residual_upscaled_dir + file + '_[NS-L' + str(self.noise_level) + '][x' + str(
                self.scale_factor) + '.000000]' + ".png"
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
