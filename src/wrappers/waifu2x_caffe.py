#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: Dandere2X waifu2x-caffe
Author: CardinalPanda
Date Created: March 22, 2019
Last Modified: April 2, 2019
"""
from dandere2x_core.dandere2x_utils import get_lexicon_value
import logging
import os
import subprocess
import threading


# temporary implementation of waifu2x-caffe wrapper
# note to self - add listener to delete files in real time(maybe?) for resume.
# Not sure if Video2x wants that as a feature, though.

class Waifu2xCaffe(threading.Thread):
    def __init__(self, workspace, frame_count, waifu2x_caffe_dir, model_dir, output_dir, upscaled_dir, p_setting,
                 noise_level, scale_factor):

        self.frame_count = frame_count
        self.waifu2x_caffe_dir = waifu2x_caffe_dir
        self.output_dir = output_dir
        self.upscaled_dir = upscaled_dir
        self.p_setting = p_setting
        self.noise_level = noise_level
        self.scale_factor = scale_factor
        self.model_dir = model_dir
        self.workspace = workspace
        threading.Thread.__init__(self)
        logging.basicConfig(filename=self.workspace + 'waifu2x.log', level=logging.INFO)

    @staticmethod
    def upscale_file(workspace, waifu2x_caffe_dir, model_dir, input_file, output, setting, noise_level, scale_factor):
        logger = logging.getLogger(__name__)

        exec = [waifu2x_caffe_dir,
                "-i", input_file,
                "-p", setting,
                "-n", noise_level,
                "-s", scale_factor,
                "-o", output]

        if model_dir != "default":
            exec.append("--model_dir")
            exec.append(model_dir)

        logger.info("manually upscaling file")
        logger.info(exec)
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

        exec = [self.waifu2x_caffe_dir,
                "-i", self.output_dir,
                "-p", self.p_setting,
                "-n", self.noise_level,
                "-s", self.scale_factor,
                "-o", self.upscaled_dir]

        if self.model_dir != "default":
            exec.append("--model_dir")
            exec.append(self.model_dir)

        logger.info("waifu2xcaffe session")
        logger.info(exec)

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
            subprocess.run(exec)
            for item in names[::-1]:
                if os.path.isfile(self.upscaled_dir + item):
                    os.remove(self.output_dir + item)
                    names.remove(item)
