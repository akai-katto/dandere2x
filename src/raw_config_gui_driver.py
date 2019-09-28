"""
Start the dandere2x_gui_wrapper class using the .yaml. Essentially, use this if you want to
simulate d2x being started from the gui w/o having to actually use the GUI.

Starting from this driver will do stuff the GUI will do, such as delete the workspace, and other functions
if decided on by the user.
"""

from dandere2xlib.utils.dandere2x_utils import get_operating_system
from wrappers.dandere2x_gui_wrapper import Dandere2x_Gui_Wrapper

import time
import yaml


def main():

    start = time.time()

    # get config based on OS
    configfile = "dandere2x_%s.yaml" % get_operating_system()

    # load yaml

    with open(configfile, "r") as read_file:
        config = yaml.safe_load(read_file)

    # continue d2x
    d2x = Dandere2x_Gui_Wrapper(config)
    d2x.start()

    print("\n Total runtime duration:", time.time() - start)

if __name__ == "__main__":
    main()
