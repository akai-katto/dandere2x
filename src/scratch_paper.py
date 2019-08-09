from dandere2x_gui_wrapper import Dandere2x_Gui_Wrapper
import json

from dandere2xlib.utils.json_utils import get_options_from_section

from dandere2xlib.utils.json_utils import list_to_string

with open("dandere2x.json", "r") as read_file:
    config_json = json.load(read_file)


print(config_json['ffmpeg']['video_to_frames']['output_options']['-vf'])

print(type(config_json['ffmpeg']['video_to_frames']['output_options']['-vf']))

print(type(config_json['ffmpeg']['video_to_frames']['output_options']['-vf']) == list)

print(list_to_string(config_json['ffmpeg']['video_to_frames']['output_options']['-vf']))


print(get_options_from_section(config_json['ffmpeg']['video_to_frames']['output_options'], ffmpeg_command=True))

d = Dandere2x_Gui_Wrapper(config_json)

print(d.context.realtime_encoding)

d.start()
# #
# #
# # # import tempfile
# # # import pathlib
# # #
# # # print()pathlib.Path(tempfile.gettempdir()) / 'dandere2x'


