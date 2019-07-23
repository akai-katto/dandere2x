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
from context import Context



# example extract_frames_command:
# [ffmpeg] -i [file_name] -r [frame_rate] -qscale:v 2 -vf noise=c1s=8:c0f=u [output_file]
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

