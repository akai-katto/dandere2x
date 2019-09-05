import json

from wrappers.dandere2x_gui_wrapper import Dandere2x_Gui_Wrapper

with open("dandere2x_linux.json", "r") as read_file:
    config_json = json.load(read_file)

d = Dandere2x_Gui_Wrapper(config_json)

d.start()
