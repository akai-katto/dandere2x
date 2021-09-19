import argparse
import copy
import logging
import os
import shutil
from enum import Enum

import yaml


class ProcessingType(Enum):
    SINGLE_PROCESS = "single"
    MULTI_PROCESS = "multi"

    @staticmethod
    def from_str(input: str):
        if input == "single":
            return ProcessingType.SINGLE_PROCESS
        if input == "multi":
            return ProcessingType.MULTI_PROCESS

        raise Exception("processing type not found %s", input)


class UpscalingEngineType(Enum):
    VULKAN = "vulkan"
    CONVERTER_CPP = "converter_cpp"
    CAFFE = "caffe"

    @staticmethod
    def from_str(input: str):
        if input == "vulkan":
            return UpscalingEngineType.VULKAN
        if input == "converter_cpp":
            return UpscalingEngineType.CONVERTER_CPP
        if input == "caffe":
            return UpscalingEngineType.CAFFE

        raise Exception("UpscalingEngineType not found %s" % input)


class Dandere2xServiceRequest:

    # todo, rename quality_minimum -> image_quality
    def __init__(self,
                 input_file: str,
                 output_file: str,
                 workspace: str,
                 block_size: int,
                 denoise_level: int,
                 quality_minimum: int,
                 scale_factor: int,
                 output_options: dict,
                 name: str,
                 processing_type: ProcessingType,
                 upscale_engine: UpscalingEngineType):
        """
        The highest-level of abstraction Dandere2x uses to upscale a video file. These variables are set explicitly
        by the user, and may be modified by the program in lower-levels of the program to meet the needs of the
        process_type selected (i.e behaviour of a gif / video will differ).

        Args:
            input_file:
            output_file:
            workspace:
            block_size:
            denoise_level:
            quality_minimum:
            scale_factor:
            output_options:
            name: Name string used 
            processing_type:
            upscale_engine:
        """

        self.workspace: str = os.path.abspath(workspace)
        self.scale_factor: int = scale_factor
        self.quality_minimum: int = quality_minimum
        self.denoise_level: int = denoise_level
        self.block_size: int = block_size
        self.output_file: str = output_file
        self.input_file: str = input_file
        self.output_options: dict = copy.deepcopy(output_options)
        self.name: str = name
        self.processing_type: ProcessingType = processing_type
        self.upscale_engine: UpscalingEngineType = upscale_engine

    @classmethod
    def load_from_args(cls, args):
        """
        Constructs a service request from args.
        @param args: An argsparse instance
        @return: The "root" Dandere2xServiceRequest, using the args object as it's input.
        """

        with open(args.config, "r") as read_file:
            output_config = yaml.safe_load(read_file)

        request = \
            Dandere2xServiceRequest(
                input_file=os.path.abspath(args.input_file),
                output_file=os.path.abspath(args.output_file),
                workspace=os.path.abspath(args.workspace),
                block_size=args.block_size,
                denoise_level=args.noise_level,
                quality_minimum=args.image_quality,
                scale_factor=args.scale_factor,
                output_options=output_config,
                processing_type=ProcessingType.from_str(args.processing_type),
                name="Master Service Request",
                upscale_engine=UpscalingEngineType.from_str(args.waifu2x_type))

        return request

    @staticmethod
    def get_args_parser():
        """
        Create a parser for dandere2x for the needed arguments.
        :return: ArgsParse for dandere2x.
        """

        parser = argparse.ArgumentParser()

        parser.add_argument('-c', '--config', action="store", dest="config", type=str,
                            default="./config_files/output_options.yaml",
                            help='Config path. Defaults to "./config_files/output_options.yaml"')

        parser.add_argument('-b', '--block_size', action="store", dest="block_size", type=int, default=30,
                            help='Block Size (Default 30)')

        parser.add_argument('-i', '--input', action="store", dest="input_file", help='Input Video (no default)')

        parser.add_argument('-o', '--output', action="store", dest="output_file", help='Output Video (no default)')

        parser.add_argument('-q', '--quality', action="store", dest="image_quality", type=int, default=97,
                            help='Image Quality (Default 85)')

        parser.add_argument('-w', '--waifu2x_type', action="store", dest="waifu2x_type", type=str, default="vulkan",
                            help='Waifu2x Type. Options: "vulkan" "converter_cpp" "caffe". Default: "vulkan"')

        parser.add_argument('-s', '--scale_factor', action="store", dest="scale_factor", type=int, default=2,
                            help='Scale Factor (Default 2)')

        parser.add_argument('-n', '--noise_level', action="store", dest="noise_level", type=int, default=3,
                            help='Denoise Noise Level (Default 3)')

        parser.add_argument('-p', '--process_type', action="store", dest="processing_type", type=str, default="single",
                            help='Processing Type (Options: "single", "multi"')

        parser.add_argument('-ws', '--workspace', action="store", dest="workspace", type=str, default="./workspace/",
                            help='Workspace directory for dandere2x.')

        args = parser.parse_args()
        return args

    def make_workspace(self):

        print("attempting to make or clear % s" % self.workspace)
        if os.path.exists(self.workspace):
            shutil.rmtree(self.workspace)

        os.mkdir(self.workspace)

    def log_all_variables(self):
        log = logging.getLogger()
        log.info("Service Request Settings:")
        for item in self.__dict__:
            # log.info("%s : %s" % (item, self.__dict__[item]))
            print("%s : %s" % (item, self.__dict__[item]))
