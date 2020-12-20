import argparse
import os
import shutil
import sys
import time

import yaml
from dandere2x.context import Context
from wrappers.dandere2x_wrappers.dandere2x_gui_upscale_folder_wrapper import Dandere2xUpscaleFolder

from dandere2x.dandere2x_service.__init__ import Dandere2xServiceThread
from dandere2xlib.utils.dandere2x_utils import get_operating_system, dir_exists, file_exists


def create_parser():
    """
    Create a parser for dandere2x for the needed arguments.
    :return: ArgsParse for dandere2x.
    """

    parser = argparse.ArgumentParser()

    parser.add_argument('-b', '--block_size', action="store", dest="block_size", type=int, default=30,
                        help='Block Size (Default 30)')

    parser.add_argument('-i', '--input', action="store", dest="input_file", help='Input Video (no default)')

    parser.add_argument('-o', '--output', action="store", dest="output_file", help='Output Video (no default)')

    parser.add_argument('-q', '--quality', action="store", dest="image_quality", type=int, default=95,
                        help='Image Quality (Default 95)')

    parser.add_argument('-w', '--waifu2x_type', action="store", dest="waifu2x_type", type=str, default="vulkan",
                        help='Waifu2x Type. Options: "vulkan" "converter-cpp" "caffe". Default: "vulkan"')

    parser.add_argument('-s', '--scale_factor', action="store", dest="scale_factor", type=int, default=2,
                        help='Scale Factor (Default 2)')

    parser.add_argument('-n', '--noise_level', action="store", dest="noise_level", type=int, default=3,
                        help='Denoise Noise Level (Default 3)')

    args = parser.parse_args()
    return args


def cli_start():
    """
    Start Dandere2x using command line. Parse the user arguments and run dandere2x in

    :return: none
    """

    # get config based on OS
    configfile = "dandere2x_%s.yaml" % get_operating_system()

    # load yaml

    with open(configfile, "r") as read_file:
        config = yaml.safe_load(read_file)

    args = create_parser()  # Get the parser specific to dandere2x
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

        d2x = Dandere2xServiceThread(context)
        d2x.start()
        d2x.join()


def start_gui():
    """ Start the dandere2x GUI. We load gui_start inline here, because on import gui_driver gets called and made. """
    from dandere2xlib.wrappers.gui_driver import gui_start

    print("Calling GUI start.")
    gui_start()


def main():
    """ Start a Dandere2x session either through CLI or GUI. In either event, the total runtime is printed. """

    start = time.time()

    if len(sys.argv) == 1:
        start_gui()
    else:
        cli_start()

    print("Total runtime duration:", time.time() - start)


main()
