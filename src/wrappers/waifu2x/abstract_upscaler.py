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
from threading import Thread
from abc import ABC, abstractmethod

from context import Context


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

        self.upscale_command = []

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def repeated_call(self):
        pass

    @abstractmethod
    def removed_used(self):
        pass

    @abstractmethod
    def upscale_once(self, input_image: str, output_image: str):
        pass

    @abstractmethod
    def join(self, timeout=None):
        pass
