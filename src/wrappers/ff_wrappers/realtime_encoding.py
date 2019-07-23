import os
import subprocess
from dandere2x_core.dandere2x_utils import wait_on_file
from dandere2x_core.dandere2x_utils import file_exists
from dandere2x_core.dandere2x_utils import get_lexicon_value
from dandere2x_core.dandere2x_utils import get_options_from_section
from wrappers.frame import Frame
from dandere_context import Context

import copy


# Questions
# - why does merged_1 show up when resuming is called? I don't know.

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


# massive headache having to include + 1.
# delete the files using the file prefix as a format from the range start to end.
def delete_specific_merged(file_prefix, extension, lexiconic_digits, start, end):

    for x in range(start, end):
        os.remove(file_prefix + str(get_lexicon_value(lexiconic_digits, x)) + extension)


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


# we create about 'n' amount of videos during runtime, and we need to re-encode those videos into
# one whole video. If we don't re-encode it, we get black frames whenever two videos are spliced together,
# so the whole thing needs to be quickly re-encoded at the very end.
def merge_encoded_vids(context: Context,  output_file: str):

    text_file = context.workspace + "encoded\\list.txt"
    ffmpeg_dir = context.ffmpeg_dir

    merge_video_command = context.merge_video_command

    merge_video_command = merge_video_command.replace("[ffmpeg_dir]", ffmpeg_dir)
    merge_video_command = merge_video_command.replace("[text_file]", text_file)
    merge_video_command = merge_video_command.replace("[output_file]", output_file)

    exec = merge_video_command.split(" ")

    print(merge_video_command)
    print(exec)
    subprocess.run(exec)


def run_realtime_encoding(context: Context, output_file: str):
    workspace = context.workspace
    frame_rate = int(context.frame_rate)
    frame_count = int(context.frame_count)
    realtime_encoding_delete_files = context.realtime_encoding_delete_files
    extension_type = context.extension_type
    file_dir = context.file_dir

    # directories
    merged_files_prefix = context.merged_dir + "merged_"
    upscaled_files_prefix = context.upscaled_dir + "output_"
    compressed_files_prefix = context.compressed_dir + "compressed_"
    input_frames_prefix = context.input_frames_dir + "frame"

    for x in range(0, int(frame_count / frame_rate)):
        text_file = open(workspace + "encoded\\list.txt", 'a+')  # text file for ffmpeg to use to concat vids together
        encoded_vid = workspace + "encoded\\encoded_" + str(x) + ".mkv"

        if file_exists(encoded_vid):
            continue

        wait_on_file(merged_files_prefix + str(x * frame_rate + 1) + extension_type)
        wait_on_file(merged_files_prefix + str(x * frame_rate + frame_rate) + extension_type)

        # create a video for frames in this section
        create_video_from_specific_frames(context, merged_files_prefix, encoded_vid, x * frame_rate + 1, frame_rate)

        # ensure ffmpeg video exists before deleting files
        wait_on_file(encoded_vid)

        # write to text file video for ffmpeg to concat vids with
        text_file.write("file " + "'" + encoded_vid + "'" + "\n")

        # put files to delete inside of here.
        if realtime_encoding_delete_files == 1:
            delete_specific_merged(merged_files_prefix, extension_type, 0,  x * frame_rate + 1, x * frame_rate + frame_rate + 1)
            delete_specific_merged(compressed_files_prefix, extension_type, 0,  x * frame_rate + 1, x * frame_rate + frame_rate + 1)
            delete_specific_merged(input_frames_prefix, extension_type, 0, x * frame_rate + 1, x * frame_rate + frame_rate + 1)

            # upscaled files end on a different number than merged files.
            if x == int(frame_count / frame_rate) - 1:
                delete_specific_merged(
                    upscaled_files_prefix, ".png", 6, x * frame_rate + 1, x * frame_rate + frame_rate  )

            else:
                delete_specific_merged(
                    upscaled_files_prefix, ".png", 6, x * frame_rate + 1, x * frame_rate + frame_rate + 1)

    text_file.close()

    merge_encoded_vids(context, output_file)
    merge_tracks(context, output_file, file_dir, workspace + "finished.mkv")

