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
Purpose: A mutable object to be passed around dandere2x, and breaks
         encapsulation. The point of this is, if we're going to break
         encapsulation by passing a super-variable around, might as well
         do it cleanly.
         
         This class goes inside of the Context class. 
====================================================================="""


class Controller:
    def __init__(self):
        self._is_alive = True
        self._current_frame = 1

    def update_frame_count(self, set_frame: int):
        self._current_frame = set_frame

    def get_current_frame(self):
        return self._current_frame

    def kill(self):
        self._is_alive = False

    def is_alive(self):
        return self._is_alive
