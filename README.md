# Dandere2x - Faster Waifu2x Video Upscaling

## What is Dandere2x

Dandere2x is a lossy video upscaler also built around waifu2x, with video compression techniques to shorten the time required to process videos.

In other words, although lossy, dandere2x allows waifu2x to upscale videos much faster.

## Demo Video

[![Demo Video](https://img.youtube.com/vi/HW6fl1dAk7M/0.jpg)](https://www.youtube.com/watch?v=HW6fl1dAk7M)

### Requirements

- Python 3: https://www.python.org/downloads/windows/

- OpenCL compatabile system

- CUDA (Nvidia) (preferred) 

### Installation

- Download the latest release (probably from subreddit).

- Install requirements.txt (can be found inside the latest release) (can also be installed in 'install' folder in the latest release)


## Current Features

- Block Matching Video Compression
- Interpolated Frame Video Compression
- Minimum / maximum quality loss (By JPEG standards)
- Custom block sizes
- Custom scaling sizes (1x, 2x, 3x).

## FAQ

Q: What is the difference between Dandere2x and Video2x?

A: Video2x aims for quality over speed. If you're looking for the best-possible looking video, Video2x is more streamlined and provides lossless upscaling. Dandere2x, on the other hand, is still in development, is (can) much faster than video2x, but at the cost of being lossy. 


Q: How does Dandere2x work?

A: Dandere2x works by trying to recycle redundant information between frames. In anime (or cartoons in general), scenes tend to be very static, and as a result, not every part of a frame needs to be redrawn. Dandere2x identifies these blocks and reuses them to avoid unneccecary computation. 

## Related Resources

[Video2x](https://github.com/k4yt3x/video2x): A lossless video enlarger/video upscaler achieved with waifu2x.

## Legal Stuff

`Dandere2x` Copyright (C) 2018-2019
Licensed under GPLv3

## Credits

This project relies on the following software and projects.

- waifu2x-caffe
- waifu2x
- FFmpeg
- STB Image
