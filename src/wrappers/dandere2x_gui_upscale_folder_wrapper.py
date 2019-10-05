import copy
import glob
import os

from context import Context
from wrappers.dandere2x_gui_wrapper import Dandere2x_Gui_Wrapper


class Dandere2xUpscaleFolder:
    """
    A wrapper that wraps around dandere2_gui_wrapper that upscales an entire folder.
    """

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
            iteration_yaml = copy.copy(self.config_yaml)

            file_name = os.path.join(self.input_folder, files_in_folder[x])
            output_name = os.path.join(self.output_folder, "upscaled_" + files_in_folder[x])

            # change the yaml to contain the data for this iteration of dandere2x
            iteration_yaml['dandere2x']['usersettings']['input_file'] = file_name
            iteration_yaml['dandere2x']['usersettings']['output_file'] = output_name
            iteration_yaml['dandere2x']['developer_settings']['workspace'] = self.workspace + str(x) + os.path.sep

            d2x = Dandere2x_Gui_Wrapper(iteration_yaml)
            d2x.start()
