from dandere2x_gui_wrapper import Dandere2x_Gui_Wrapper
import json

with open("dandere2x.json", "r") as read_file:
    config_json = json.load(read_file)

d = Dandere2x_Gui_Wrapper(config_json)

d.start()

