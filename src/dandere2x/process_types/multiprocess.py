import copy
import glob
import os

from dandere2x.dandere2x_service.dandere2x_service_interface import Dandere2xInterface
from dandere2x.dandere2x_service.__init__ import Dandere2xServiceThread
from dandere2x.dandere2x_service_request import Dandere2xServiceRequest
from dandere2xlib.utils.yaml_utils import load_executable_paths_yaml
from dandere2xlib.wrappers.ffmpeg.ffmpeg import divide_and_reencode_video, concat_n_videos, migrate_tracks_contextless


class MultiProcess(Dandere2xInterface):

    def __init__(self, service_request: Dandere2xServiceRequest):
        super().__init__(service_request=copy.deepcopy(service_request))
        self._child_requests = []
        self.divided_videos_upscaled: list = []

    def _pre_process(self):
        resized_output_options = Dandere2xInterface._check_and_fix_resolution(
            input_file=self._service_request.input_file,
            block_size=self._service_request.block_size,
            output_options_original=self._service_request.output_options)

        ffprobe_path = load_executable_paths_yaml()['ffprobe']
        ffmpeg_path = load_executable_paths_yaml()['ffmpeg']

        divide_and_reencode_video(ffmpeg_dir=ffmpeg_path, ffprobe_path=ffprobe_path,
                                  input_video=self._service_request.input_file,
                                  output_options=resized_output_options,
                                  divide=3, output_dir=self._service_request.workspace)

        divided_re_encoded_videos = glob.glob(os.path.join(self._service_request.workspace, "*.mkv"))

        for x in range(0, len(divided_re_encoded_videos)):
            child_request = copy.deepcopy(self._service_request)
            child_request.input_file = os.path.join(divided_re_encoded_videos[x])
            child_request.output_file = os.path.join(self._service_request.workspace, "non_migrated%d.mkv" % x)
            child_request.workspace = os.path.join(self._service_request.workspace, "subworkspace%d" % x)

            self.divided_videos_upscaled.append(child_request.output_file)
            self._child_requests.append(Dandere2xServiceThread(child_request))

    def run(self):
        self._pre_process()

        for request in self._child_requests:
            request.start()

        for request in self._child_requests:
            request.join()

        self._on_completion()

    def _on_completion(self):
        ffmpeg_path = load_executable_paths_yaml()['ffmpeg']

        no_audio = os.path.join(self._service_request.workspace, "noaudio.mkv")
        concat_n_videos(ffmpeg_dir=ffmpeg_path, temp_file_dir=self._service_request.workspace,
                        console_output_dir=self._service_request.workspace, list_of_files=self.divided_videos_upscaled,
                        output_file=no_audio)

        migrate_tracks_contextless(ffmpeg_dir=ffmpeg_path, no_audio=no_audio,
                                   file_dir=self._service_request.input_file,
                                   output_file=self._service_request.output_file)
