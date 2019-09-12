"""
Start the dandere2x_gui_wrapper class using the .json. Essentially, use this if you want to
simulate d2x being started from the gui w/o having to actually use the GUI.
"""

import json

from wrappers.dandere2x_gui_wrapper import Dandere2x_Gui_Wrapper

with open("dandere2x_win32.json", "r") as read_file:
    config_json = json.load(read_file)

d = Dandere2x_Gui_Wrapper(config_json)

d.start()
