import logging
from fractions import Fraction

from dandere2x.dandere2xlib.wrappers.ffmpeg.ffprobe import get_video_info, get_width_height, get_frame_rate, \
    get_aspect_ratio, get_frame_count
from dandere2x.dandere2xlib.wrappers.ffmpeg.frame_counters import get_frame_count_fast, get_frame_count_slow


class VideoSettings:

    def __init__(self, ffprobe_dir, ffmpeg_dir, video_file: str, frame_count_method: str):
        """
        A simple class to get the video settings needed for dandere2x using ffprobe.
        """

        log = logging.getLogger()
        self.ffprobe_dir = ffprobe_dir
        self.ffmpeg_dir = ffmpeg_dir
        self.settings_json = get_video_info(self.ffprobe_dir, video_file)

        if frame_count_method == "fast":
            self.frame_count = int(get_frame_count_fast(ffmpeg_dir=self.ffmpeg_dir, input_video=video_file))
        if frame_count_method == "slow":
            self.frame_count = int(get_frame_count_fast(ffmpeg_dir=self.ffmpeg_dir, input_video=video_file))

        print("setting json %s" % self.settings_json)
        # todo: This entire class can be removed and simplified into the 'except' clause,
        # but having this try / except provides me a sense of security. Some file containers
        # Won't work for the first try, and some won't work for the except, so there's double security here?
        try:
            self.height = self.settings_json['streams'][0]['height']
            self.width = self.settings_json['streams'][0]['width']
            self.frame_rate = float(Fraction(self.settings_json['streams'][0]['avg_frame_rate']))
            self.dar = self.settings_json['streams'][0]['display_aspect_ratio']

        except KeyError:
            log.warning("Warning, getting video information from ffprobe failed. Using backup commands.")
            self.width, self.height = get_width_height(self.ffprobe_dir, video_file)
            self.frame_rate = float(Fraction(get_frame_rate(self.ffprobe_dir, video_file)))
            self.dar = get_aspect_ratio(self.ffprobe_dir, video_file)

        # horizontal videos often do not include rotate so this is separated to keep up the performance
        try:
            self.rotate = int(self.settings_json['streams'][0]["tags"]["rotate"])
        except KeyError:
            self.rotate = int(0)

        log.info("Loaded Video Settings for %s :" % video_file)
        for item in self.__dict__:
            log.info("%s : %s" % (item, self.__dict__[item]))

    def log_all_variables(self):
        log = logging.getLogger()

        log.info("Context Settings:")
        for item in self.__dict__:
            print("%s : %s" % (item, self.__dict__[item]))
