import time
from abc import abstractmethod, ABC
from threading import Thread

from dandere2x.dandere2x_service_request import Dandere2xServiceRequest


class Dandere2xServiceInterface(Thread, ABC):
    """
    An abstract-base-class dictating how dandere2x_service should be utilized.

    As an example, a singleprocess_service will only use one dandere2x-thread to upscale a video file, where as
    multiprocess_service will use multiple. In either case, an upscaled video will still be produced, but the black
    box implementation in between will change.

    This abstract-interface gives enough shared functions / descriptions of how the black-box should be implemented,
    See singleprocess_service.py or gif_service.py for examples of how to use these shared functions / see why they
    exist.
    """

    def __init__(self, service_request: Dandere2xServiceRequest):
        super().__init__()

        self._service_request = service_request

        # meta-data
        self.__start_time: float = 0
        self.__end_time: float = 0

    # Public Methods

    def timer_start(self) -> None:
        self.__start_time = time.time()

    def timer_end(self) -> None:
        self.__end_time = time.time()

    def timer_get_duration(self) -> float:
        return self.__end_time - self.__start_time

    @abstractmethod
    def run(self):
        pass

    # Protected Methods

    @abstractmethod
    def _pre_process(self):
        pass

    @abstractmethod
    def _on_completion(self):
        pass

    @staticmethod
    def _check_and_fix_resolution(input_file: str, block_size: int, output_options_original: dict) -> dict:
        """
        Returns a dictionary containing the output settings, taking into consideration if the video needs to be resized,
        and if it does, changes the pipe_video commands to include dar.
        """
        from dandere2x.dandere2xlib.utils.yaml_utils import load_executable_paths_yaml
        from dandere2x.dandere2xlib.wrappers.ffmpeg.ffmpeg import append_resize_filter_to_pre_process, \
            append_dar_filter_to_pipe_process
        from dandere2x.dandere2xlib.wrappers.ffmpeg.videosettings import VideoSettings
        import copy

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
            append_dar_filter_to_pipe_process(output_options=new_output_options,
                                              width=width,
                                              height=height)

        return new_output_options
