from wrappers.ffprobe import get_video_info
from fractions import Fraction
import datetime

# my function to just have a callable object to have the video information we need

class VideoSettings:

    def __init__(self, ffprobe_dir, video_file: str):

        self.ffprobe_dir = ffprobe_dir
        self.settings_json = get_video_info(self.ffprobe_dir, video_file)

        print(self.settings_json)

        self.height = self.settings_json['streams'][0]['height']
        self.width = self.settings_json['streams'][0]['width']
        self.duration = str(datetime.timedelta(self.settings_json['streams'][0]['duration_ts']))
        self.frame_rate = float(Fraction(self.settings_json['streams'][0]['r_frame_rate']))

