#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: Dandere2X FFMmpeg
Author: CardinalPanda
Date Created: March 22, 2019
Last Modified: April 2, 2019

Description: temp ffmpeg wrapper, terrible implementation fix later
"""
import subprocess
import copy
import os
from context import Context

def trim_video(context: Context, output_file: str):

    file_dir = context.file_dir
    exec = copy.copy(context.trim_video_command)
    # replace the exec command withthe files we're concerned with
    for x in range(len(exec)):
        if exec[x] == "[input_file]":
            exec[x] = file_dir

        if exec[x] == "[output_file]":
            exec[x] = output_file

    print("EXEC FOR TRIM")
    print(exec)

    subprocess.run(exec)


def extract_frames(context: Context):

    extract_frames_command = context.extract_frames_command

    file_dir = context.file_dir
    input_frames_dir = context.input_frames_dir
    extension_type = context.extension_type
    output_file = input_frames_dir + "frame%01d" + extension_type

    exec = copy.copy(context.extract_frames_command)
    # replace the exec command withthe files we're concerned with
    for x in range(len(exec)):
        if exec[x] == "[input_file]":
            exec[x] = file_dir

        if exec[x] == "[output_file]":
            exec[x] = output_file

    print("EXEC")
    print(exec)

    subprocess.run(exec)

# we create about 'n' amount of videos during runtime, and we need to re-encode those videos into
# one whole video. If we don't re-encode it, we get black frames whenever two videos are spliced together,
# so the whole thing needs to be quickly re-encoded at the very end.
def concat_encoded_vids(context: Context, output_file: str):
    text_file = context.workspace + "encoded\\list.txt"
    ffmpeg_dir = context.ffmpeg_dir

    exec = copy.copy(context.concat_videos_command)

    for x in range(len(exec)):
        if exec[x] == "[text_file]":
            exec[x] = text_file

        if exec[x] == "[output_file]":
            exec[x] = output_file

    print(exec)
    subprocess.run(exec)

# 'file_dir' refers to the file in the config file, aka the 'input_video'.

def merge_tracks(context: Context, no_audio: str, file_dir: str, output_file: str):
    exec = copy.copy(context.migrate_tracks_command)

    for x in range(len(exec)):
        if exec[x] == "[no_audio]":
            exec[x] = no_audio

        if exec[x] == "[video_sound]":
            exec[x] = file_dir

        if exec[x] == "[output_file]":
            exec[x] = str(output_file)

    print(exec)

    subprocess.run(exec, stdout=open(os.devnull, 'wb'))

# Given the file prefixes, the starting frame, and how many frames should fit in a video
# Create a short video using those values.
def create_video_from_specific_frames(context: Context, file_prefix, output_file, start_number, frames_per_video):
    ffmpeg_dir = context.ffmpeg_dir
    extension_type = context.extension_type
    frame_rate = context.frame_rate
    input_files = file_prefix + "%d" + extension_type
    exec = copy.copy(context.video_from_frames_command)

    # replace the exec command with the files we're concerned with
    for x in range(len(exec)):
        if exec[x] == "[input_file]":
            exec[x] = input_files

        if exec[x] == "[output_file]":
            exec[x] = output_file

        if exec[x] == "[start_number]":
            exec[x] = str(start_number)

        if exec[x] == "[frames_per_video]":
            exec[x] = str(frames_per_video)

    print(exec)

    subprocess.run(exec)