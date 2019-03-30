import logging
import os
import subprocess
import threading


# should this be a script instead of a class?

class Dandere2xCppWrapper(threading.Thread):
    def __init__(self, workspace, dandere2x_cpp_dir, frame_count, block_size, tolerance, psnr_high, \
                 psnr_low, step_size, extension_type, resume):
        self.workspace = workspace
        self.dandere2x_cpp_dir = dandere2x_cpp_dir
        self.frame_count = frame_count
        self.block_size = block_size
        self.tolerance = tolerance
        self.psnr_high = psnr_high
        self.psnr_low = psnr_low
        self.step_size = step_size
        self.extension_type = extension_type
        self.resume = resume
        threading.Thread.__init__(self)

    def run(self):
        if not self.resume:
            self.new_run()

        elif self.resume:
            self.resume_run()

    def new_run(self):
        logger = logging.getLogger(__name__)
        exec = [self.dandere2x_cpp_dir, self.workspace, str(self.frame_count),
                str(self.block_size), str(self.tolerance),
                str(self.psnr_high), str(self.psnr_low), str(self.step_size), "n",
                str(1), self.extension_type]

        logger.info(exec)
        subprocess.run(exec, creationflags=subprocess.CREATE_NEW_CONSOLE)
        logger.info("finished correctly")

    def resume_run(self):
        logger = logging.getLogger(__name__)
        last_found = int(self.frame_count)

        logger.info("looking for previous frames...")
        while last_found > 0:
            exists = os.path.isfile(
                self.workspace + os.path.sep + "pframe_data" + os.path.sep + "pframe_" + str(last_found) + ".txt")
            if not exists:
                last_found -= 1

            elif exists:
                break

        last_found = last_found - 1

        logger.info("last found is " + str(last_found))

        exec = [self.dandere2x_cpp_dir, self.workspace, str(self.frame_count),
                str(self.block_size), str(self.tolerance),
                str(self.psnr_high), str(self.psnr_low), str(self.step_size), "r",
                str(last_found), self.extension_type]

        logger.info(exec)
        subprocess.run(exec, creationflags=subprocess.CREATE_NEW_CONSOLE)
        logger.info("finished correctly")
