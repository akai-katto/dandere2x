"""
Use this if you want to start d2x raw from the dandere2x.py driver. Doesn't delete or verify settings.
"""

import json
import time

from context import Context
from dandere2x import Dandere2x

from dandere2xlib.utils.dandere2x_utils import get_operating_system, jsonyaml, dir_exists, wait_on_delete_dir

start = time.time()

# get config based on OS
if get_operating_system() == "linux":
    configfile = "dandere2x_linux.yaml"
else:
    configfile = "dandere2x_win32.yaml"

# json-yaml wrapper
configwrapper = jsonyaml()

# load the config and get its data
configwrapper.load(configfile)
config = configwrapper.getdata()

# continue d2x
context = Context(config)

# recreate workspace dir if it's there
if dir_exists(self.context.workspace):
    print("Deleted Folder")
    shutil.rmtree(self.context.workspace)
    wait_on_delete_dir(self.context.workspace)

try:
    os.mkdir(self.context.workspace)
except OSError:
    print("\n  Creation of workspace directory failed")
    exit()
    
# starting shit
d = Dandere2x(context)
d.run_concurrent()

print("\n duration: ", time.time() - start)