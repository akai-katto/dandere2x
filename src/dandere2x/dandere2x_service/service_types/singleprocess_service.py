import copy
import os

from dandere2x.dandere2x_service import Dandere2xServiceThread
from dandere2x.dandere2x_service.service_types.dandere2x_service_interface import Dandere2xServiceInterface
from dandere2x.dandere2x_service_request import Dandere2xServiceRequest
from dandere2x.dandere2xlib.utils.yaml_utils import load_executable_paths_yaml
from dandere2x.dandere2xlib.wrappers.ffmpeg.ffmpeg import re_encode_video, migrate_tracks_contextless


class SingleProcessService(Dandere2xServiceInterface):

    def __init__(self, service_request: Dandere2xServiceRequest):
        """
        Uses a single Dandere2xServiceThread object to upscale a video file.

        Args:
            service_request: Dandere2xServiceRequest object.
        """
        super().__init__(service_request=copy.deepcopy(service_request))

        self.child_request = copy.deepcopy(service_request)
        self.child_request.input_file = os.path.join(service_request.workspace, "pre_processed.mkv")
        self.child_request.output_file = os.path.join(service_request.workspace, "non_migrated.mkv")
        self.child_request.workspace = os.path.join(service_request.workspace, "subworkspace")
        self.dandere2x_service = None

    def _pre_process(self):
        """
        Creates self.child_request.input_file file by re-encoding self._service_request.input_file. Without this
        re-encode, dandere2x isn't guaranteed to function correctly.
        """

        # Checks to see the video needs to be resized in order to conform to the block size. Applies the "DAR"
        # ffmpeg filter to 'pipe_video' in 'output_options.yaml' if the video was resized.
        resized_output_options = Dandere2xServiceInterface._check_and_fix_resolution(
            input_file=self._service_request.input_file,
            block_size=self._service_request.block_size,
            output_options_original=self._service_request.output_options)

        ffprobe_path = load_executable_paths_yaml()['ffprobe']
        ffmpeg_path = load_executable_paths_yaml()['ffmpeg']

        # Re-encode the sent service_request into the child's input file, so that the child_request will operate on
        # "pre_processed.mkv", rather than self._service_request.input_file, which may not be a valid video file to
        # operate on.
        re_encode_video(ffmpeg_dir=ffmpeg_path,
                        ffprobe_dir=ffprobe_path,
                        output_options=resized_output_options,
                        input_file=self._service_request.input_file,
                        output_file=self.child_request.input_file)

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
                                   output_file=self._service_request.output_file)
