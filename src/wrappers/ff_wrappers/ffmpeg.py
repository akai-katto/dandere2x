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

from context import Context


# example extract_frames_command:
# [ffmpeg] -i [file_name] -r [frame_rate] -qscale:v 2 -vf noise=c1s=8:c0f=u [output_file]
def extract_frames(context: Context):

    extract_frames_command = context.extract_frames_command
    ffmpeg_dir = context.ffmpeg_dir
    file_dir = context.file_dir
    input_frames_dir = context.input_frames_dir
    extension_type = context.extension_type
    output_file = input_frames_dir + "frame%01d" + extension_type

    extract_frames_command = extract_frames_command.replace("[ffmpeg_dir]", ffmpeg_dir)
    extract_frames_command = extract_frames_command.replace("[file_name]", file_dir)
    extract_frames_command = extract_frames_command.replace("[output_file]", output_file)

    exec = extract_frames_command.split(" ")

    subprocess.run(exec)


def extract_audio(context: Context):
    ffmpeg_dir = context.ffmpeg_dir
    file_dir = context.file_dir
    workspace = context.workspace
    audio_layer = context.audio_layer
    audio_type = context.audio_type

    output_file = workspace + "audio" + audio_type

    extract_audio_command = context.extract_audio_command

    extract_audio_command = extract_audio_command.replace("[ffmpeg_dir]", ffmpeg_dir)
    extract_audio_command = extract_audio_command.replace("[file_dir]", file_dir)
    extract_audio_command = extract_audio_command.replace("[audio_layer]", audio_layer)
    extract_audio_command = extract_audio_command.replace("[audio_type]", audio_type)
    extract_audio_command = extract_audio_command.replace("[output_file]", output_file)
    exec = extract_audio_command.split(" ")
    print(exec)
    subprocess.run(exec)
