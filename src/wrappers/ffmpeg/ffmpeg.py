#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import subprocess

from context import Context
from dandere2xlib.utils.yaml_utils import get_options_from_section


def trim_video(context: Context, output_file: str):
    """
    Create a trimmed video using -ss and -to commands from FFMPEG. The trimmed video will be named 'output_file'
    """
    # load context

    input_file = context.input_file

    trim_video_command = [context.ffmpeg_dir,
                          "-hwaccel", context.hwaccel,
                          "-i", input_file]

    trim_video_time = get_options_from_section(context.config_yaml["ffmpeg"]["trim_video"]["time"])

    for element in trim_video_time:
        trim_video_command.append(element)

    trim_video_options = \
        get_options_from_section(context.config_yaml["ffmpeg"]["trim_video"]["output_options"], ffmpeg_command=True)

    for element in trim_video_options:
        trim_video_command.append(element)

    trim_video_command.append(output_file)

    console_output = open(context.log_dir + "ffmpeg_trim_video_command.txt", "w")
    console_output.write(str(trim_video_command))
    subprocess.call(trim_video_command, shell=False, stderr=console_output, stdout=console_output)


def extract_frames(context: Context, input_file: str):
    """
    Extract frames from a video using ffmpeg.
    """
    input_frames_dir = context.input_frames_dir
    extension_type = context.extension_type
    output_file = input_frames_dir + "frame%01d" + extension_type
    logger = logging.getLogger(__name__)
    frame_rate = context.frame_rate

    extract_frames_command = [context.ffmpeg_dir,
                              "-hwaccel", context.hwaccel,
                              "-i", input_file]

    extract_frames_options = \
        get_options_from_section(context.config_yaml["ffmpeg"]["video_to_frames"]['output_options'],
                                 ffmpeg_command=True)

    for element in extract_frames_options:
        extract_frames_command.append(element)

    extract_frames_command.append("-r")
    extract_frames_command.append(str(frame_rate))

    extract_frames_command.extend([output_file])

    logger.info("extracting frames")

    console_output = open(context.log_dir + "ffmpeg_extract_frames_console.txt", "w")
    console_output.write(str(extract_frames_command))
    subprocess.call(extract_frames_command, shell=False, stderr=console_output, stdout=console_output)


def create_video_from_extract_frames(context: Context, output_file: str):
    """
    Create a new video by applying the filters that d2x needs to work into it's own seperate video.
    """
    input_file = context.input_file
    logger = logging.getLogger(__name__)

    command = [context.ffmpeg_dir,
                              "-hwaccel", context.hwaccel,
                              "-i", input_file]

    extract_frames_options = \
        get_options_from_section(context.config_yaml["ffmpeg"]["video_to_frames"]['output_options'],
                                 ffmpeg_command=True)

    for element in extract_frames_options:
        command.append(element)

    command.extend([output_file])

    logger.info("Applying filter to video...")

    console_output = open(context.log_dir + "ffmpeg_create_video_from_extract_frame_filters.txt", "w")
    console_output.write(str(command))
    subprocess.call(command, shell=False, stderr=console_output, stdout=console_output)


def concat_encoded_vids(context: Context, output_file: str):
    """
    Concatonate a video using 2) in this stackoverflow post.
    https://stackoverflow.com/questions/7333232/how-to-concatenate-two-mp4-files-using-ffmpeg

    The 'list.txt' should already exist, as it's produced in realtime_encoding.py
    """

    encoded_dir = context.encoded_dir

    text_file = encoded_dir + "list.txt"
    concat_videos_command = [context.ffmpeg_dir,
                             "-f", "concat",
                             "-safe", "0",
                             "-hwaccel", context.hwaccel,
                             "-i", text_file]

    concat_videos_option = \
        get_options_from_section(context.config_yaml["ffmpeg"]["concat_videos"]['output_options'], ffmpeg_command=True)

    for element in concat_videos_option:
        concat_videos_command.append(element)

    concat_videos_command.extend([output_file])

    console_output = open(context.log_dir + "ffmpeg_concat_videos_command.txt", "w")
    console_output.write((str(concat_videos_command)))
    subprocess.call(concat_videos_command, shell=False, stderr=console_output, stdout=console_output)


def migrate_tracks(context: Context, no_audio: str, file_dir: str, output_file: str):
    """
    Add the audio tracks from the original video to the output video.
    """
    migrate_tracks_command = [context.ffmpeg_dir,
                              "-i", no_audio,
                              "-i", file_dir,
                              "-map", "0:v:0?",
                              "-map", "1?",
                              "-c", "copy",
                              "-map", "-1:v?"]

    migrate_tracks_options = \
        get_options_from_section(context.config_yaml["ffmpeg"]["migrating_tracks"]['output_options'],
                                 ffmpeg_command=True)

    for element in migrate_tracks_options:
        migrate_tracks_command.append(element)

    migrate_tracks_command.extend([str(output_file)])

    console_output = open(context.log_dir + "migrate_tracks_command.txt", "w")
    console_output.write(str(migrate_tracks_command))
    subprocess.call(migrate_tracks_command, shell=False, stderr=console_output, stdout=console_output)


def create_video_from_specific_frames(context: Context, file_prefix, output_file, start_number, frames_per_video):
    """
    Create a video using the 'start_number' ffmpeg flag and the 'vframes' input flag to create a video
    using frames for a range of output images.
    """

    # load context
    logger = context.logger
    extension_type = context.extension_type
    input_files = file_prefix + "%d" + extension_type

    video_from_frames_command = [context.ffmpeg_dir,
                                 "-start_number", str(start_number),
                                 "-hwaccel", context.hwaccel,
                                 "-framerate", str(context.frame_rate),
                                 "-i", input_files,
                                 "-vframes", str(frames_per_video),
                                 "-r", str(context.frame_rate)]

    frame_to_video_option = get_options_from_section(context.config_yaml["ffmpeg"]["frames_to_video"]['output_options']
                                                     , ffmpeg_command=True)

    for element in frame_to_video_option:
        video_from_frames_command.append(element)

    video_from_frames_command.extend([output_file])

    logger.info("running ffmpeg command: " + str(video_from_frames_command))

    console_output = open(context.log_dir + "video_from_frames_command.txt", "w")
    console_output.write(str(video_from_frames_command))
    subprocess.call(video_from_frames_command, shell=False, stderr=console_output, stdout=console_output)
