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

from dandere2x.dandere2x_service.dandere2x_service_context import Dandere2xServiceContext
from dandere2x.dandere2x_service.dandere2x_service_controller import Dandere2xController
from dandere2x.dandere2xlib.utils.yaml_utils import load_executable_paths_yaml


class Dandere2xCppWrapper(threading.Thread):
    """
    A wrapper for the dandere2x_cpp module. It simply calls the module using information used from the context.
    """

    def __init__(self, context: Dandere2xServiceContext, controller: Dandere2xController):
        threading.Thread.__init__(self, name="Dandere2xCpp")
        self.context = context
        self.controller = controller

        self.dandere2x_cpp_subprocess = None
        self.log = logging.getLogger()

        dandere2x_cpp_dir = load_executable_paths_yaml()['dandere2x_cpp']
        self.exec_command = [dandere2x_cpp_dir,
                             self.context.service_request.workspace,
                             str(self.context.frame_count),
                             str(self.context.service_request.block_size),
                             "exhaustive",
                             "mse",
                             str(self.context.service_request.quality_minimum)]

    def join(self, timeout=None):
        self.log.info("Thread joined")
        threading.Thread.join(self, timeout)

    def run(self):
        logger = logging.getLogger(__name__)
        logger.info(self.exec_command)

        console_output = open(self.context.log_dir + "dandere2x_cpp.txt", "w")
        console_output.write(str(self.exec_command))
        self.dandere2x_cpp_subprocess = subprocess.Popen(self.exec_command, shell=False, stderr=console_output,
                                                         stdout=console_output)

        self.dandere2x_cpp_subprocess.wait()

        if self.dandere2x_cpp_subprocess.returncode == 0:
            logger.info("D2xcpp finished correctly.")
        elif self.dandere2x_cpp_subprocess.returncode != 0:
            logger.error("D2xcpp ended unexpectedly.")
            logger.error("Dandere2x will stop the current session.")
            raise Exception
