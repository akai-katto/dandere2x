# For the GUI to work around

import os
import shutil
import time
import copy

from context import Context
from dandere2x import Dandere2x
from dandere2xlib.utils.dandere2x_utils import dir_exists, wait_on_delete_dir, rename_file_wait
from wrappers.ffmpeg.ffmpeg import concat_two_videos

class Dandere2x_Gui_Wrapper_Resume:
    """
    A wrapper to call dandere2x.py from the GUI. The extra-added faetures are clearing the workspace ahead of time
    and deleting the files after run-time, if gui_delete_workspace_after json is set to true.
    """

    def __init__(self, config_yaml, resume_yaml: dict):

        self.resume_yaml = resume_yaml
        self.start_frame = self.resume_yaml['signal_merged_count']
        config_yaml['dandere2x']['developer_settings']['workspace'] =\
            config_yaml['dandere2x']['developer_settings']['workspace'] + str(self.start_frame) + os.path.sep
        self.context = Context(config_yaml)


    def start(self):
        print(self.context.workspace)

        if dir_exists(self.context.workspace):
            print("Deleted Folder")

            # This is a recurring bug that seems to be popping up on other people's operating systems.
            # I'm unsure if this will fix it, but it could provide a solution for people who can't even get d2x to work.
            try:
                shutil.rmtree(self.context.workspace)
            except PermissionError:
                print("Trying to delete workspace via RM tree threw PermissionError - Dandere2x may not work.")

        wait_on_delete_dir(self.context.workspace)
        try:
            os.mkdir(self.context.workspace)
        except OSError:
            print("Creation of directory failed")

        start = time.time()

        # starting shit
        print("Starting Dandere2x")
        d = Dandere2x(self.context, self.start_frame)
        d.run()

        time.sleep(15)
        d.kill()
        d.join()

        file_to_be_concat = self.context.workspace + "file_to_be_concat.mp4"

        # need to migrate concat 
        rename_file_wait(self.context.nosound_file, file_to_be_concat)

        print("dandere2x is concating two videos")
        concat_two_videos(self.context, self.resume_yaml['nosound_file'], file_to_be_concat,self.context.nosound_file)

        # if d.context.config_yaml['dandere2x']['developer_settings']['gui_delete_workspace_after']:
        #     d.delete_workspace_files()

        print("Dandere2x GUI Run Finished Successfully")

        end = time.time()

        print("\n "
              "duration: " + str(time.time() - start))
