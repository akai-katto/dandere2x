"""
Start the dandere2x_gui_wrapper class using the .json. Essentially, use this if you want to
simulate d2x being started from the gui w/o having to actually use the GUI.
"""

import time

from wrappers.dandere2x_gui_wrapper import Dandere2x_Gui_Wrapper
from dandere2xlib.utils.dandere2x_utils import get_operating_system, jsonyaml

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

#continue d2x
d = Dandere2x_Gui_Wrapper(config)
d.start()

print("\n duration: ", time.time() - start)
