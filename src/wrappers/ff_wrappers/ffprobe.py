import json
import subprocess


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
