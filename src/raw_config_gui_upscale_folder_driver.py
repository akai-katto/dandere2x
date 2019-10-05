"""
Start the dandere2x_gui_wrapper class using the .yaml. Essentially, use this if you want to
simulate d2x being started from the gui w/o having to actually use the GUI.

This is a variation of raw_config_gui_driver, but instead of only doing one file, it'll use the "input_folder" and
"output_folder" variables to upscale an entire folder.
"""

from dandere2xlib.utils.dandere2x_utils import get_operating_system
from wrappers.dandere2x_gui_wrapper import Dandere2x_Gui_Wrapper

from context import Context
import time
import yaml
import glob, os


def main():

    start = time.time()

    configfile = os.path.abspath("dandere2x_%s.yaml" % get_operating_system())

    # We need to make a context object to get variables needed to upscale an entire folder.
    with open(configfile, "r") as read_file:
        config = yaml.safe_load(read_file)

    c = Context(config)
    input_folder = c.input_folder
    output_folder = c.output_folder

    files_in_folder = []

    for file in glob.glob(os.path.join(input_folder, "*")):
        files_in_folder.append(os.path.basename(file))

    for x in range(len(files_in_folder)):

        with open(configfile, "r") as read_file:
            iteration_file = yaml.safe_load(read_file)

        file_name = os.path.join(input_folder, files_in_folder[x])
        output_name = os.path.join(output_folder, "upscaled_" + files_in_folder[x])

        iteration_file['dandere2x']['usersettings']['input_file'] = file_name
        iteration_file['dandere2x']['usersettings']['output_file'] = output_name
        iteration_file['dandere2x']['developer_settings']['workspace'] = c.workspace + str(x) + os.path.sep

        d2x = Dandere2x_Gui_Wrapper(iteration_file)
        d2x.start()

    print("\n Total runtime duration:", time.time() - start)


if __name__ == "__main__":
    main()
