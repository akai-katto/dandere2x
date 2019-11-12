"""
Start the dandere2x_gui_wrapper class using the .yaml. Essentially, use this if you want to
simulate d2x being started from the gui w/o having to actually use the GUI.

This is a variation of raw_config_gui_driver, but instead of only doing one file, it'll use the "input_folder" and
"output_folder" variables to upscale an entire folder.
"""

from dandere2xlib.utils.dandere2x_utils import get_operating_system
from wrappers.dandere2x_gui_wrapper import Dandere2x_Gui_Wrapper
from wrappers.dandere2x_gui_upscale_folder_wrapper import Dandere2xUpscaleFolder

from context import Context
import time
import yaml
import glob, os


def main():

    start = time.time()

    # get config based on OS
    configfile = "dandere2x_%s.yaml" % get_operating_system()

    with open(configfile, "r") as read_file:
        config = yaml.safe_load(read_file)

    upscale_folder = Dandere2xUpscaleFolder(config)
    upscale_folder.start()

    print("\n Total runtime duration:", time.time() - start)


if __name__ == "__main__":
    main()
