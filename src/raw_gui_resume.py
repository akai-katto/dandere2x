"""
Start the dandere2x_gui_wrapper class using the .yaml. Essentially, use this if you want to
simulate d2x being started from the gui w/o having to actually use the GUI.

Starting from this driver will do stuff the GUI will do, such as delete the workspace, and other functions
if decided on by the user.
"""

import time

import yaml

from dandere2xlib.utils.dandere2x_utils import get_operating_system
from wrappers.dandere2x_gui_wrapper import Dandere2x_Gui_Wrapper
from wrappers.resume_wrapper import Dandere2x_Gui_Wrapper_Resume


def main():
    start = time.time()

    # get config based on OS
    configfile = "dandere2x_%s.yaml" % get_operating_system()

    # load yaml

    with open(configfile, "r") as read_file:
        config = yaml.safe_load(read_file)

    resume_file = "C:\\Users\\windwoz\\Documents\\GitHub\\dandere2x\\src\\workspace\\default\\death_folder.txt"

    # load yaml

    with open(resume_file, "r") as read_file:
        resume_yaml = yaml.safe_load(read_file)

    # continue d2x
    d2x = Dandere2x_Gui_Wrapper_Resume(config, resume_yaml)
    d2x.start()

    print("\n Total runtime duration:", time.time() - start)


if __name__ == "__main__":
    main()
