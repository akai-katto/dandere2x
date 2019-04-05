# Dandere2x - Faster Waifu2x Video Upscaling

## What is Dandere2x

Dandere2x is a lossy video upscaler also built around waifu2x, with video compression techniques to shorten the time required to process videos.

In other words, although lossy, dandere2x dramatically increases the video processing speed.

## Current Features

- Block Matching Video Compression
- Interpolated Frame Video Compression
- Minimum / maximum quality loss
- Custom block sizes
- Custom scaling sizes (1x, 2x, 3x).

## Development Status

Dandere2x is written natively on Ubuntu Linux but is ported and released on windows. I hope to have an official Linux release soon, but for the time being the windows version is easier to configure.

The project is currently in alpha right now and is ready for testing (windows).

I highly recommend subscribing/checking reddit.com/r/dandere2x. I tend to be more active on there, as well as responding to PM's if problems come up.

## Current Releases

Latest releases are uploaded on my subreddit (at the moment).

### 0.4 Changelog (since 0.3)

- Support for OpenCL (via Waifu2x-Converter-Cpp)
- Support for resuming Dandere2x Sessions
- Custom model type for Waifu2x-Caffe
- Entirely reworked in python
- Support for .pngs, although I do not recommend this

Reddit Link: https://www.reddit.com/r/Dandere2x/comments/b1lmeh/dandere2x_alpha_03_release/


### Requirements

- Python 3: https://www.python.org/downloads/windows/

### Installation

- Download the latest release (probably from subreddit).

- Install requirements.txt (can be found inside the latest release).


## Usage

Dandere2x changes every week so I don't have a streamlined user experience setup. However, it's still usable
for the general masses. 

I'm aware that the experience is not very user-friendly at the moment. 

1) Run new.bat

2) Let Dandere2x run 

3) After Dandere2x is finished, run the commands in the 'commands.txt' folder (found in demo_folder\workspace\ ) to remerge the video back together (this will be automated soon).



### Debug and Tips


1) I highly recommend playing with psnr_low and psnr_high before starting a long upscale. Do a small test of 10-15 seconds, see
   if you like the way it looks, and adjust accordingly.
    
2) I highly recommend using compressed footage.


### Upscaling Your Own Video ###

(You may operate out of any directory, but I recommend following this guide for beginners)

0) Open up your Dandere2x Folder

1) Open up 'config.ini' using a text editor

2) Place your video, "YOUR_VIDEO.mkv" into \demo_folder\video\

3) Edit the variable **workspace** to house a new workspace. For begineers, I recommend changing

[this]demo_folder\shelter\ -> [this]demo_folder\YOUR_VIDEO\


4) Edit the variable **file_dir** to point to your file. For begineers, I recommend changing

file_dir=[this]demo_folder\video\shelter.mkv -> file_dir=[this]demo_folder\video\YOUR_VIDEO.mkv

5) Change block size to match your input video's resolution. The blocksize must be a common factor between the height and width of your video. You can calculate common factors here: https://www.calculatorsoup.com/calculators/math/commonfactors.php


If "YOUR_VIDEO.mkv" is 1280x720, a common factor is 16. So change blocksize

block_size=30 -> block_size=16









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
