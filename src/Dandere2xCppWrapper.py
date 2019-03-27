import os
import subprocess
import threading


# should this be a script instead of a class?

class Dandere2xCppWrapper(threading.Thread):
    def __init__(self, workspace, dandere2x_cpp_dir, frame_count, block_size, tolerance, psnr_high, \
                 psnr_low, step_size):
        self.workspace = workspace
        self.dandere2x_cpp_dir = dandere2x_cpp_dir
        self.frame_count = frame_count
        self.block_size = block_size
        self.tolerance = tolerance
        self.psnr_high = psnr_high
        self.psnr_low = psnr_low
        self.step_size = step_size
        threading.Thread.__init__(self)

    def run(self):
        command = self.dandere2x_cpp_dir + " " + self.workspace + " " + str(
            self.frame_count) + " " + str(self.block_size) + " " + \
                  str(self.tolerance) + " " + str(self.psnr_high) + " " + str(self.psnr_low) + " " + str(
            self.step_size) + " " + "n" + " " + str(15)

        exec = command.split(" ")

        print(exec)

        os.system("start cmd /K dir")  # /K remains the window, /C executes and dies (popup)
        subprocess.run(exec)
