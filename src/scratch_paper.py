from dandere2x_gui_wrapper import Dandere2x_Gui_Wrapper
import json

from dandere2xlib.utils.json_utils import get_options_from_section

from dandere2xlib.utils.json_utils import list_to_string
from dandere2xlib.utils.dandere2x_utils import valid_input_resolution, get_a_valid_input_resolution



with open("dandere2x.json", "r") as read_file:
    config_json = json.load(read_file)


d = Dandere2x_Gui_Wrapper(config_json)

print(d.context.realtime_encoding)

d.start()
# # #
# # #
# # # # import tempfile
# # # # import pathlib
# # # #
# # # # print()pathlib.Path(tempfile.gettempdir()) / 'dandere2x'
#
#

from wrappers.frame import Frame


f1 = Frame()

f1.load_from_string("C:\\Users\\windwoz\\Documents\\github_projects\\src\\workspace\\15_seconds_round_up\\inputs\\frame1.jpg")

f1.save_image("C:\\Users\\windwoz\\Documents\\github_projects\\src\\workspace\\15_seconds_round_up\\inputs\\temp.jpg")