import argparse
import sys
import time

import yaml

from dandere2xlib.utils.dandere2x_utils import get_operating_system
from gui_driver import gui_start
from wrappers.dandere2x_gui_wrapper import Dandere2x_Gui_Wrapper


def printLogs():
    print("logs!")


parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', action="store", dest="input_file", help='Input Video (no default)')
parser.add_argument('-o', '--output', action="store", dest="output_file", help='Output Video (no default)')

parser.add_argument('-b', '--block_size', action="store", dest="block_size", type=int, default=30,
                    help='Block Size (Default 30)')

args = parser.parse_args()

if len(sys.argv) == 1:
    gui_start()

else:
    start = time.time()

    # get config based on OS
    configfile = "dandere2x_%s.yaml" % get_operating_system()

    # load yaml

    with open(configfile, "r") as read_file:
        config = yaml.safe_load(read_file)

    config['dandere2x']['usersettings']['output_file'] = args.output_file
    config['dandere2x']['usersettings']['input_file'] = args.input_file
    config['dandere2x']['usersettings']['block_size'] = args.block_size

    # continue d2x
    d2x = Dandere2x_Gui_Wrapper(config)
    d2x.start()

    print("\n Total runtime duration:", time.time() - start)
