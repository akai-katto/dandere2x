from dandere2x_gui_wrapper import Dandere2x_Gui_Wrapper
import json

with open("dandere2x.json", "r") as read_file:
    config_json = json.load(read_file)


print(config_json['ffmpeg']['video_to_frames']['output_options']['-vf'])

print(type(config_json['ffmpeg']['video_to_frames']['output_options']['-vf']))

print(type(config_json['ffmpeg']['video_to_frames']['output_options']['-vf']) == list)

# d = Dandere2x_Gui_Wrapper(config_json)
#
# print(d.context.realtime_encoding)
#
# d.start()
# #
# #
# # # import tempfile
# # # import pathlib
# # #
# # # print()pathlib.Path(tempfile.gettempdir()) / 'dandere2x'


