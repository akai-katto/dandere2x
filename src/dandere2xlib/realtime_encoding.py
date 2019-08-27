import os

from context import Context
from dandere2xlib.utils.dandere2x_utils import file_exists, get_lexicon_value, wait_on_file
from wrappers.ffmpeg.ffmpeg import create_video_from_specific_frames, concat_encoded_vids, migrate_tracks


# Delete files that come in the form filename_1, filename_2.... filename_end.
def delete_digit_files_in_range(context: Context, file_prefix, extension, lexiconic_digits, start, end):
    logger = context.logger
    logger.info("Deleting files " + file_prefix + extension + " from " + str(start) + " to " + str(end))

    for x in range(start, end):
        os.remove(file_prefix + str(get_lexicon_value(lexiconic_digits, x)) + extension)


# This function allows Dandere2x to apply filters to the Dandere2x created images while waifu2x upscales frames
# The filters dandere2x requires are really computationally heavy - having it encode during runtime allows us to reduce
# Overall runtime, since encoding all the frames after could waste a lot of time for the user.

def run_realtime_encoding(context: Context, output_file: str):
    logger = context.logger
    logger.info("Real time encoding process started")

    # Load context
    workspace = context.workspace
    frames_per_video = int(context.frame_rate * context.realtime_encoding_seconds_per_video)
    frame_count = int(context.frame_count)
    realtime_encoding_delete_files = context.realtime_encoding_delete_files
    extension_type = context.extension_type
    input_file = context.input_file

    # directories
    merged_files_prefix = context.merged_dir + "merged_"
    upscaled_files_prefix = context.upscaled_dir + "output_"
    compressed_files_prefix = context.compressed_static_dir + "compressed_"
    input_frames_prefix = context.input_frames_dir + "frame"

    # Create an encoded every frame_rate seconds.
    for x in range(0, int(frame_count / frames_per_video)):
        text_file = open(workspace + "encoded\\list.txt", 'a+')  # text file for ffmpeg to use to concat vids together
        encoded_vid = workspace + "encoded\\encoded_" + str(x) + ".mkv"

        if file_exists(encoded_vid):
            logger.info(encoded_vid + " already exists: skipping iteration")
            continue

        wait_on_file(merged_files_prefix + str(x * frames_per_video + 1) + extension_type)
        wait_on_file(merged_files_prefix + str(x * frames_per_video + frames_per_video) + extension_type)

        # create a video for frames in this section
        create_video_from_specific_frames(context, merged_files_prefix, encoded_vid, x * frames_per_video + 1,
                                          frames_per_video)

        # ensure ffmpeg video exists before deleting files
        wait_on_file(encoded_vid)

        # write to text file video for ffmpeg to concat vids with
        text_file.write("file " + "'" + encoded_vid + "'" + "\n")

        # put files to delete inside of here.
        if realtime_encoding_delete_files:
            delete_digit_files_in_range(context, merged_files_prefix, extension_type, 0, x * frames_per_video + 1,
                                        x * frames_per_video + frames_per_video + 1)

            delete_digit_files_in_range(context, compressed_files_prefix, extension_type, 0, x * frames_per_video + 1,
                                        x * frames_per_video + frames_per_video + 1)

            delete_digit_files_in_range(context, input_frames_prefix, extension_type, 0, x * frames_per_video + 1,
                                        x * frames_per_video + frames_per_video + 1)

            # upscaled files end on a different number than merged files.
            if x == int(frame_count / frames_per_video) - 1:

                wait_on_file(upscaled_files_prefix + get_lexicon_value(6, x * frames_per_video + 1) + ".png")
                wait_on_file(
                    upscaled_files_prefix + get_lexicon_value(6, x * frames_per_video + frames_per_video) + ".png")

                delete_digit_files_in_range(context,
                                            upscaled_files_prefix, ".png", 6, x * frames_per_video + 1,
                                            x * frames_per_video + frames_per_video)

            else:

                wait_on_file(upscaled_files_prefix + get_lexicon_value(6, x * frames_per_video + 1) + ".png")
                wait_on_file(
                    upscaled_files_prefix + get_lexicon_value(6, x * frames_per_video + frames_per_video + 1) + ".png")

                delete_digit_files_in_range(context,
                                            upscaled_files_prefix, ".png", 6, x * frames_per_video + 1,
                                            x * frames_per_video + frames_per_video + 1)

    # Because we divided the video into int(frame_count / frames_per_video) videos, and
    # int(frame_count / frames_per_video) != frame_count / frames_per_video, there's still frames that are left out.
    # We need to now encode those separately

    if frame_count - int(frame_count / frames_per_video) * frames_per_video > 0:
        print("got in here")
        x = int(frame_count / frames_per_video)
        encoded_vid = workspace + "encoded\\encoded_" + str(x) + ".mkv"

        wait_on_file(merged_files_prefix + str(x * frames_per_video + 1) + extension_type)
        wait_on_file(merged_files_prefix + str(frame_count - x * frames_per_video + frames_per_video) + extension_type)

        # create a video for frames in this section
        create_video_from_specific_frames(context, merged_files_prefix, encoded_vid, x * frames_per_video + 1,
                                          frames_per_video)

        # ensure ffmpeg video exists before deleting files
        wait_on_file(encoded_vid)

        # write to text file video for ffmpeg to concat vids with
        text_file.write("file " + "'" + encoded_vid + "'" + "\n")

    text_file.close()

    concat_encoded_vids(context, workspace + "nosound.mkv")
    migrate_tracks(context, workspace + "nosound.mkv", input_file, output_file)
