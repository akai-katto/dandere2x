import os
from abc import ABC, abstractmethod

# Abstract Class
from dandere2x.dandere2x_service_request import Dandere2xServiceRequest
from dandere2xlib.utils.dandere2x_utils import force_delete_directory
from wrappers.ffmpeg.ffmpeg import append_resize_filter_to_pre_process


class Dandere2xInterface(ABC):
    """
    Dandere2x now has two routes of operations (starting N different dandere2x instances, or one single instance)
    and functions needs to be abstracted outwards as a result. Unfortunately, starting dandere2x requires two different
    interfaces that will work with dandere2x differently in order to correctly handle both instances.
    """

    def __init__(self, service_request: Dandere2xServiceRequest):
        self.service_request = service_request

        if os.path.exists(self.service_request.workspace):
            print("Workspace already exists.. deleting")
            force_delete_directory(self.service_request.workspace)

        os.makedirs(service_request.workspace)

    @abstractmethod
    def _pre_process(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def on_completion(self):
        pass
    #
    # @abstractmethod
    # def join(self):
    #     pass

    @staticmethod
    def check_and_fix_resolution(input_file: str, block_size: int, output_options_original: dict) -> dict:
        import copy
        from wrappers.ffmpeg.videosettings import VideoSettings
        from dandere2xlib.utils.yaml_utils import load_executable_paths_yaml

        def valid_input_resolution(width: int, height: int, block_size: int):
            return width % block_size == 0 and height % block_size == 0

        new_output_options = copy.copy(output_options_original)

        # get meta-data from the video to do pre-processing
        ffprobe_path = load_executable_paths_yaml()['ffprobe']
        video_settings = VideoSettings(ffprobe_path, input_file)
        width, height = video_settings.width, video_settings.height

        if not valid_input_resolution(width=width, height=height, block_size=block_size):
            append_resize_filter_to_pre_process(output_options=new_output_options,
                                                width=width,
                                                height=height,
                                                block_size=block_size)
            # implement dar here later

        return new_output_options