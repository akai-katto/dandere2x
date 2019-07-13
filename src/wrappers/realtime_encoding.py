import os
import subprocess
from dandere2x_core.dandere2x_utils import wait_on_file
from dandere2x_core.dandere2x_utils import file_exists
from wrappers.frame import Frame
from context import Context


# Questions
# - why does merged_1 show up when resuming is called? I don't know.

# Given the file prefixes, the starting frame, and how many frames should fit in a video
# Create a short video using those values.
def create_video_from_specific_frames(context: Context, file_prefix, output, fpv, end):

    ffmpeg_dir = context.ffmpeg_dir
    extension_type = context.extension_type

    exec = [ffmpeg_dir,
            '-framerate',
            str(24),
            '-start_number',
            str(fpv),
            '-i',
            file_prefix + "%d" + extension_type,
            '-vframes',
            str(end),
            '-vf',
            'deband',
            output]

    print(exec)
    subprocess.run(exec)


# massive headache having to include + 1.
# delete the files using the file prefix as a format from the range start to end.
def delete_specific_merged(file_prefix, extension,  start, end):

    for x in range(start, end + 1):
        os.remove(file_prefix + str(x) + extension)


def merge_audio(context: Context,  video: str, audio: str, output: str):
    ffmpeg_dir = context.ffmpeg_dir

    exec = [ffmpeg_dir,
            "-i",
            video,
            "-i",
            audio,
            "-c",
            "copy",
            output]

    subprocess.run(exec)


# we create about 'n' amount of videos during runtime, and we need to re-encode those videos into
# one whole video. If we don't re-encode it, we get black frames whenever two videos are spliced together,
# so the whole thing needs to be quickly re-encoded at the very end.
def merge_encoded_vids(context: Context,  output_file: str):

    text_file = context.workspace + "encoded\\list.txt"
    ffmpeg_dir = context.ffmpeg_dir

    exec = [ffmpeg_dir,
            '-f',
            'concat',
            '-safe',
            str(0),
            '-i',
            text_file,
            '-c:v',
            'libx264',
            output_file]

    subprocess.run(exec)


def run_realtime_encoding(context: Context, output_file: str):
    workspace = context.workspace
    frame_rate = int(context.frame_rate)
    frame_count = int(context.frame_count)
    realtime_encoding_delete_files = context.realtime_encoding_delete_files
    audio_type = context.audio_type
    extension_type = context.extension_type
    merged_files = workspace + "merged\\merged_"

    for x in range(0, int(frame_count / frame_rate)):
        text_file = open(workspace + "encoded\\list.txt", 'a+')  # text file for ffmpeg to use to concat vids together
        encoded_vid = workspace + "encoded\\encoded_" + str(x) + ".mkv"

        if file_exists(encoded_vid):
            continue

        wait_on_file(merged_files + str(x * frame_rate + 1) + extension_type)
        wait_on_file(merged_files + str(x * frame_rate + frame_rate) + extension_type)

        # create a video for frames in this section
        create_video_from_specific_frames(context, merged_files, encoded_vid, x * frame_rate + 1, frame_rate)

        # ensure ffmpeg video exists before deleting files
        wait_on_file(encoded_vid)

        # write to text file video for ffmpeg to concat vids with
        text_file.write("file " + "'" + encoded_vid + "'" + "\n")

        if realtime_encoding_delete_files == 1:
            delete_specific_merged(merged_files, extension_type,  x * frame_rate + 1, x * frame_rate + frame_rate)

    text_file.close()

    merge_encoded_vids(context, output_file)
    merge_audio(context, output_file, workspace + "audio" + audio_type, workspace + "finished.mkv")

