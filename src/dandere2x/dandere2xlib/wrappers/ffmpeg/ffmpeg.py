import logging
import os
import subprocess
import sys

from dandere2x.dandere2xlib.utils.dandere2x_utils import get_a_valid_input_resolution, get_operating_system
from dandere2x.dandere2xlib.utils.yaml_utils import get_options_from_section
from dandere2x.dandere2xlib.wrappers.ffmpeg.ffprobe import get_seconds
from dandere2x.dandere2xlib.wrappers.ffmpeg.videosettings import VideoSettings


def re_encode_video(ffmpeg_dir: str, ffprobe_dir: str, output_options: dict, input_file: str,
                    output_file: str, console_output=None) -> None:
    """
    #todo
    """

    if console_output:
        assert type(console_output) == str

    logger = logging.getLogger("root")
    video_settings = VideoSettings(ffprobe_dir=ffprobe_dir, video_file=input_file)
    frame_rate = video_settings.frame_rate

    extract_frames_command = [ffmpeg_dir]

    hw_accel = output_options["ffmpeg"]["pre_process_video"]["-hwaccel"]
    if hw_accel is not None:
        extract_frames_command.append("-hwaccel")
        extract_frames_command.append(hw_accel)

    extract_frames_command.extend(["-i", input_file])

    extract_frames_options = \
        get_options_from_section(output_options["ffmpeg"]['pre_process_video']['output_options'],
                                 ffmpeg_command=True)

    for element in extract_frames_options:
        extract_frames_command.append(element)

    extract_frames_command.append("-r")
    extract_frames_command.append(str(frame_rate))
    extract_frames_command.extend([output_file])

    logger.warning("Re-encoding your video, this may take some time.")
    process = subprocess.Popen(extract_frames_command, stdout=sys.stdout, stderr=sys.stdout,
                               stdin=subprocess.PIPE, shell=False)

    stdout, stderr = process.communicate()


def convert_video_to_gif(ffmpeg_dir: str, input_path: str, output_path: str, output_options=None) -> None:
    assert get_operating_system() != "win32" or os.path.exists(ffmpeg_dir), \
        "%s does not exist" % ffmpeg_dir

    execute = [
        ffmpeg_dir,
        "-i", input_path,
    ]

    options = get_options_from_section(output_options["ffmpeg"]['convert_video_to_gif']['output_options'],
                                       ffmpeg_command=True)

    for item in options:
        execute.append(item)

    execute.append(output_path)

    print(execute)
    process = subprocess.Popen(execute, stdout=open(os.devnull, 'w'), stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE, shell=False)

    stdout, stderr = process.communicate()


def convert_gif_to_video(ffmpeg_dir: str, input_path: str, output_path: str, output_options=None) -> None:
    assert get_operating_system() != "win32" or os.path.exists(ffmpeg_dir), \
        "%s does not exist" % ffmpeg_dir

    execute = [
        ffmpeg_dir,
        "-i", input_path,
    ]

    options = get_options_from_section(output_options["ffmpeg"]['convert_video_to_gif']['output_options'],
                                       ffmpeg_command=True)

    for item in options:
        execute.append(item)

    execute.append(output_path)

    print(execute)
    process = subprocess.Popen(execute, stdout=open(os.devnull, 'w'), stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE, shell=False)

    stdout, stderr = process.communicate()


def is_file_video(ffprobe_dir: str, input_video: str):
    assert get_operating_system() != "win32" or os.path.exists(ffprobe_dir), "%s does not exist!" % ffprobe_dir

    execute = [
        ffprobe_dir,
        "-i", input_video,
        "-v", "quiet"
    ]

    return_bytes = subprocess.run(execute, check=True, stdout=subprocess.PIPE).stdout

    if "Invalid data found when processing input" in return_bytes.decode("utf-8"):
        return False

    return True


def append_resize_filter_to_pre_process(output_options: dict, width: int, height: int, block_size: int) -> None:
    """

    Args:
        output_options: Dictionary containing the loaded ./config_files/output_options.yaml
        width: Video Width
        height: Video Height
        block_size: Dandere2x Blocksize

    Returns:
        Nothing, but output_options is modified to containing video filters to resize the pre_processed video
        to be compatible with the block size.
    """

    log = logging.getLogger()
    width, height = get_a_valid_input_resolution(width, height, block_size)

    log.info("Dandere2x is resizing the video in order to make the resolution compatible with your settings... ")
    log.info("New width -> %s " % str(width))
    log.info("New height -> %s " % str(height))

    output_options['ffmpeg']['pre_process_video']['output_options']['-vf'] \
        .append("scale=" + str(width) + ":" + str(height))


def append_dar_filter_to_pipe_process(output_options: dict, width: int, height: int) -> None:
    """

    Args:
        output_options: Dictionary containing the loaded ./config_files/output_options.yaml
        width: Desired width
        height: Desired height

    Returns:
        Nothing, but output_option's pipe commands will resize the pipe'd video using the setdar filter.
    """

    # reduce width and height down
    from fractions import Fraction
    frac = Fraction(width, height)
    frac_str = str(frac.numerator) + "/" + str(frac.denominator)

    output_options['ffmpeg']['pipe_video']['output_options']['-vf'].append("setdar=" + frac_str)


def divide_and_reencode_video(ffmpeg_path: str, ffprobe_path: str,
                              input_video: str, output_options: dict,
                              divide: int, output_dir: str):
    """
    
    Attempts to divide a video into N different segments, using the ffmpeg segment_time argument. See the reading
    I referenced here: 
        https://superuser.com/questions/692714/how-to-split-videos-with-ffmpeg-and-segment-times-option
    
    Note that this will not perfectly divide the video into N different, equally sized chunks, but rather will cut them
    where keyframes allow them to be split. 

    Args:
        ffmpeg_path: ffmpeg binary
        ffprobe_path: ffprobe binary
        input_video: File to be split
        output_options: Dictionary containing the loaded ./config_files/output_options.yaml
        divide: N divisions.
        output_dir: Where to save split_video%d.mkv's. 

    Returns:
        Nothing, but split_video%d.mkv files will appear in output_dir.
    """
    import math

    seconds = int(get_seconds(ffprobe_dir=ffprobe_path, input_video=input_video))
    ratio = math.ceil(seconds / divide)
    frame_rate = VideoSettings(ffprobe_dir=ffprobe_path, video_file=input_video).frame_rate

    execute = [ffmpeg_path,
               "-i", input_video,
               "-f", "segment",
               "-segment_time", str(ratio),
               "-r", str(frame_rate)]

    options = get_options_from_section(output_options["ffmpeg"]['pre_process_video']['output_options'],
                                       ffmpeg_command=True)

    for element in options:
        execute.append(element)

    execute.append(os.path.join(output_dir, "split_video%d.mkv"))

    return_bytes = subprocess.run(execute, check=True, stdout=subprocess.PIPE).stdout
    return_string = return_bytes.decode("utf-8")

    return return_string


def get_console_output(method_name: str, console_output_dir=None):
    if console_output_dir:
        assert type(console_output_dir) == str

        log_file = os.path.join(console_output_dir, method_name + "output.txt")
        console_output = open(log_file, "w", encoding="utf8")
        return console_output

    return open(os.devnull, 'w')


def concat_n_videos(ffmpeg_dir: str, temp_file_dir: str, console_output_dir: str, list_of_files: list,
                    output_file: str) -> None:
    import subprocess

    file_list_text_file = os.path.join(temp_file_dir, "temp.txt")

    file_template = "file " + "'" + "%s" + "'" + "\n"

    # we need to create a text file for ffmpeg's concat function to work properly.
    file = open(file_list_text_file, "a")
    for file_name in list_of_files:
        file.write(file_template % file_name)
    file.close()

    concat_videos_command = [ffmpeg_dir,
                             "-f", "concat",
                             "-safe", "0",
                             "-i", file_list_text_file]

    concat_videos_command.extend([output_file])

    console_output = get_console_output(__name__, console_output_dir)
    subprocess.call(concat_videos_command, shell=False, stderr=console_output, stdout=console_output)


def migrate_tracks_contextless(ffmpeg_dir: str, no_audio: str, file_dir: str, output_file: str,
                               output_options: dict,
                               console_output_dir=None):
    """
    Add the audio tracks from the original video to the output video.
    """

    log = logging.getLogger("root")

    # to remove
    def convert(lst):
        return ' '.join(lst)

    log = logging.getLogger()

    migrate_tracks_command = [ffmpeg_dir,
                              "-i", no_audio,
                              "-i", file_dir,
                              "-map", "0:v?",
                              "-map", "1:a?",
                              "-map", "1:s?",
                              "-map", "1:d?",
                              "-map", "1:t?"
                              ]

    options = get_options_from_section(output_options["ffmpeg"]['migrate_audio']['output_options'],
                                       ffmpeg_command=True)

    for element in options:
        migrate_tracks_command.append(element)

    migrate_tracks_command.extend([str(output_file)])

    log.info("Migrating tracks %s " % convert(migrate_tracks_command))

    console_output = get_console_output(__name__, console_output_dir)

    log.info("Writing files to %s" % str(console_output_dir))
    log.info("Migrate Command: %s" % convert(migrate_tracks_command))
    subprocess.call(migrate_tracks_command, shell=False, stderr=console_output, stdout=console_output)
    log.info("Finished migrating to file: %s" % output_file)
