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

        raise Exception("processing type not found %s" % input)


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
                 processing_type: ProcessingType):

        self.workspace: str = workspace
        self.scale_factor: int = scale_factor
        self.quality_minimum: int = quality_minimum
        self.denoise_level: int = denoise_level
        self.block_size: int = block_size
        self.output_file: str = output_file
        self.input_file: str = input_file
        self.output_options: dict = copy.deepcopy(output_options)
        self.name: str = name
        self.processing_type: ProcessingType = processing_type

    @classmethod
    def load_from_args(cls, args):
        """
        Constructs a service request from args.
        @param args: An argsparse instance
        @return: The "root" Dandere2xServiceRequest, using the args object as it's input.
        """

        with open("output_options.yaml", "r") as read_file:
            output_config = yaml.safe_load(read_file)

        request = \
            Dandere2xServiceRequest(
                input_file=args.input_file,
                output_file=args.output_file,
                workspace=os.path.abspath(args.workspace),
                block_size=args.block_size,
                denoise_level=args.noise_level,
                quality_minimum=args.image_quality,
                scale_factor=args.scale_factor,
                output_options=output_config,
                processing_type=ProcessingType.from_str(args.processing_type),
                name="Master Service Request")

        return request

    @staticmethod
    def get_args_parser():
        """
        Create a parser for dandere2x for the needed arguments.
        :return: ArgsParse for dandere2x.
        """

        parser = argparse.ArgumentParser()

        parser.add_argument('-b', '--block_size', action="store", dest="block_size", type=int, default=30,
                            help='Block Size (Default 30)')

        parser.add_argument('-i', '--input', action="store", dest="input_file", help='Input Video (no default)')

        parser.add_argument('-o', '--output', action="store", dest="output_file", help='Output Video (no default)')

        parser.add_argument('-q', '--quality', action="store", dest="image_quality", type=int, default=85,
                            help='Image Quality (Default 85)')

        parser.add_argument('-w', '--waifu2x_type', action="store", dest="waifu2x_type", type=str, default="vulkan",
                            help='Waifu2x Type. Options: "vulkan" "converter-cpp" "caffe". Default: "vulkan"')

        parser.add_argument('-s', '--scale_factor', action="store", dest="scale_factor", type=int, default=2,
                            help='Scale Factor (Default 2)')

        parser.add_argument('-n', '--noise_level', action="store", dest="noise_level", type=int, default=3,
                            help='Denoise Noise Level (Default 3)')

        parser.add_argument('-p', '--process_type', action="store", dest="processing_type", type=str, default="single",
                            help='Processing Type (Options: "single", "multi"')

        parser.add_argument('-ws', '--workspace', action="store", dest="workspace", type=str, default=".",
                            help='Workspace Directory (Default "." ) ')

        args = parser.parse_args()
        return args

    def make_workspace(self):
        if os.path.exists(self.workspace):
            shutil.rmtree(self.workspace)

        os.mkdir(self.workspace)

    def log_all_variables(self):
        log = logging.getLogger()
        log.info("Service Request Settings:")
        for item in self.__dict__:
            # log.info("%s : %s" % (item, self.__dict__[item]))
            print("%s : %s" % (item, self.__dict__[item]))