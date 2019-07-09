import subprocess
import json
from fractions import Fraction


# Credit: https://github.com/k4yt3x/video2x
# Changes: Not much, just got it to work with d2x.

def get_video_info(ffprobe_dir, input_video):
    """ Gets input video information
    This method reads input video information
    using ffprobe in dictionary.
    Arguments:
        input_video {string} -- input video file path
    Returns:
        dictionary -- JSON text of input video information
    """


    # this execution command needs to be hard-coded
    # since video2x only strictly recignizes this one format
    execute = [
        ffprobe_dir,
        '-v',
        'quiet',
        '-print_format',
        'json',
        '-show_format',
        '-show_streams',
        '-i',
        input_video
    ]

    json_str = subprocess.run(execute, check=True, stdout=subprocess.PIPE).stdout

    return json.loads(json_str.decode('utf-8'))

ffprobe = "C:\\Users\\windwoz\\AppData\\Local\\video2x\\ffmpeg-latest-win64-static\\bin\\ffprobe.exe"

test = get_video_info(ffprobe, "C:\\Users\\windwoz\\Desktop\\plz\\pythonreleases\\0.9\\demo_folder\\video.mkv")

print(test)

print(test['streams'][0]['height'])

print(test['streams'][0]['tags']['DURATION'])

print(test['streams'][0]['r_frame_rate'])


print(float(Fraction(test['streams'][0]['r_frame_rate'])))