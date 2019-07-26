from dandere2x_gui_wrapper import Dandere2x_Gui_Wrapper
import json

with open("dandere2x.json", "r") as read_file:
    config_json = json.load(read_file)

print(config_json["dandere2x"]["realtime_encoding"])
d = Dandere2x_Gui_Wrapper(config_json)


print(d.context.realtime_encoding)

d.start()

