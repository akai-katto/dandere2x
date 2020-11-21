import logging

import imageio
import numpy as np

from dandere2x.dandere2x_service_controller import Dandere2xController


class Frame:
    """
    A wrapper that wraps dandere2x related functions around the PIL / Numpy library, primarily implementing tools and
    fail safe checks that are much needed for dandere2x development.
    """

    def __init__(self, width: int, height: int, frame_name = None):
        """
        Instantiates a blank frame with bounds (height, width).

        @param width: Height of the image
        @param height: Width of the image
        @param frame_name: An optional name paramater to help with debugging.
        """
        self._frame_array: np.zeros([height, width, 3], dtype=np.uint8)
        self.__image_width: int = width
        self.__image_height: int = height

        if frame_name:
            self.frame_name = frame_name
        else:
            self.frame_name = "no frame_name set"

        self._logger = ""

    # class methods #

    @classmethod
    def from_file(cls, file_path: str):
        """
        Returns a Frame instance loading from a text file on disk.
        @param file_path: Location of the file on disk
        """

        image = cls(0, 0)
        image._frame_array = imageio.imread(file_path).astype(np.uint8)
        image.__height = image._frame_array.frame.shape[0]
        image.__width = image._frame_array.frame.shape[1]
        image.frame_name = file_path

    # todo
    @classmethod
    def from_file_wait(cls, file_path: str, controller=Dandere2xController()):
        """
        Repeatedly calls the "from_file" method until the image is properly loaded - this is a result of window's
        file handler labeling a file as ready-to-be-read but not actually, thus resulting in a string of potential
        errors.

        @param file_path: Location of the file on disk
        @param controller: Controller to revoke the wait function if the current dandere2x session is killed.
        """

        logger = logging.getLogger(__name__)
        pass


    # Getters #
    @property
    def width(self) -> int:
        return self.__image_width

    @property
    def height(self) -> int:
        return self.__image_height
