#temp ffmpeg wrapper, terrible implementation fix later
import os
import subprocess


def extract_frames(time_frame, file_dir, frame_rate, duration, workspace):
    command = "ffmpeg -ss " + time_frame + " -i " + file_dir + " -r " + frame_rate + " -qscale:v 2" + \
              " -t " + duration + " " + workspace + "inputs" + os.path.sep + "frame%01d.jpg"

    exec = command.split(" ")

    print(exec)

    subprocess.run(exec)
