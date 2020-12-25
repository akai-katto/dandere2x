import copy
import glob
import os

from pathlib import Path
from typing import Type, List

from dandere2x.dandere2x_service import Dandere2xServiceThread
from dandere2x.dandere2x_service_request import Dandere2xServiceRequest
from dandere2x.dandere2xlib.utils.yaml_utils import load_executable_paths_yaml
from dandere2x.dandere2xlib.wrappers.ffmpeg.ffmpeg import convert_gif_to_video, convert_video_to_gif
from dandere2x.service_types.dandere2x_service_interface import Dandere2xInterface


class FolderProcess(Dandere2xInterface):

    def __init__(self, service_request: Dandere2xServiceRequest):
        super().__init__(service_request=copy.deepcopy(service_request))
        self.service_request_list: List[Dandere2xServiceRequest] = []

    def _pre_process(self):
        assert os.path.isdir(self._service_request.input_file),\
            "%s file not a directory!" % self._service_request.input_file
        assert os.path.isdir(self._service_request.output_file),\
            "%s is not a directory!" % self._service_request.output_file

        # get a list of file names in a folder
        list_of_files = glob.glob(os.path.join(self._service_request.input_file, "*"))

        # remove non-directories
        list_of_files = filter(os.path.isfile, list_of_files)

        print("list of files %s" % str(list_of_files))
        for item in list_of_files:

            # create a new service request for each file in a folder, replacing the input_file and output file for each.
            current_request: Dandere2xServiceRequest = copy.deepcopy(self._service_request)
            current_request.input_file = item

            # set each output_file with the name "upscaled + [name_here]"
            output_path_name = os.path.join(current_request.output_file, "upscaled_" + Path(item).name)
            current_request.output_file = output_path_name

            self.service_request_list.append(current_request)


    def run(self):
        from dandere2x import Dandere2x
        self._pre_process()

        for sub_service in self.service_request_list:
            print("Processing %s" % sub_service.input_file)

            sub_service.make_workspace()
            instance = Dandere2x(service_request=sub_service)
            instance.start()
            instance.join()

            print("%s completed" % sub_service.input_file)

        self._on_completion()

    def _on_completion(self):
        pass
