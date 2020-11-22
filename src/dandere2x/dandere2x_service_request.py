import copy
import logging
import os
import shutil
from enum import Enum

# code from https://docs.python.org/3/library/enum.html

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


def get_root_thread_from_root_service_request(request: Dandere2xServiceRequest):
    if request.processing_type == ProcessingType.MULTI_PROCESS:
        from dandere2x.multiprocess import MultiProcess
        return MultiProcess

    if request.processing_type == ProcessingType.SINGLE_PROCESS:
        from dandere2x.singleprocess import SingleProcess
        return SingleProcess
