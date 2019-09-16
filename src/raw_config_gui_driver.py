"""
Start the dandere2x_gui_wrapper class using the .json. Essentially, use this if you want to
simulate d2x being started from the gui w/o having to actually use the GUI.
"""

import json

from wrappers.dandere2x_gui_wrapper import Dandere2x_Gui_Wrapper

from dandere2xlib.utils.dandere2x_utils import get_operating_system

if get_operating_system == "linux":
    configfile = "dandere2x_linux.json"
else:
    configfile = "dandere2x_win32.json"

yamlconfigfile = configfile.replace("json", "yaml")

#create object
conv = jsonyaml.jsonyaml()

#convert json to yaml
conv.convert(configfile, yamlconfigfile)

#load yaml and get its data
conv.load(yamlconfigfile)
config = conv.getdata()

#continue d2x
d = Dandere2x_Gui_Wrapper(config)

d.start()
