import copy
import os

from dandere2x.dandere2x_service import Dandere2xServiceThread
from dandere2x.dandere2x_service.service_types.dandere2x_service_interface import Dandere2xServiceInterface
from dandere2x.dandere2x_service_request import Dandere2xServiceRequest
from dandere2x.dandere2xlib.utils.yaml_utils import load_executable_paths_yaml
from dandere2x.dandere2xlib.wrappers.ffmpeg.ffmpeg import migrate_tracks_contextless, is_file_video


class SingleProcessService(Dandere2xServiceInterface):

    def __init__(self, service_request: Dandere2xServiceRequest):
        """
        Uses a single Dandere2xServiceThread object to upscale a video file.

        Args:
            service_request: Dandere2xServiceRequest object.
        """
        super().__init__(service_request=copy.deepcopy(service_request))

        assert is_file_video(ffprobe_dir=load_executable_paths_yaml()['ffprobe'],
                             input_video=self._service_request.input_file),\
            "%s is not a video file!" % self._service_request.input_file

        self.child_request = copy.deepcopy(service_request)
        self.child_request.input_file = os.path.join(service_request.workspace, service_request.input_file)
        self.child_request.output_file = os.path.join(service_request.workspace, "non_migrated.mkv")
        self.child_request.workspace = os.path.join(service_request.workspace, "subworkspace")
        self.dandere2x_service = None

    def _pre_process(self):
        """
        Creates self.child_request.input_file file by re-encoding self._service_request.input_file. Without this
        re-encode, dandere2x isn't guaranteed to function correctly.
        """
        self.dandere2x_service = Dandere2xServiceThread(service_request=self.child_request)

    def run(self):
        self._pre_process()
        self.dandere2x_service.start()
        self.dandere2x_service.join()
        self._on_completion()

    def _on_completion(self):
        """
        Finishes the video up by migrating the audio tracks from the child's output file with the original input file.
        """
        ffmpeg_path = load_executable_paths_yaml()['ffmpeg']
        migrate_tracks_contextless(ffmpeg_dir=ffmpeg_path, no_audio=self.child_request.output_file,
                                   file_dir=self._service_request.input_file,
                                   output_file=self._service_request.output_file,
                                   output_options=self._service_request.output_options,
                                   console_output_dir=self._service_request.workspace)
