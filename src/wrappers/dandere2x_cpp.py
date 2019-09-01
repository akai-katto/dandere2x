#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: Dandere2X CPP
Author: CardinalPanda
Date Created: March 22, 2019
Last Modified: April 2, 2019
"""
import logging
import os
import subprocess
import threading

from context import Context
from dandere2xlib.utils.dandere2x_utils import get_lexicon_value


class Dandere2xCppWrapper(threading.Thread):

    def __init__(self, context: Context, resume: bool):
        # load stuff from context
        self.workspace = context.workspace
        self.dandere2x_cpp_dir = context.dandere2x_cpp_dir
        self.frame_count = context.frame_count
        self.block_size = context.block_size
        self.step_size = context.step_size
        self.extension_type = context.extension_type
        self.differences_dir = context.differences_dir

        self.resume = resume
        threading.Thread.__init__(self)

    def run(self):
        if not self.resume:
            self.new_run()

        elif self.resume:
            self.resume_run()

    # start a new dandere2x cpp session
    def new_run(self):
        logger = logging.getLogger(__name__)

        exec = [self.dandere2x_cpp_dir,
                self.workspace,
                str(self.frame_count),
                str(self.block_size),
                str(self.step_size),
                "n",
                str(1),
                self.extension_type]

        logger.info(exec)

        # return_val = subprocess.run(exec, creationflags=subprocess.CREATE_NEW_CONSOLE).returncode
        return_val = subprocess.run(exec).returncode
        # p = subprocess.Popen(exec, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        if return_val == 0:
            logger.info("d2xcpp finished correctly")
        else:
            logger.info("d2xcpp ended unexpectedly")

    # Count how many p_frame_data files exist, then start at that minus 1.
    # Consider including counting how many inversion_data files exist also, but doesn't seem necessary.

    # What we're trying to do is essentially force d2x to create a new key frame at the last found p_frame.
    def resume_run(self):
        logger = logging.getLogger(__name__)
        last_found = int(self.frame_count)

        # count how many vector files that have already been produced by dandere2xcpp
        logger.info("looking for previous frames...")
        while last_found > 0:
            exists = os.path.isfile(
                self.workspace + os.path.sep + "pframe_data" + os.path.sep + "pframe_" + str(last_found) + ".txt")
            if not exists:
                last_found -= 1

            elif exists:
                break

        # Delete the most recent files produced. Not all 3 files may exist (we only know the pframe_data exists)
        # so we do a try. There's cases where inversion data or difference_image didn't save.
        try:
            os.remove(self.workspace + os.path.sep + "pframe_data" + os.path.sep + "pframe_" + str(last_found) + ".txt")
            os.remove(
                self.workspace + os.path.sep + "inversion_data" + os.path.sep + "inversion_" + str(last_found) + ".txt")
            os.remove(self.differences_dir + "output_" + get_lexicon_value(6, last_found) + ".png")

        except FileNotFoundError:
            pass

        # start one lower because we deleted the file(s)
        last_found = last_found - 1
        logger.info("Resuming at p_frame # " + str(last_found))

        # Delete the current files, and resume work from there. We know all 3 of these files exist
        # because we started one lower.
        os.remove(self.workspace + os.path.sep + "pframe_data" + os.path.sep + "pframe_" + str(last_found) + ".txt")
        os.remove(
            self.workspace + os.path.sep + "inversion_data" + os.path.sep + "inversion_" + str(last_found) + ".txt")
        os.remove(self.differences_dir + "output_" + get_lexicon_value(6, last_found) + ".png")

        exec = [self.dandere2x_cpp_dir,
                self.workspace,
                str(self.frame_count),
                str(self.block_size),
                str(self.step_size),
                "r",
                str(last_found),
                self.extension_type]

        logger.info(exec)
        return_val = subprocess.run(exec, creationflags=subprocess.CREATE_NEW_CONSOLE).returncode

        if return_val == 0:
            logger.info("d2xcpp finished correctly")
        else:
            logger.info("d2xcpp ended unexpectedly")
