import os
import re
import subprocess
from pprint import pprint

from dandere2x.dandere2xlib.utils.dandere2x_utils import get_operating_system


def get_frame_count_fast(ffmpeg_dir: str, input_video: str):
    assert get_operating_system() != "win32" or os.path.exists(ffmpeg_dir), "%s does not exist!" % ffmpeg_dir

    execute = [
        ffmpeg_dir,
        "-vsync", str(1),
        "-i", input_video,
        "-c", "copy",
        "-f", "null",
        "-"
    ]

    process = subprocess.run(execute, capture_output=True)
    stdout_as_str = process.stderr.decode("utf-8")

    regex = re.compile("frame=.{0,3}[0-9]{1,10}")
    matched_regex = regex.findall(stdout_as_str)
    assert matched_regex

    matched_regex = matched_regex[0]
    frame_count = re.compile("\d{1,10}").findall(matched_regex)[0]
    return int(frame_count)


def get_frame_count_slow(ffmpeg_dir: str, input_video: str):
    """
    Gets the total number of frames by exporting each frame as a 1x1 image, and we collect the buffer sum.
    """
    assert get_operating_system() != "win32" or os.path.exists(ffmpeg_dir), "%s does not exist!" % ffmpeg_dir

    extraction_args = [
        str(ffmpeg_dir), "-vsync", "1", "-loglevel", "panic",
        "-i", str(input_video), "-vf", "scale=1:1",  "-f", "rawvideo"
    ]
    extraction_args.extend(["-an", "-"])

    pprint(extraction_args)
    ffmpeg = subprocess.Popen(extraction_args, stdout=subprocess.PIPE)

    max_x_value = 0
    for x in range(1000000):
        max_x_value = x
        raw = ffmpeg.stdout.read(3)
        if not raw:
            break

    return max_x_value


if __name__ == "__main__":
    print(get_frame_count_fast("C:\\ffmpeg\\ffmpeg.exe", "C:\\Users\\windw0z\\Documents\\GitHub\\dandere2x\\src\\workspace\\yn_moving.mkv"))