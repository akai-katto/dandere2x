import sys
import threading
import time

from context import Context
from dandere2xlib.utils.thread_utils import CancellationToken


# todo
# This could probably be improved visually for the user.. it's not the most pleasing to look at
# Also, in a very niche case the GUI didn't catch up with the deletion of files, so it ceased updating


class Status(threading.Thread):

    def __init__(self, context: Context):
        self.context = context
        self.workspace = context.workspace
        self.extension_type = context.extension_type
        self.frame_count = context.frame_count
        self.is_alive = True
        self._is_stopped = False
        self.start_frame = 1

        # Threading Specific

        self.alive = True
        self.cancel_token = CancellationToken()
        self._stopevent = threading.Event()
        threading.Thread.__init__(self, name="StatusTHread")

    def join(self, timeout=None):
        threading.Thread.join(self, timeout)

    def kill(self):
        self.alive = False
        self.cancel_token.cancel()
        self._stopevent.set()

    def set_start_frame(self, start_frame: int):
        self.start_frame = start_frame

    def run(self):

        last_10 = [0]

        for x in range(self.start_frame, self.frame_count - 1):

            if not self.is_alive:
                break

            percent = int((x / self.frame_count) * 100)

            average = 0
            for time_count in last_10:
                average = average + time_count

            average = round(average / len(last_10), 2)

            sys.stdout.write('\r')
            sys.stdout.write("Frame: [%s] %i%%    Average of Last 10 Frames: %s sec / frame" % (x, percent, average))

            if len(last_10) == 10:
                last_10.pop(0)

            now = time.time()

            while x >= self.context.signal_merged_count and self.alive:
                time.sleep(.00001)

            later = time.time()
            difference = float(later - now)
            last_10.append(difference)

