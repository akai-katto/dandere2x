# Dandere2x - Fast Waifu2x Video Upscaling

Subreddit (Preferred Contact): https://www.reddit.com/r/Dandere2x/

Telegram Server: https://t.me/joinchat/KTRznBIPPNCbHkUqnwT8pA


# Quick Overview

This following section is a brief, white-paper styled explanation of Dandere2x. For a more in-depth explanation, check out this link: https://github.com/aka-katto/dandere2x/wiki/How-Dandere2x-Works




## Abstract (Introduction)

Dandere2x reduces the time needed for Waifu2x to upscale animation (sometimes live-action) videos by applying compression techniques. Just as Netflix uses compression to quickly stream videos to your home, Dandere2x uses compression to expedite the waifu2x upscaling process.

## Motivation 

Waifu2x is a powerful tool for upscaling anime-styled images to a higher resolution. However, for most users, the task is very slow, with each frame taking around 1-2 seconds in a 1080p video to be scaled to 3840p. Considering the number of visual redundancies found in anime, having an algorithm to identify these redundancies and recycling them would prove to be an effective time-reducing step to help upscale images to higher resolutions. Dandere2x does this by applying I-frame and p-frame compression to anime-styled videos.


![Image of I-Frame Compression](https://upload.wikimedia.org/wikipedia/commons/thumb/6/64/I_P_and_B_frames.svg/1920px-I_P_and_B_frames.svg.png)
*Image: Different compression types being visualized with PacMan. Source: Wikipedia*

## Methods

Dandere2x is a novel method and algorithm for anime-specific and upscaling-specific compression targeted at reducing the GPU time needed to upscale a video. Without going in-depth into the tools used, the following image summarizes the dandere2x process, and how it uses previous frames to create future frames.

![Image of Dandere2x](https://i.imgur.com/7cqZz4I.png)

By only upscaling the content that can't be produced from a previous frame, Dandere2x can dramatically speed up the upscaling process by only upscaling essential information.

## Results

Here is are some user-created videos that were produced using older versions of Dandere2x.

https://www.youtube.com/watch?v=sfD_D9KVfzE

https://www.youtube.com/watch?v=VhqRVW_fU5s

https://www.youtube.com/watch?v=w3QBHD47Yr0

# Dandere2x as a Program

Dandere2x as a program is still being improved and maintained. My current goal is to provide a more user-friendly and stable experience for the program.



## Current Features

#### Quality Customizable

The quality of a dandere2x video is currently customizable. For more in-depth reading, refer to this link: https://github.com/aka-katto/dandere2x/wiki/Settings-and-Their-Meanings


#### Interactive GUI

![Image of the GUI](https://i.imgur.com/PWe7NzV.png)

While still in the works, Dandere2x currently has a GUI which allows for a user-friendly experience. 

#### Suspend / Resume Session Capabilities

Dandere2x can be started, suspended, then resumed in a later session. This feature is still being tested by users, but for the developer, it seems stable.


#### Reduced Disk Usage

Dandere2x has a novel method of minimizing the hard-drive complexity by only referring to files on-disk when needed, and will delete files in real-time to prevent the workspace from being too large. It is possible to allow Dandere2x to upscale a video while keeping the used space under 200mb. 

# Development Status

I consider 1.3.1 the most stable build, with any release after that a testing version. You can test these later versions yourself and report bugs as they come up to help bring another stable release out.

As for me, I'm a college student and I put time into Dandere2x when it's appropriate. I prioritize school + life, but Dandere2x is worked on when I can. If you wish to actively follow my thoughts and developments, I highly encourage you to check out the subreddit at

www.reddit.com/r/dandere2x

## Downloads


For those looking to use Dandere2x, I highly encourage using the latest stable release at 

https://github.com/aka-katto/dandere2x/releases


## Can I help with Dandere2x?

Dandere2x has been very reliant on the community for its development. Testing nightly releases and reporting bugs and crashes has allowed Dandere2x to become usable over many months. 

Feel free to comment on your ideas on what can or should be improved on. I'm more than happy to explain some code to you over telegram if you wish to contribute to the project.

## FAQ

Q: What is the difference between Dandere2x and Video2x?

A: Video2x aims for quality over speed. If you're looking for the best-possible looking video, Video2x is more streamlined and provides lossless upscaling. Dandere2x, on the other hand, is much faster than video2x, but at the cost of being lossy. 


Q: How does Dandere2x work?

A: https://github.com/aka-katto/dandere2x/wiki/How-Dandere2x-Works


## Links 

Documentation:

https://dandere2x.readthedocs.io/

Subreddit:

https://www.reddit.com/r/Dandere2x/

Telegram Server:

https://t.me/joinchat/KTRznBIPPNCbHkUqnwT8pA

Patreon:

https://www.patreon.com/dandere2x


## Related Resources

[Video2x](https://github.com/k4yt3x/video2x): A lossless video enlarger/video upscaler achieved with waifu2x.

## Credits

This project relies on the following software and projects.

- waifu2x-caffe
- waifu2x
- ffmpeg
- STB Image
- waifu2x-ncnn-vulkan
- waifu2x-converter-cpp-deadsix 

Code was used from the following projects

- Video2x
