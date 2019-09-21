"""
Use this if you want to start d2x raw from the dandere2x.py driver. Doesn't delete or verify settings.
"""

from dandere2xlib.utils.dandere2x_utils import get_operating_system, jsonyaml, dir_exists, wait_on_delete_dir
from dandere2x import Dandere2x
from context import Context

import shutil
import json
import time
import os


def main():
        
    start = time.time()

    # get config based on OS
    configfile = "dandere2x_%s.yaml" % get_operating_system()

    # json-yaml wrapper
    configwrapper = jsonyaml()

    # load the config and get its data
    configwrapper.load(configfile)
    config = configwrapper.getdata()

    # continue d2x
    context = Context(config)

    # delete workspace dir if it's there
    # this breaks resume_run functions but
    # they ain't working as for today. TODO.
    if dir_exists(context.workspace):
        print("Deleting old workspace")
        shutil.rmtree(context.workspace)
        wait_on_delete_dir(context.workspace)

    # make workspace dir
    try: os.mkdir(context.workspace)
    except OSError: print(("\n  Creation of workspace directory failed"
                           "\n  Permission error? exiting..")); exit(1)
        
    # starting shit
    d2x = Dandere2x(context)
    d2x.run_concurrent()

    print("\n Total runtime duration: ", time.time() - start)

if __name__ == "__main__":
    main()