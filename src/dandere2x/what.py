import copy
import os

from threading import Thread
from dandere2x.dandere2x_interface import Dandere2xInterface
from dandere2x.dandere2x_service_request import Dandere2xServiceRequest
from dandere2x.dandere2x_service import Dandere2xServiceThread
from dandere2xlib.utils.yaml_utils import load_executable_paths_yaml
from wrappers.ffmpeg.ffmpeg import re_encode_video_contextless, migrate_tracks_contextless


class What(Dandere2xInterface):

    def __init__(self, service_request: Dandere2xServiceRequest):
        super().__init__(service_request=service_request)

        self.child_request = copy.copy(service_request)
        self.child_request.input_file = os.path.join(service_request.workspace, "pre_processed.mkv")
        self.child_request.output_file = os.path.join(service_request.workspace, "non_migrated.mkv")
        self.child_request.workspace = os.path.join(service_request.workspace, "subworkspace")
        self.dandere2x_service = None

    def _pre_process(self):
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

        self.dandere2x_service = Dandere2xServiceThread(service_request=self.child_request)

    def start(self):
        self._pre_process()
        self.dandere2x_service.start()

    # migrate_tracks(context: Context, no_audio: str, file_dir: str, output_file: str, copy_if_failed=False):
    def on_completion(self):
        ffmpeg_path = load_executable_paths_yaml()['ffmpeg']

        migrate_tracks_contextless(ffmpeg_dir=ffmpeg_path, no_audio=self.child_request.output_file,
                                   file_dir=self.service_request.input_file, output_file=self.service_request.output_file)


    def join(self):
        self.dandere2x_service.join()
