import logging

import cv2


class VideoSettingsCV2:

    def __init__(self, video_file: str):
        """A class to get the meta-data needed for Dandere2x to work. """

        cap = cv2.VideoCapture(video_file)
        self.height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.frame_rate = cap.get(cv2.CAP_PROP_FPS)
