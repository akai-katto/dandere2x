import logging
import os
import subprocess
import threading

from Dandere2xUtils import get_lexicon_value


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

        exec = [waifu2x_caffe_dir, "-i", input_file, "-p", setting, "-n", noise_level, "-s",
                scale_factor, "-o", output]

        if model_dir != "default":
            exec.append("--model_dir")
            exec.append(model_dir)

        logger.info("manually upscaling file")
        logger.info(exec)
        subprocess.run(exec)

    def run(self):
        logger = logging.getLogger(__name__)
        exec = [self.waifu2x_caffe_dir, "-i", self.output_dir, "-p",
                self.p_setting, "-n", self.noise_level, "-s", self.scale_factor, "-o", self.upscaled_dir]

        if self.model_dir != "default":
            exec.append("--model_dir")
            exec.append(self.model_dir)

        logger.info("waifu2xcaffe session")
        logger.info(exec)

        names = []
        for x in range(1, self.frame_count):
            names.append("output_" + get_lexicon_value(6, x) + ".png")

        count_removed = 0

        # for resuming
        for item in names[::-1]:
            if os.path.isfile(self.upscaled_dir + item):
                names.remove(item)
                count_removed += 1

        if count_removed:
            logger.info("Already have " + str(count_removed) + " upscaled")

        while names:
            logger.info("Frames remaining before batch: ")
            logger.info(len(names))
            subprocess.run(exec)
            for item in names[::-1]:
                if os.path.isfile(self.upscaled_dir + item):
                    os.remove(self.output_dir + item)
                    names.remove(item)
