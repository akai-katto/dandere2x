# Dandere2x - Faster Waifu2x Video Upscaling

## What is Dandere2x

Dandere2x is a lossy video upscaler also built around waifu2x, with video compression techniques to shorten the time required to process videos.

In other words, although lossy, dandere2x dramatically reduces the time needed to upscale most anime videos. 

## What does Dandere2x Do?

Dandere2x seeks to reduce the time needed to upscale videos.

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
