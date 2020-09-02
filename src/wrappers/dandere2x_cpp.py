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
Purpose: Simply put, very expensive computations for Dandere2x are
====================================================================="""
import logging
import subprocess
import threading

from context import Context
from dandere2xlib.utils.thread_utils import CancellationToken


class Dandere2xCppWrapper(threading.Thread):
    """
    A wrapper for the dandere2x_cpp module. It simply calls the module using information used from the context.
    """

    def __init__(self, context: Context):
        # load stuff from context
        self.context = context
        self.workspace = context.workspace
        self.dandere2x_cpp_dir = context.dandere2x_cpp_dir
        self.frame_count = context.frame_count
        self.block_size = context.block_size
        self.step_size = context.step_size
        self.extension_type = context.extension_type
        self.residual_images_dir = context.residual_images_dir
        self.log_dir = context.console_output_dir
        self.dandere2x_cpp_subprocess = None
        self.start_frame = self.context.start_frame
        self.log = logging.getLogger()

        self.exec_command = [self.dandere2x_cpp_dir,
                             self.workspace,
                             str(self.frame_count),
                             str(self.block_size),
                             str(self.step_size),
                             "r",
                             str(self.start_frame),
                             self.extension_type]

        # Threading Specific

        self.alive = True
        self.cancel_token = CancellationToken()
        self._stopevent = threading.Event()
        threading.Thread.__init__(self, name="Dandere2xCpp")

    def join(self, timeout=None):
        self.log.info("Thread joined")
        threading.Thread.join(self, timeout)

    def kill(self):
        self.log.info("Killing thread")
        self.dandere2x_cpp_subprocess.kill()

    def set_start_frame(self, start_frame):
        self.exec_command = [self.dandere2x_cpp_dir,
                             self.workspace,
                             str(self.frame_count),
                             str(self.block_size),
                             str(self.step_size),
                             "r",
                             str(start_frame),
                             self.extension_type]

    def run(self):
        logger = logging.getLogger(__name__)
        logger.info(self.exec_command)

        console_output = open(self.log_dir + "dandere2x_cpp.txt", "w")
        console_output.write(str(self.exec_command))
        self.dandere2x_cpp_subprocess = subprocess.Popen(self.exec_command, shell=False, stderr=console_output,
                                                             stdout=console_output)

        self.dandere2x_cpp_subprocess.wait()

        if self.dandere2x_cpp_subprocess.returncode == 0:
            logger.info("D2xcpp finished correctly.")
        elif self.dandere2x_cpp_subprocess.returncode != 0 and self.context.controller.is_alive():
            logger.error("D2xcpp ended unexpectedly.")
            logger.error("Dandere2x will suspend the current session.")
            self.context.controller.kill()
