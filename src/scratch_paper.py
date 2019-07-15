# from wrappers.videosettings import VideoSettings
# import configparser
#
# ffprobe_dir = "C:\\Users\\windwoz\\AppData\\Local\\video2x\\ffmpeg-latest-win64-static\\bin\\ffprobe.exe"
# file_dir = "C:\\Users\\windwoz\\Desktop\\plz\\customvideos\\violetep8.mkv"
#
# video_settings = VideoSettings(ffprobe_dir, file_dir)
#
# config = configparser.ConfigParser()
# config.read("config.ini")
#
# print(config.get('dandere2x', 'workspace'))
#
# config.set('dandere2x','workspace', 'memes')
#
# print(config.get('dandere2x', 'workspace'))

import configparser
import time

from dandere2x import Dandere2x

start = time.time()

d = Dandere2x('config.ini')

config = configparser.ConfigParser()
config.read("config.ini")
d.context.init_from_config_file(config)

d.run_concurrent()

end = time.time()
