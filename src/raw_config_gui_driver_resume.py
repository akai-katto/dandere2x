"""
Start the dandere2x_gui_wrapper class using the .yaml. Essentially, use this if you want to
simulate d2x being started from the gui w/o having to actually use the GUI.

Starting from this driver will do stuff the GUI will do, such as delete the workspace, and other functions
if decided on by the user.
"""

import time

import yaml

from dandere2xlib.utils.dandere2x_utils import get_operating_system
from wrappers.resume_wrapper import Dandere2x_Gui_Wrapper_Resume


def main():
    start = time.time()

    # get config based on OS
    resume_file = "C:\\Users\\windwoz\\Documents\\GitHub\\dandere2x\\src\\workspace\\default\\33\\43\\suspended_session_data.yaml"

    # load yaml

    with open(resume_file, "r") as read_file:
        resume = yaml.safe_load(read_file)

    # continue d2x
    d2x = Dandere2x_Gui_Wrapper_Resume(resume, resume)
    d2x.start()

    print("\n Total runtime duration:", time.time() - start)


if __name__ == "__main__":
    main()
