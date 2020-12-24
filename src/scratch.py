from dandere2x.dandere2xlib.utils.yaml_utils import load_executable_paths_yaml
from dandere2x.dandere2xlib.wrappers.ffmpeg.videosettings import VideoSettings

ffprobe_path = load_executable_paths_yaml()['ffprobe']
ffmpeg_path = load_executable_paths_yaml()['ffmpeg']


video = VideoSettings(ffprobe_dir=ffprobe_path, video_file="./workspace/gui/outputvid1.mkv")

print(video.frame_rate)