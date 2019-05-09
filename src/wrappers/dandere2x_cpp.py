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
from dandere2x_core.context import Context

class Dandere2xCppWrapper(threading.Thread):

    def __init__(self, context: Context, resume: bool):
        # load stuff from context
        self.workspace = context.workspace
        self.dandere2x_cpp_dir = context.dandere2x_cpp_dir
        self.frame_count = context.frame_count
        self.block_size = context.block_size
        self.tolerance = context.tolerance
        self.step_size = context.step_size
        self.extension_type = context.extension_type

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
                str(self.tolerance),
                str(self.step_size),
                "n",
                str(1),
                self.extension_type]

        logger.info(exec)
        subprocess.run(exec, creationflags=subprocess.CREATE_NEW_CONSOLE)
        logger.info("finished correctly")

    # Count how many p_frame_data files exist, then start at that minus 1.
    # Consider including counting how many inversion_data files exist also, but
    # Doesn't seem necessary.
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

        # start one lower to overwrite / prevent weirdness
        last_found = last_found - 1
        logger.info("last found is " + str(last_found))

        exec = [self.dandere2x_cpp_dir,
                self.workspace,
                str(self.frame_count),
                str(self.block_size),
                str(self.tolerance),
                str(self.mse_max),
                str(self.mse_min),
                str(self.step_size),
                "r",
                str(last_found),
                self.extension_type]

        logger.info(exec)
        subprocess.run(exec, creationflags=subprocess.CREATE_NEW_CONSOLE)
        logger.info("finished correctly")
