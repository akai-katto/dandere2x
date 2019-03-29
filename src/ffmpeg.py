# temp ffmpeg wrapper, terrible implementation fix later
import os
import subprocess


def extract_frames(ffmpeg_dir, time_frame, file_dir, frame_rate, duration, workspace, file_type):
    command = ffmpeg_dir + " -ss " + time_frame + " -i " + file_dir + " -r " + frame_rate + " -qscale:v 2" + \
              " -t " + duration + " " + workspace + "inputs" + os.path.sep + "frame%01d" + file_type

    exec = command.split(" ")

    print(exec)

    subprocess.run(exec)

def extract_audio(ffmpeg_dir, time_frame, file_dir, audio_layer, duration, workspace, audio_type):
    command = ffmpeg_dir + " -ss " + time_frame + " -i " + file_dir + \
              " -t " + duration + " -map " + audio_layer + " " + workspace + "audio" + audio_type

    exec = command.split(" ")

    print(exec)

    subprocess.run(exec)
