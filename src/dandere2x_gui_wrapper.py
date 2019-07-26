# For the GUI to work around

import os
import shutil

from context import Context
from dandere2x import Dandere2x
from dandere2x_core.dandere2x_utils import dir_exists

class Dandere2x_Gui_Wrapper:

    def __init__(self, config_json):
        self.config_json = config_json
        self.context = Context(config_json)

    def start(self):
        print(self.context.workspace)

        if dir_exists(self.context.workspace):
            print("deleted shit")
            shutil.rmtree(self.context.workspace)

        # starting shit
        print("starting shit")
        d = Dandere2x(self.context)
        d.run_concurrent()
        d.context.close_logger()

        d.delete_workspace_files()


        # if folder exists, delete



