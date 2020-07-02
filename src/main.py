import argparse
import os
import shutil
import sys
import time

import yaml

from context import Context
from dandere2x import Dandere2x
from dandere2xlib.utils.dandere2x_utils import get_operating_system, wait_on_file, dir_exists, file_exists
from wrappers.dandere2x_wrappers.dandere2x_gui_upscale_folder_wrapper import Dandere2xUpscaleFolder


def load_parser():
    """
    Create a parser for dandere2x for the needed arguments
    :return:
    """

    parser = argparse.ArgumentParser()

    parser.add_argument('-b', '--block_size', action="store", dest="block_size", type=int, default=30,
                        help='Block Size (Default 30)')

    parser.add_argument('-i', '--input', action="store", dest="input_file", help='Input Video (no default)')

    parser.add_argument('-o', '--output', action="store", dest="output_file", help='Output Video (no default)')

    parser.add_argument('-q', '--quality', action="store", dest="image_quality", type=int, default=85,
                        help='Image Quality (Default 85)')

    parser.add_argument('-w', '--waifu2x_type', action="store", dest="waifu2x_type", type=str, default="vulkan",
                        help='Waifu2x Type. Options: "vulkan" "converter-cpp" "caffe". Default: "vulkan"')

    parser.add_argument('-s', '--scale_factor', action="store", dest="scale_factor", type=int, default=2,
                        help='Scale Factor (Default 2)')

    parser.add_argument('-n', '--noise_level', action="store", dest="noise_level", type=int, default=3,
                        help='Denoise Noise Level (Default 3)')

    args = parser.parse_args()
    return args


def cli_start(args):
    """
    Start Dandere2x using command line

    :param args: args loaded from load_parser()
    :return: none
    """

    # get config based on OS
    configfile = "dandere2x_%s.yaml" % get_operating_system()

    # load yaml

    with open(configfile, "r") as read_file:
        config = yaml.safe_load(read_file)

    config['dandere2x']['usersettings']['output_file'] = args.output_file
    config['dandere2x']['usersettings']['input_file'] = args.input_file

    config['dandere2x']['usersettings']['block_size'] = args.block_size
    config['dandere2x']['usersettings']['quality_minimum'] = args.image_quality
    config['dandere2x']['usersettings']['waifu2x_type'] = args.waifu2x_type
    config['dandere2x']['usersettings']['scale_factor'] = args.scale_factor
    config['dandere2x']['usersettings']['denoise_level'] = args.noise_level

    print("arg input file: " + args.input_file)
    if os.path.isdir(args.input_file):
        print("is not dir")
        if not os.path.isdir(args.output_file):
            print("input is type 'directory' but output is not type 'directory'. Dandere2x exiting")
            sys.exit(1)
        config['dandere2x']['usersettings']['input_folder'] = args.input_file
        config['dandere2x']['usersettings']['output_folder'] = args.output_file

        d2x = Dandere2xUpscaleFolder(config)
        d2x.start()

    else:
        context = Context(config)

        if dir_exists(context.workspace):
            print("Deleted Folder")

            # This is a recurring bug that seems to be popping up on other people's operating systems.
            # I'm unsure if this will fix it, but it could provide a solution for people who can't even get d2x to work.
            try:
                shutil.rmtree(context.workspace)
            except PermissionError:
                print("Trying to delete workspace via RM tree threw PermissionError - Dandere2x may not work.")

            while (file_exists(context.workspace)):
                time.sleep(1)

        d2x = Dandere2x(context)
        d2x.start()
        d2x.join()


def start_gui():
    # load in code to prevent any code from gui_driver from even being loaded, or else it loads the
    # gui driver itself

    from gui_driver import gui_start
    print("gui start called")
    gui_start()


def debug_start():
    """
    Debug function meant for dandere2x development. Starts dandere2x with minimal exterior function calls and
    will only work based off what's in the yaml.
    """
    # get config based on OS
    configfile = "dandere2x_%s.yaml" % get_operating_system()

    # load yaml

    with open(configfile, "r") as read_file:
        config = yaml.safe_load(read_file)

    # load the context with yaml stuff
    context = Context(config)

    # continue d2x
    d2x = Dandere2x(context)
    d2x.run_concurrent()


def main():
    """
    Start a Dandere2x session either through CLI or GUI. Times the session used in either case.

    :return:
    """

    args = load_parser()
    start = time.time()

    debug = False

    if debug:
        """Switch to true for debugging. Not really used otherwise."""
        debug_start()
        return
    elif len(sys.argv) == 1:
        start_gui()
    else:
        cli_start(args)

    print("Total runtime duration:", time.time() - start)


main()
