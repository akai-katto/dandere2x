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

    # get config based on OS
    configfile = os.path.abspath("dandere2x_%s.yaml" % get_operating_system())

    # load yaml

    with open(configfile, "r") as read_file:
        config = yaml.safe_load(read_file)

    c = Context(config)

    input_folder = c.input_folder
    output_folder = c.output_folder

    # for incrementing workspaces
    iter_val = 1

    for file in glob.glob(os.path.join(input_folder, "*")):
        # Create a list of every item in the input_folder

        # load the raw config file again
        with open(configfile, "r") as read_file:
            iteration_file = yaml.safe_load(read_file)

        file_name = os.path.join(input_folder, os.path.basename(file))
        output_name = os.path.join(output_folder, "upscaled_" + os.path.basename(file))

        print("workspace is " + c.workspace + str(iter_val) + os.path.sep)
        print("file name is" + file_name)
        print("output name is" + output_name)

        # change the needed variables for d2x to work, particularly, workspace is now put into workspace + iter_val
        # rather than just workspace.
        iteration_file['dandere2x']['usersettings']['input_file'] = file_name
        iteration_file['dandere2x']['usersettings']['output_file'] = output_name
        iteration_file['dandere2x']['developer_settings']['workspace'] = c.workspace + str(iter_val) + os.path.sep

        print("iter file " + iteration_file['dandere2x']['developer_settings']['workspace'])
        iter_val = iter_val + 1

        d2x = Dandere2x_Gui_Wrapper(iteration_file)
        d2x.start()


    print("\n Total runtime duration:", time.time() - start)

if __name__ == "__main__":
    main()
