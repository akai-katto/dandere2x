"""
    This file is part of the Dandere2x project.
    Dandere2x is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    Dandere2x is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with Dandere2x.  If not, see <https://www.gnu.org/licenses/>.
""""""
========= Copyright aka_katto 2018, All rights reserved. ============
Original Author: aka_katto 
Purpose: 
 
====================================================================="""
import os
from threading import Thread
from abc import ABC, abstractmethod

from context import Context
from dandere2xlib.utils.dandere2x_utils import get_lexicon_value, wait_on_file, wait_on_file_controller


class AbstractUpscaler(Thread, ABC):

    def __init__(self, context: Context):
        super().__init__()

        # load context
        self.context = context
        self.controller = self.context.controller
        self.residual_images_dir = context.residual_images_dir
        self.residual_upscaled_dir = context.residual_upscaled_dir
        self.noise_level = context.noise_level
        self.scale_factor = context.scale_factor
        self.workspace = context.workspace
        self.frame_count = context.frame_count

        self.upscale_command = []

    def run(self) -> None:
        """
        Every upscaler essentially works like this (more or less):
        1) Continue to do the same thing until we've upscaled every frame possible.
        2) The dandere2x session was yanked.
        3) Delete upscaled files so the upscaler doesnt have to upscale them twice.

        As a result, I've abstracted this into the abstract class, so every upscaler to behave in this way
        to keep the variation of upscalers consistent across variations.
        """

        remove_thread = RemoveUpscaledFiles(context=self.context)
        remove_thread.start()

        while not self.check_if_done() and self.controller.is_alive():
            self.repeated_call()

    def check_if_done(self) -> bool:
        if self.controller.get_current_frame() >= self.frame_count - 1:
            return True

        return False

    @abstractmethod
    def upscale_file(self, input_image: str, output_image: str) -> None:
        """
        Upscale a single file using the implemented upscaling program.
        """
        pass

    @abstractmethod
    def repeated_call(self) -> None:
        """
        Every upscaler varient will continue to repeat the same call (in whatever way it was implemented)
        until Dandere2x has finished.
        """
        pass

    @abstractmethod
    def join(self, timeout=None) -> None:
        pass


class RemoveUpscaledFiles(Thread):
    def __init__(self, context):
        # threading specific
        Thread.__init__(self, name="Remove Upscale Files Thread")
        super().__init__()

        # load context
        self.start_frame = context.start_frame
        self.frame_count = context.frame_count
        self.context = context
        self.controller = self.context.controller
        self.residual_images_dir = context.residual_images_dir
        self.residual_upscaled_dir = context.residual_upscaled_dir

        # make a list of names that will eventually (past or future) be upscaled
        self.list_of_names = []
        for x in range(self.start_frame, self.frame_count):
            self.list_of_names.append("output_" + get_lexicon_value(6, x) + ".jpg")

    # todo, fix this a bit. This isn't scalable / maintainable
    def run(self) -> None:
        for x in range(len(self.list_of_names)):
            name = self.list_of_names[x]
            residual_file = self.residual_images_dir + name.replace(".png", ".jpg")
            residual_upscaled_file = self.residual_upscaled_dir + name.replace(".jpg", ".png")

            wait_on_file_controller(residual_upscaled_file, self.controller)
            if not self.controller.is_alive():
                return

            if os.path.exists(residual_file):
                os.remove(residual_file)
            else:
                pass

    def join(self, timeout=None):
        Thread.join(self, timeout)
