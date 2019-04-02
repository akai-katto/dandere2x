# Dandere2x - Faster Waifu2x Video Upscaling

## What is Dandere2x

Dandere2x is a lossy video upscaler also built around waifu2x, with video compression techniques to shorten the time required to process videos.

In another word, although lossy, dandere2x dramatically increases the video processing speed.

## Current Features

- Block Matching Video Compression
- Interpolated Frame Video Compression
- Minimum / maximum quality loss
- Custom block sizes
- Custom scaling sizes (1x, 2x, 3x).

## Development Status

Dandere2x is written natively on ubuntu Linux but is ported and released on windows. I hope to have an official Linux release soon, but for the time being the windows version is easier to configure.

The project is currently in alpha right now and is ready for testing (windows).

I highly recommend subscribing / checking reddit.com/r/dandere2x. I tend to be more active on there, as well as responding to PM's if problems come up .

## Current Releases

Latests releases are uploaded on my subreddit (at the moment).

### 0.4 Changelog (since 0.3)

- Support for OpenCL (via Waifu2x-Conveter-Cpp)
- Support for resuming Dandere2x Sessions
- Custom model type for Waifu2x-Caffe
- Entirely reworked in python
- Support for .pngs, although I do not recommend this

Reddit Link: https://www.reddit.com/r/Dandere2x/comments/b1lmeh/dandere2x_alpha_03_release/

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
