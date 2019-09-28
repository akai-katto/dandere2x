"""
Use this if you want to start d2x raw from the dandere2x.py driver. Doesn't delete or verify settings.
"""

from dandere2xlib.utils.dandere2x_utils import get_operating_system
from dandere2x import Dandere2x
from context import Context
import time
import yaml


def main():

    start = time.time()

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

    print("\n Total runtime duration:", time.time() - start)

if __name__ == "__main__":
    main()
