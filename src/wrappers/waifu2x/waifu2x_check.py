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
Purpose: A test script to ensure waifu2x works for the user correctly.
====================================================================="""
import os

from context import Context
from dandere2xlib.utils.dandere2x_utils import file_exists
from wrappers.frame.frame import Frame


def verify_waifu2x_works(context: Context, waifu2x):
    """
    Throws a critical error if waifu2x failed to upscale a single frame.
    """
    workspace = context.workspace
    test_file = workspace + "testframe.png"
    test_file_upscaled = workspace + "testframe_upscaled.png"

    test_frame = Frame()
    test_frame.create_new(2, 2)

    test_frame.save_image(test_file)
    waifu2x.upscale_file(test_file, test_file_upscaled)

    if not file_exists(test_file_upscaled):
        print("Waifu2x failed to upscale test file: %s" % test_file)
        print("Dandere2x will not continue, refer to the waifu2x file in %s to see what went wrong."
              % context.log_folder_dir)

        raise RuntimeError("Waifu2x failed to upscale file.")

    os.remove(test_file)
    os.remove(test_file_upscaled)
