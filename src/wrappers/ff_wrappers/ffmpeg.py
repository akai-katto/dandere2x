#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: Dandere2X FFMmpeg
Author: CardinalPanda
Date Created: March 22, 2019
Last Modified: April 2, 2019

Description: temp ffmpeg wrapper, terrible implementation fix later
"""
import os
import subprocess

from context import Context
from dandere2x_core.dandere2x_utils import get_options_from_section


def trim_video(context: Context, output_file: str):
    trim_video_command = [context.ffmpeg_dir,
                          "-i", "[input_file]"]

    trim_video_time = get_options_from_section(context.config_json["ffmpeg"]["trim_video"]["time"])

    for element in trim_video_time:
        trim_video_command.append(element)

    trim_video_options = get_options_from_section(context.config_json["ffmpeg"]["trim_video"]["output_options"])

    for element in trim_video_options:
        trim_video_command.append(element)

    trim_video_command.append("[output_file]")

    file_dir = context.file_dir

    # replace the exec command withthe files we're concerned with
    for x in range(len(trim_video_command)):
        if trim_video_command[x] == "[input_file]":
            trim_video_command[x] = file_dir

        if trim_video_command[x] == "[output_file]":
            trim_video_command[x] = output_file

    subprocess.run(trim_video_command)


def extract_frames(context: Context):
    file_dir = context.file_dir
    input_frames_dir = context.input_frames_dir
    extension_type = context.extension_type
    output_file = input_frames_dir + "frame%01d" + extension_type

    extract_frames_command = [context.ffmpeg_dir,
                              "-i", "[input_file]"]

    extract_frames_options = get_options_from_section(
        context.config_json["ffmpeg"]["video_to_frames"]['output_options'])

    for element in extract_frames_options:
        extract_frames_command.append(element)

    extract_frames_command.extend(["[output_file]"])

    # replace the exec command withthe files we're concerned with
    for x in range(len(extract_frames_command)):
        if extract_frames_command[x] == "[input_file]":
            extract_frames_command[x] = file_dir

        if extract_frames_command[x] == "[output_file]":
            extract_frames_command[x] = output_file

    subprocess.run(extract_frames_command)


# we create about 'n' amount of videos during runtime, and we need to re-encode those videos into
# one whole video. If we don't re-encode it, we get black frames whenever two videos are spliced together,
# so the whole thing needs to be quickly re-encoded at the very end.
def concat_encoded_vids(context: Context, output_file: str):
    text_file = context.workspace + "encoded\\list.txt"
    concat_videos_command = [context.ffmpeg_dir,
                             "-f", "concat",
                             "-safe", "0",
                             "-i", "[text_file]"]

    concat_videos_option = get_options_from_section(context.config_json["ffmpeg"]["concat_videos"]['output_options'])

    for element in concat_videos_option:
        concat_videos_command.append(element)

    concat_videos_command.extend(["[output_file]"])

    for x in range(len(concat_videos_command)):
        if concat_videos_command[x] == "[text_file]":
            concat_videos_command[x] = text_file

        if concat_videos_command[x] == "[output_file]":
            concat_videos_command[x] = output_file

    subprocess.run(concat_videos_command)


# 'file_dir' refers to the file in the config file, aka the 'input_video'.

def migrate_tracks(context: Context, no_audio: str, file_dir: str, output_file: str):
    migrate_tracks_command = [context.ffmpeg_dir,
                              "-i", "[no_audio]",
                              "-i", "[video_sound]",
                              "-map", "0:v:0?",
                              "-map", "1?",
                              "-c", "copy",
                              "-map", "-1:v?"]

    migrate_tracks_options = get_options_from_section(
        context.config_json["ffmpeg"]["migrating_tracks"]['output_options'])

    for element in migrate_tracks_options:
        migrate_tracks_command.append(element)

    migrate_tracks_command.extend(["[output_file]"])

    for x in range(len(migrate_tracks_command)):
        if migrate_tracks_command[x] == "[no_audio]":
            migrate_tracks_command[x] = no_audio

        if migrate_tracks_command[x] == "[video_sound]":
            migrate_tracks_command[x] = file_dir

        if migrate_tracks_command[x] == "[output_file]":
            migrate_tracks_command[x] = str(output_file)

    print(migrate_tracks_command)

    subprocess.run(migrate_tracks_command)


# Given the file prefixes, the starting frame, and how many frames should fit in a video
# Create a short video using those values.
def create_video_from_specific_frames(context: Context, file_prefix, output_file, start_number, frames_per_video):
    video_from_frames_command = [context.ffmpeg_dir,
                                 "-start_number", "[start_number]",
                                 "-i", "[input_file]",
                                 "-vframes", "[frames_per_video]",
                                 "-r", str(context.frame_rate)]

    frame_to_video_option = get_options_from_section(context.config_json["ffmpeg"]["frames_to_video"]['output_options'])

    for element in frame_to_video_option:
        video_from_frames_command.append(element)

    video_from_frames_command.extend(["[output_file]"])
    extension_type = context.extension_type

    input_files = file_prefix + "%d" + extension_type

    # replace the exec command with the files we're concerned with
    for x in range(len(video_from_frames_command)):
        if video_from_frames_command[x] == "[input_file]":
            video_from_frames_command[x] = input_files

        if video_from_frames_command[x] == "[output_file]":
            video_from_frames_command[x] = output_file

        if video_from_frames_command[x] == "[start_number]":
            video_from_frames_command[x] = str(start_number)

        if video_from_frames_command[x] == "[frames_per_video]":
            video_from_frames_command[x] = str(frames_per_video)

    subprocess.run(video_from_frames_command)
