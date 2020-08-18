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

import datetime

from sty import fg


class ConsoleLogger:
    def __init__(self, log_level: int):
        self.log_file_set = False
        self.log_level = log_level
        self.file = None
        self.logfile = None

    def switch_color(self, argument):
        switcher = {
            "default": fg.cyan,
            "expected": fg.li_green,
            "unexpected": fg.li_yellow,
            "error": fg.li_red
        }
        return switcher.get(argument, "Invalid month")

    def log(self, *message, color_type="default", log_level_required=1):

        if self.log_level <= log_level_required:
            return

        color = self.switch_color(color_type)
        now = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S,%f")[:-3]
        processed_message = "[%s] " % now

        # Basically we define *message as an argument so we have to "merge" it, ' '.join(everything)
        for index, item in enumerate(message):
            if isinstance(item, list) or isinstance(item, tuple):
                processed_message += " ".join(map(str, message[index])) + " "
            else:
                processed_message += str(item) + " "

        # As we add that extra space at the end, gotta remove it
        processed_message = processed_message[:-1]
        print(color + processed_message)

        if self.log_file_set:
            try:
                with open(self.logfile, "a", encoding="utf-8") as f:
                    f.write(processed_message + "\n")
            except Exception:
                pass
