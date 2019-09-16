"""
Use this if you want to start d2x raw from the dandere2x.py driver. Doesn't delete or verify settings. b
"""

import jsonyaml
import json
import time

from context import Context
from dandere2x import Dandere2x

from dandere2xlib.utils.dandere2x_utils import get_operating_system

start = time.time()


#get variables done, configfile, yamlconfigtile based on OS
if get_operating_system() == "linux":
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
context = Context(config)

d = Dandere2x(context)
d.run_concurrent()

end = time.time()

print("\n duration: " + str(time.time() - start))
