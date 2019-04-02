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


def extract_frames(ffmpeg_dir, time_frame, file_dir, frame_rate, duration, input_frames_dir, file_type):
    command = ffmpeg_dir + " -ss " + time_frame + " -i " + file_dir + " -r " + frame_rate + " -qscale:v 2" + \
        " -t " + duration + " " + input_frames_dir + "frame%01d" + file_type

    exec = command.split(" ")
    print(exec)
    subprocess.run(exec)


def extract_audio(ffmpeg_dir, time_frame, file_dir, audio_layer, duration, workspace, audio_type):
    command = ffmpeg_dir + " -ss " + time_frame + " -i " + file_dir + \
        " -t " + duration + " -map " + audio_layer + " " + workspace + "audio" + audio_type

    exec = command.split(" ")
    print(exec)
    subprocess.run(exec)
