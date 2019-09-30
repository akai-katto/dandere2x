import logging
import subprocess
import threading

from context import Context
from dandere2xlib.utils.dandere2x_utils import get_operating_system


class Dandere2xCppWrapper(threading.Thread):
    """
    A wrapper for the dandere2x_cpp module. It simply calls the module using information used from the context.
    """

    def __init__(self, context: Context):
        # load stuff from context
        self.workspace = context.workspace
        self.dandere2x_cpp_dir = context.dandere2x_cpp_dir
        self.frame_count = context.frame_count
        self.block_size = context.block_size
        self.step_size = context.step_size
        self.extension_type = context.extension_type
        self.residual_images_dir = context.residual_images_dir
        self.log_dir = context.log_dir

        threading.Thread.__init__(self)

    def run(self):
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

        # On linux, we can't use subprocess.create_new_console, so we just write
        # The dandere2x_cpp output to a text file.
        if get_operating_system() == 'win32':
            return_val = subprocess.run(exec, creationflags=subprocess.CREATE_NEW_CONSOLE).returncode

        elif get_operating_system() == 'linux':
            console_output = open(self.log_dir + "dandere2x_cpp.txt", "w")
            console_output.write(str(exec))
            return_val = subprocess.run(exec, shell=False, stderr=console_output, stdout=console_output).returncode

        if return_val == 0:
            logger.info("d2xcpp finished correctly")
        else:
            logger.info("d2xcpp ended unexpectedly")
