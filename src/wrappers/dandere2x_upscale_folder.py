from context import Context
from dandere2xlib.utils.dandere2x_utils import get_operating_system
from wrappers.dandere2x_gui_wrapper import Dandere2x_Gui_Wrapper
import os
import yaml
import glob
import time
import copy

class Dandere2x_Upscale_Folder:

    def __init__(self, config_yaml):
        self.config_yaml = config_yaml
        self.context = Context(config_yaml)
        self.input_folder = self.context.input_folder
        self.output_folder = self.context.output_folder
        self.workspace = self.context.workspace

    def start(self):

        files_in_folder = []

        for file in glob.glob(os.path.join(self.input_folder, "*")):
            files_in_folder.append(os.path.basename(file))

        for x in range(len(files_in_folder)):

            iteration_file = copy.copy(self.config_yaml)

            file_name = os.path.join(self.input_folder, files_in_folder[x])
            output_name = os.path.join(self.output_folder, "upscaled_" + files_in_folder[x])

            iteration_file['dandere2x']['usersettings']['input_file'] = file_name
            iteration_file['dandere2x']['usersettings']['output_file'] = output_name
            iteration_file['dandere2x']['developer_settings']['workspace'] = self.workspace + str(x) + os.path.sep

            print("iteration file is ")
            print(iteration_file)

            d2x = Dandere2x_Gui_Wrapper(iteration_file)
            d2x.start()
