import copy
import os

from dandere2x.dandere2x_interface import Dandere2xInterface
from dandere2x.dandere2x_service_request import Dandere2xServiceRequest
from dandere2xlib.utils.yaml_utils import load_executable_paths_yaml
from wrappers.ffmpeg.ffmpeg import re_encode_video_contextless


class What(Dandere2xInterface):

    def __init__(self, service_request: Dandere2xServiceRequest):
        super().__init__(service_request=service_request)

        self.child_request = copy.copy(service_request)
        self.child_request.input_file = os.path.join(service_request.workspace, "pre_processed.mkv")
        self.child_request.output_file = os.path.join(service_request.workspace, "non_migrated.mkv")
        self.child_request.workspace = os.path.join(service_request.workspace, ".mkv")

    def pre_process(self):
        resized_output = Dandere2xInterface.check_and_fix_resolution(input_file=self.service_request.input_file,
                                                                     block_size=self.service_request.block_size,
                                                                     output_options_original=self.service_request.output_options)

        ffprobe_path = load_executable_paths_yaml()['ffprobe']
        ffmpeg_path = load_executable_paths_yaml()['ffmpeg']

        re_encode_video_contextless(ffmpeg_dir=ffmpeg_path,
                                    ffprobe_dir=ffprobe_path,
                                    output_options=resized_output,
                                    input_file=self.service_request.input_file,
                                    output_file=self.child_request.input_file)

    def join(self):
        pass

    def on_completion(self):
        pass

    def start(self):
        pass
