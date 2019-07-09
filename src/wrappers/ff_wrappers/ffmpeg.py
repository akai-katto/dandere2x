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


def extract_frames(context: Context):
    ffmpeg_dir = context.ffmpeg_dir
    time_frame = context.time_frame
    file_dir = context.file_dir
    frame_rate = context.frame_rate
    duration = context.duration
    input_frames_dir = context.input_frames_dir
    extension_type = context.extension_type


    exec = [ffmpeg_dir,
               "-ss",
               time_frame,
               "-i",
               file_dir,
               "-r",
               str(frame_rate),
               "-qscale:v",
               str(2),
               "-t",
               str(duration),
               "-vf",
               "noise=c1s=8:c0f=u",
               input_frames_dir + "frame%01d" + extension_type]


    print(exec)
    subprocess.run(exec)


def extract_audio(context: Context):
    ffmpeg_dir = context.ffmpeg_dir
    time_frame = context.time_frame
    file_dir = context.file_dir
    workspace = context.workspace
    duration = context.duration
    audio_layer = context.audio_layer
    audio_type = context.audio_type

    command = ffmpeg_dir + " -ss " + time_frame + " -i " + file_dir + \
              " -t " + duration + " -map " + audio_layer + " " + workspace + "audio" + audio_type

    exec = command.split(" ")
    print(exec)
    subprocess.run(exec)
