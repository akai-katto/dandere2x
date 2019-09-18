"""
Use this if you want to start d2x raw from the dandere2x.py driver. Doesn't delete or verify settings. b
"""

import json
import time

from context import Context
from dandere2x import Dandere2x

from dandere2xlib.utils.dandere2x_utils import get_operating_system, jsonyaml

start = time.time()

# get config based on OS
if get_operating_system() == "linux":
    configfile = "dandere2x_linux.yaml"
else:
    configfile = "dandere2x_win32.yaml"

# json-yaml wrapper
conv = jsonyaml()

# load the config and get its data
conv.load(configfile)
config = conv.getdata()

# continue d2x
context = Context(config)

d = Dandere2x(context)
d.run_concurrent()

print("\n duration: ", time.time() - start)
