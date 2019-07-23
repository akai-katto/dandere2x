#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: Dandere2X waifu2x-caffe
Author: CardinalPanda
Date Created: March 22, 2019
Last Modified: April 2, 2019
"""
import copy
import logging
import os
import subprocess
import threading

from context import Context
from dandere2x_core.dandere2x_utils import get_lexicon_value
from dandere2x_core.dandere2x_utils import get_options_from_section

# temporary implementation of waifu2x-caffe wrapper
# note to self - add listener to delete files in real time(maybe?) for resume.
# Not sure if Video2x wants that as a feature, though.

# workspace, frame_count, waifu2x_caffe_dir, model_dir, output_dir, upscaled_dir, p_setting,
#                  noise_level, scale_factor

class Waifu2xCaffe(threading.Thread):
    def __init__(self, context: Context):
        self.frame_count = context.frame_count
        self.waifu2x_caffe_cui_dir = context.waifu2x_caffe_cui_dir
        self.differences_dir = context.differences_dir
        self.upscaled_dir = context.upscaled_dir
        self.noise_level = context.noise_level
        self.scale_factor = context.scale_factor
        self.workspace = context.workspace
        self.context = context

        # Create Caffe Command
        self.waifu2x_caffe_upscale_frame = [self.waifu2x_caffe_cui_dir,
                                            "-i", "[input_file]",
                                            "-n", str(self.noise_level),
                                            "-s", str(self.scale_factor)]

        waifu2x_caffe_options = get_options_from_section(context.config_json["waifu2x_caffe"]["output_options"])

        for element in waifu2x_caffe_options:
            self.waifu2x_caffe_upscale_frame.append(element)

        self.waifu2x_caffe_upscale_frame.extend(["-o", "[output_file]"])


        threading.Thread.__init__(self)
        logging.basicConfig(filename=self.workspace + 'waifu2x.log', level=logging.INFO)

    def upscale_file(self, input_file: str, output_file: str):

        exec = copy.copy(self.waifu2x_caffe_upscale_frame)

        # replace the exec command withthe files we're concerned with
        for x in range(len(exec)):
            if exec[x] == "[input_file]":
                exec[x] = input_file

            if exec[x] == "[output_file]":
                exec[x] = output_file

        subprocess.run(exec)

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

        differences_dir = self.context.differences_dir
        upscaled_dir = self.context.upscaled_dir
        exec = copy.copy(self.waifu2x_caffe_upscale_frame)

        # replace the exec command withthe files we're concerned with
        for x in range(len(exec)):
            if exec[x] == "[input_file]":
                exec[x] = differences_dir

            if exec[x] == "[output_file]":
                exec[x] = upscaled_dir


        # make a list of names that will eventually (past or future) be upscaled
        names = []
        for x in range(1, self.frame_count):
            names.append("output_" + get_lexicon_value(6, x) + ".png")

        count_removed = 0

        # remove from the list images that have already been upscaled
        for item in names[::-1]:
            if os.path.isfile(self.upscaled_dir + item):
                names.remove(item)
                count_removed += 1

        if count_removed:
            logger.info("Already have " + str(count_removed) + " upscaled")

        # while there are pictures that have yet to be upscaled, keep calling the upscale command
        while names:
            logger.info("Frames remaining before batch: ")
            logger.info(len(names))
            subprocess.run(exec, stdout=open(os.devnull, 'wb'))
            for item in names[::-1]:
                if os.path.isfile(self.upscaled_dir + item):
                    os.remove(self.differences_dir + item)
                    names.remove(item)
