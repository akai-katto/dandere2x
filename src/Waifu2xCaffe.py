import os
import subprocess
import threading

from Dandere2xUtils import get_lexicon_value



# temporary implementation of waifu2x-caffe wrapper

class Waifu2xCaffe(threading.Thread):

    def __init__(self, frame_count, waifu2x_caffe_dir, output_dir, upscaled_dir, p_setting, noise_level, scale_factor):
        self.frame_count = frame_count
        self.waifu2x_caffe_dir = waifu2x_caffe_dir
        self.output_dir = output_dir
        self.upscaled_dir = upscaled_dir
        self.p_setting = p_setting
        self.noise_level = noise_level
        self.scale_factor = scale_factor
        threading.Thread.__init__(self)

    @staticmethod
    def upscale_file(waifu2x_caffe_dir, input_file, output, setting, noise_level, scale_factor):
        command = waifu2x_caffe_dir + " -i " + input_file + " -p " + setting + " -n " + noise_level +\
                  " -s " + scale_factor + " -o " + output
        exec = command.split(" ")
        subprocess.run(exec)

    def run(self):
        command = self.waifu2x_caffe_dir + " -i " + self.output_dir + " -p " + self.p_setting + " -n " +\
                  self.noise_level + " -s " + self.scale_factor + " -o " + self.upscaled_dir
        exec = command.split(" ")
        names = []

        for x in range(1, self.frame_count):
            names.append("output_" + get_lexicon_value(6, x) + ".png")

        while names:
            subprocess.run(exec)
            for item in names[::-1]:
                print(self.output_dir + item)
                print(os.path.isfile(self.upscaled_dir + item))
                if os.path.isfile(self.upscaled_dir + item):
                    os.remove(self.output_dir + item)
                    names.remove(item)
