import copy
import glob
import os
import shutil
import time

from dandere2x import Dandere2x
from context import Context
from dandere2xlib.utils.dandere2x_utils import wait_on_file, dir_exists, file_exists

class Dandere2xUpscaleFolder:
    """
    A wrapper that wraps around dandere2x that upscales an entire folder. It does this by creating
    a new 'yaml' config for each video file in the folder.
    """

    def __init__(self, config_yaml):
        self.config_yaml = config_yaml
        self.input_folder = config_yaml['dandere2x']['usersettings']['input_folder']
        self.output_folder = config_yaml['dandere2x']['usersettings']['output_folder']
        self.workspace = config_yaml['dandere2x']['developer_settings']['workspace']

    def start(self):

        files_in_folder = []

        for file in glob.glob(os.path.join(self.input_folder, "*")):
            files_in_folder.append(os.path.basename(file))

        for x in range(len(files_in_folder)):
            # Cycle through each file

            iteration_yaml = copy.copy(self.config_yaml)

            file_name = os.path.join(self.input_folder, files_in_folder[x])

            path, name = os.path.split(files_in_folder[x])
            name_only = name.split(".")[0]

            # Set the output name to be 'upscaled + original name'
            output_name = os.path.join(self.output_folder, "upscaled_" + name_only + ".mp4")

            # change the yaml to contain the data for this iteration of dandere2x
            iteration_yaml['dandere2x']['usersettings']['input_file'] = file_name
            iteration_yaml['dandere2x']['usersettings']['output_file'] = output_name
            iteration_yaml['dandere2x']['developer_settings']['workspace'] = self.workspace + str(x) + os.path.sep

            context = Context(iteration_yaml)

            # Delete the workspace if it already exists to prevent bugs
            if dir_exists(context.workspace):
                print("Deleted Folder")

                try:
                    shutil.rmtree(context.workspace)
                except PermissionError:
                    print("Trying to delete workspace via RM tree threw PermissionError - Dandere2x may not work.")

                while (file_exists(context.workspace)):
                    time.sleep(1)

            d2x = Dandere2x(context)
            d2x.start()

            wait_on_file(d2x.context.nosound_file)
            d2x.join()
