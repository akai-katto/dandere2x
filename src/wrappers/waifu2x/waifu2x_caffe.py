#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import copy
import logging
import os
import subprocess
import threading

from context import Context
from dandere2xlib.utils.dandere2x_utils import get_lexicon_value
from dandere2xlib.utils.yaml_utils import get_options_from_section


class Waifu2xCaffe(threading.Thread):
    """
    Note: This is legacy at the moment, it may or may still work, but the class isn't up to standards.

    Let me know if you have intentions to use this so I can update it.
    """
    def __init__(self, context: Context):
        self.frame_count = context.frame_count
        self.waifu2x_caffe_cui_dir = context.waifu2x_caffe_cui_dir
        self.residual_images_dir = context.residual_images_dir
        self.residual_upscaled_dir = context.residual_upscaled_dir
        self.noise_level = context.noise_level
        self.scale_factor = context.scale_factor
        self.workspace = context.workspace
        self.context = context

        # Create Caffe Command
        self.waifu2x_caffe_upscale_frame = [self.waifu2x_caffe_cui_dir,
                                            "-i", "[input_file]",
                                            "-n", str(self.noise_level),
                                            "-s", str(self.scale_factor)]

        waifu2x_caffe_options = get_options_from_section(context.config_file["waifu2x_caffe"]["output_options"])

        for element in waifu2x_caffe_options:
            self.waifu2x_caffe_upscale_frame.append(element)

        self.waifu2x_caffe_upscale_frame.extend(["-o", "[output_file]"])

        threading.Thread.__init__(self)
        logging.basicConfig(filename=self.workspace + 'waifu2x.log', level=logging.INFO)

    def upscale_file(self, input_file: str, output_file: str):

        exec_command = copy.copy(self.waifu2x_caffe_upscale_frame)

        # replace the exec command withthe files we're concerned with
        for x in range(len(exec_command)):
            if exec_command[x] == "[input_file]":
                exec_command[x] = input_file

            if exec_command[x] == "[output_file]":
                exec_command[x] = output_file

        print(exec_command)

        console_output = open(self.context.log_dir + "waifu2x_caffe_upscale_frame_single.txt", "w")
        console_output.write(str(exec_command))
        subprocess.call(exec_command, shell=False, stderr=console_output, stdout=console_output)

    # The current Dandere2x implementation requires files to be removed from the folder
    # During runtime. As files produced by Dandere2x don't all exist during the initial
    # Waifu2x call, various work arounds are in place to allow Dandere2x and Waifu2x to work in real time.

    # Briefly, 1) Create a list of names that will be upscaled by waifu2x,
    #          2) Call waifu2x to upscale whatever images are in 'differences' folder
    #          3) After waifu2x call is finished, delete whatever files were upscaled, and remove those names from list.
    #             (this is to prevent Waifu2x from re-upscaling the same image again)
    #          4) Repeat this process until all the names are removed.
    def run(self):
        logger = logging.getLogger(__name__)
        console_output = open(self.context.log_dir + "waifu2x_caffe_upscale_frame_all.txt", "w")

        residual_images_dir = self.context.residual_images_dir
        residual_upscaled_dir = self.context.residual_upscaled_dir
        exec_command = copy.copy(self.waifu2x_caffe_upscale_frame)

        # replace the exec command withthe files we're concerned with
        for x in range(len(exec_command)):
            if exec_command[x] == "[input_file]":
                exec_command[x] = residual_images_dir

            if exec_command[x] == "[output_file]":
                exec_command[x] = residual_upscaled_dir

        # make a list of names that will eventually (past or future) be upscaled
        names = []
        for x in range(1, self.frame_count):
            names.append("output_" + get_lexicon_value(6, x) + ".png")

        count_removed = 0

        # remove from the list images that have already been upscaled
        for name in names[::-1]:
            if os.path.isfile(self.residual_upscaled_dir + name):
                names.remove(name)
                count_removed += 1

        if count_removed:
            logger.info("Already have " + str(count_removed) + " upscaled")

        # while there are pictures that have yet to be upscaled, keep calling the upscale command
        while names:
            logger.info("Frames remaining before batch: ")
            logger.info(len(names))

            console_output.write(str(exec_command))
            subprocess.call(exec_command, shell=True, stderr=console_output, stdout=console_output)

            for name in names[::-1]:
                if os.path.isfile(self.residual_upscaled_dir + name):
                    os.remove(self.residual_images_dir + name.replace(".png", ".jpg"))
                    names.remove(name)
