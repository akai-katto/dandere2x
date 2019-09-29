from context import Context
from wrappers.cv2.progress_frame_extractor_cv2 import ProgressiveFramesExtractorCV2
import time
import subprocess


# TODO
# Find a solution an actual solution to apply these filters to CV2 images w/o having to use ffmpeg
# to extract another video.
def ffmpeg_filters_workaround(context: Context):
    # applies core d2x filters to the input video, FORCES using cv2 to extract the frames
    # and sets the output noisy video as the input for future

    extractfunc = "cv2"
    original_video = context.input_file

    noisy_video = context.workspace + "noisy.mkv"

    print("\n    PFE WORKAROUND: APPLY FILTERS BEFORE STARTED")

    start = time.time()

    subprocess.run([ context.ffmpeg_dir, '-i', original_video,
                    '-loglevel', 'panic',
                    '-threads', '4',
                    '-qscale:v:', '2',
                    '-vf', 'noise=c1s=8:c0f=u', noisy_video])

    print("  PFE WORKAROUND: TOOK:", round(time.time() - start, 2))

    context.input_file = noisy_video

    return context.input_file

class MinDiskUsage:

    def __init__(self, context: Context):

        self.context = context
        self.frame_count = context.frame_count
        self.progressive_frame_extractor = ProgressiveFramesExtractorCV2(self.context)

    def run(self):

        print("running inside min disk usage")

        for x in range(1, self.frame_count - 1):

            # wait for signal to get ahead of MinDiskUsage
            while x >= self.context.signal_merged_count:
                time.sleep(.00001)

            # when it does get ahead, extract the next frame
            self.progressive_frame_extractor.next_frame()

    def extract_initial_frames(self):
        """
        Extract 'max_frames_ahead' initial frames to start out with.
        """
        max_frames_ahead = self.context.max_frames_ahead

        for x in range(max_frames_ahead):
            self.progressive_frame_extractor.next_frame()


