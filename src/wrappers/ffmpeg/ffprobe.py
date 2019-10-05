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


def get_width_height(ffprobe_dir, input_video):
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
        'error',
        '-select_streams',
        'v:0',
        '-show_entries',
        'stream=width,height',
        '-of',
        'csv=p=0',
        input_video
    ]

    return_bytes = subprocess.run(execute, check=True, stdout=subprocess.PIPE).stdout
    return_string = return_bytes.decode("utf-8").split(",")

    return int(return_string[0]), int(return_string[1])


def get_frame_rate(ffprobe_dir, input_video):
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
        'error',
        '-select_streams',
        'v:0',
        '-show_entries',
        'stream=r_frame_rate',
        '-of',
        'csv=p=0',
        input_video
    ]

    return_bytes = subprocess.run(execute, check=True, stdout=subprocess.PIPE).stdout
    return_string = return_bytes.decode("utf-8")

    return return_string


def get_frame_count(ffprobe_dir, input_video):
    # this execution command needs to be hard-coded
    # since video2x only strictly recignizes this one format
    execute = [
        ffprobe_dir,
        '-v',
        'error',
        '-count_frames',
        '-select_streams',
        'v:0',
        '-show_entries',
        'stream=nb_read_frames ',
        '-of',
        'csv=p=0',
        input_video
    ]

    return_bytes = subprocess.run(execute, check=True, stdout=subprocess.PIPE).stdout
    return_string = return_bytes.decode("utf-8")

    return return_string
