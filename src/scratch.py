import yaml

from dandere2x import Dandere2x
from dandere2xlib.utils.yaml_utils import load_executable_paths_yaml
from dandere2xlib.wrappers.ffmpeg.ffmpeg import convert_video_to_gif, convert_gif_to_video

from dandere2xlib.wrappers.ffmpeg.videosettings import VideoSettings

ffprobe = load_executable_paths_yaml()['ffprobe']

settings = VideoSettings(ffprobe_dir=ffprobe, video_file="./workspace/ffmpeg_output.gif")

print(settings.height)
print(settings.width)

with open("config_files/output_options.yaml", "r") as read_file:
    output_config = yaml.safe_load(read_file)

ffmpeg_path = load_executable_paths_yaml()['ffmpeg']

# convert_video_to_gif(ffmpeg_dir=ffmpeg_path, input_path="./workspace/konosuba.mp4",
#                      output_path="./workspace/ffmpeg_output.gif", output_options=output_config)

convert_gif_to_video(ffmpeg_dir=ffmpeg_path, input_path="./workspace/ffmpeg_output.gif",
                     output_path="./workspace/ffmpeg_output_converted.mkv", output_options=output_config)