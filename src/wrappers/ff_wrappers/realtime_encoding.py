import os

from context import Context
from dandere2x_core.dandere2x_utils import file_exists
from dandere2x_core.dandere2x_utils import get_lexicon_value
from dandere2x_core.dandere2x_utils import wait_on_file
from wrappers.ff_wrappers.ffmpeg import create_video_from_specific_frames, concat_encoded_vids, migrate_tracks


# Questions
# - why does merged_1 show up when resuming is called? I don't know.


# massive headache having to include + 1.
# delete the files using the file prefix as a format from the range start to end.


def delete_specific_merged(file_prefix, extension, lexiconic_digits, start, end):
    for x in range(start, end):
        os.remove(file_prefix + str(get_lexicon_value(lexiconic_digits, x)) + extension)


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
            delete_specific_merged(merged_files_prefix, extension_type, 0, x * frame_rate + 1,
                                   x * frame_rate + frame_rate + 1)
            delete_specific_merged(compressed_files_prefix, extension_type, 0, x * frame_rate + 1,
                                   x * frame_rate + frame_rate + 1)
            delete_specific_merged(input_frames_prefix, extension_type, 0, x * frame_rate + 1,
                                   x * frame_rate + frame_rate + 1)

            # upscaled files end on a different number than merged files.
            if x == int(frame_count / frame_rate) - 1:
                delete_specific_merged(
                    upscaled_files_prefix, ".png", 6, x * frame_rate + 1, x * frame_rate + frame_rate)

            else:
                delete_specific_merged(
                    upscaled_files_prefix, ".png", 6, x * frame_rate + 1, x * frame_rate + frame_rate + 1)

    text_file.close()

    concat_encoded_vids(context, workspace + "nosound.mkv")
    migrate_tracks(context, workspace + "nosound.mkv", file_dir, output_file)
