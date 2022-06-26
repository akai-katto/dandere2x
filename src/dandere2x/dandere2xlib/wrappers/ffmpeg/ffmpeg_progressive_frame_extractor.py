from copy import copy
from pprint import pprint

import imageio
import numpy
import numpy as np
import subprocess
from pathlib import Path
from numpy import shape
from PIL import Image

from dandere2x.dandere2xlib.utils.dandere2x_utils import get_a_valid_input_resolution
from dandere2x.dandere2xlib.utils.yaml_utils import get_options_from_section


class D2xFrame:
    """
    A wrapper that wraps dandere2x related functions around the PIL / Numpy library, primarily implementing tools and
    fail safe checks that are much needed for dandere2x development.
    """

    DTYPE = np.uint8

    def __init__(self, width: int, height: int,
                 frame_name: str = None,
                 frame_array: np.ndarray = None):
        """
        Instantiates a blank frame with bounds (height, width).

        @param width: Height of the image
        @param height: Width of the image
        @param frame_name: An optional name paramater to help with debugging.
        """

        self._frame_array: np.array = np.zeros([height, width, 3], dtype=D2xFrame.DTYPE)

        if frame_array is not None:
            numpy.copyto(self._frame_array, frame_array)
            del frame_array  # Read only, we copy it into a new buffer

        self.__image_width: int = width
        self.__image_height: int = height

        if frame_name:
            self.frame_name = frame_name
        else:
            self.frame_name = "no frame_name set"

        self._logger = ""

    @classmethod
    def from_file(cls, file_path: Path):
        """
        Returns a Frame instance loading from a text file on disk.
        @param file_path: Location of the file on disk
        """

        frame_array = imageio.imread(file_path).astype(np.uint8)
        if frame_array.shape[0] == 3:
            # Google-collab for some reason, for some images, has the arrays swapped for how the PIL
            # library needs them to be, so this is a workaround for switching the pixel's orders.
            frame_array = np.stack(frame_array, axis=2)

        height = frame_array.shape[0]
        width = frame_array.shape[1]

        instantiated_frame = D2xFrame(width, height)
        instantiated_frame._frame_array = frame_array

        return instantiated_frame

    @classmethod
    def from_ndarray(cls, frame_array: numpy.ndarray):

        height = frame_array.shape[0]
        width = frame_array.shape[1]

        instantiated_frame = D2xFrame(width, height)
        instantiated_frame._frame_array = frame_array

        return instantiated_frame

    def save(self, output_file: Path):

        pil_image = Image.fromarray(self._frame_array.astype(np.uint8))
        pil_image.save(output_file)


def _check_and_fix_resolution(input_file: str, block_size: int, output_options_original: dict) -> dict:
    """
    Returns a dictionary containing the output settings, taking into consideration if the video needs to be resized,
    and if it does, changes the pipe_video commands to include dar.
    """
    from dandere2x.dandere2xlib.utils.yaml_utils import load_executable_paths_yaml
    from dandere2x.dandere2xlib.wrappers.ffmpeg.ffmpeg import append_resize_filter_to_pre_process, \
        append_dar_filter_to_pipe_process
    from dandere2x.dandere2xlib.wrappers.ffmpeg.videosettings import VideoSettings
    import copy

    def valid_input_resolution(width: int, height: int, block_size: int):
        return width % block_size == 0 and height % block_size == 0

    new_output_options = copy.copy(output_options_original)

    # get meta-data from the video to do pre-processing
    ffprobe_path = load_executable_paths_yaml()['ffprobe']
    ffmpeg_path = load_executable_paths_yaml()['ffmpeg']
    video_settings = VideoSettings(ffprobe_path, ffmpeg_path, input_file)
    width, height = video_settings.width, video_settings.height

    if not valid_input_resolution(width=width, height=height, block_size=block_size):
        print("appending resize filter")
        append_resize_filter_to_pre_process(output_options=new_output_options,
                                            width=width,
                                            height=height,
                                            block_size=block_size)
        append_dar_filter_to_pipe_process(output_options=new_output_options,
                                          width=width,
                                          height=height)

    return new_output_options

class VideoFrameExtractor:
    FFMPEG_BINARY = "ffmpeg"

    def __init__(self, input_video: Path, width: int, height: int, block_size: int, output_options_original: dict):
        self.__count: int = 0
        self._width, self._height = get_a_valid_input_resolution(width, height, block_size)
        self._dtype = np.uint8
        self._block_size = block_size
        self._output_options_original = output_options_original

        extraction_args = [
            self.FFMPEG_BINARY, "-vsync", "1", "-loglevel", "panic",
            "-i", str(input_video)
        ]

        fixed_resolution = _check_and_fix_resolution(input_file=str(input_video),
                                                     block_size=block_size,
                                                     output_options_original=output_options_original)

        print("pre output options")
        options = get_options_from_section(fixed_resolution["ffmpeg"]["pre_process_video"]['output_options'],
            ffmpeg_command=True)
        for item in options:
            extraction_args.append(item)

        extraction_args.extend(["-c:v", "rawvideo", "-f", "rawvideo",
            "-pix_fmt", "rgb24", "-an", "-"])

        pprint(extraction_args)
        self.ffmpeg = subprocess.Popen(extraction_args, stdout=subprocess.PIPE)

    @property
    def current_frame(self) -> int:
        return self.__count

    def get_frame(self) -> D2xFrame:
        """Pipes the raw frames to stdout, converts the bytes to NumPy arrays of RGB data.
        This is a generator so usage is (for Frame in self._GetRawFrames(Video))"""

        raw = self.ffmpeg.stdout.read(self._width * self._height * 3)
        if not raw:
            raise IndexError

        raw = copy(raw)

        self.__count += 1
        return D2xFrame(width=self._width,
                        height=self._height,
                        frame_name=f"frame{self.__count}",
                        frame_array=np.frombuffer(raw, dtype=self._dtype).reshape((self._height, self._width, -1)))


if __name__ == "__main__":

    extractor = VideoFrameExtractor(Path("C:\\Users\\tyler\\Documents\\GitHub\\dandere2x\\src\\workspace\\yn_moving.mkv"), 1920, 1080)
    image_array = []
    for x in range(240):
        some_frame = extractor.get_frame()
        image_array.append(some_frame)
        # some_frame.save(Path(f"/home/tyler/Downloads/end/extracted/output{x}.png"))
