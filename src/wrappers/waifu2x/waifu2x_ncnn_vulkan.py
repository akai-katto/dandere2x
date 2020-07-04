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

from ..waifu2x.abstract_upscaler import AbstractUpscaler
from context import Context


class Waifu2xNCNNVulkan(Thread, AbstractUpscaler):

    def __init__(self, context: Context):
        super().__init__(context)

        self.context = context

        # implementation
