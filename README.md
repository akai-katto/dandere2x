# Edit:

Development status is postponed at the moment due to corona. The latest releases seem to be stable, but still please report bugs for when I return to development. 

# Dandere2x - Fast Waifu2x Video Upscaling

Subreddit (Preferred Contact): https://www.reddit.com/r/Dandere2x/

Telegram Server: https://t.me/joinchat/KTRznBIPPNCbHkUqnwT8pA

# Tech Overview

This following section is a brief, white-paper styled explanation of Dandere2x. For a more in-depth explanation, check out this link: https://github.com/aka-katto/dandere2x/wiki/How-Dandere2x-Works. I've simplified this landing page greatly to make the program more understandable for new users. 


## Abstract (Introduction)

Dandere2x reduces the time needed for Waifu2x to upscale animation (sometimes live-action) videos by applying compression techniques. Just as Netflix uses compression to quickly stream videos to your home, Dandere2x uses compression to expedite the waifu2x upscaling process.

## Motivation 

Waifu2x (https://github.com/nagadomi/waifu2x) is a powerful tool for upscaling anime-styled images to a higher resolution. It does this using a convolutional neural network, which can bring greater visual fidelity to images by removing the noise produced from resolution upscaling or compression.

![Image of a Waifu2x Upscale](https://i.imgur.com/irRaQ07.png)

*Image: An image of lower resolution ( left ) being brought to a higher resolution using waifu2x (right). Source: Wikipedia*


While waifu2x may take 2-4 seconds on a modern graphics card to produce a higher resolution image, this becomes problematic when upscaling frames in a video, as one video-second can take multiple minutes to process. Considering the number of visual redundancies found in anime, having an algorithm to identify these redundancies and recycling them would prove to be an effective time-reducing step to help upscale videos to higher resolutions. Dandere2x does this by applying I-frame and p-frame compression to anime-styled videos to reduce the work needed by the GPU.


![Image of I-Frame Compression](https://upload.wikimedia.org/wikipedia/commons/thumb/6/64/I_P_and_B_frames.svg/1920px-I_P_and_B_frames.svg.png)
*Image: Different compression types being visualized with PacMan. Source: Wikipedia*

## Methods

Dandere2x is an upscaling-specific compression algorithm targeted at reducing the GPU time needed to upscale a video. Without going in-depth into the tools used, the following image summarizes the dandere2x process, and how it uses previous frames to create future frames.

![Image of Dandere2x](https://i.imgur.com/7cqZz4I.png)

By only upscaling the content that can't be produced from a previous frame, Dandere2x can dramatically speed up the upscaling process by only upscaling essential information.

## Results



### Preformance Differences

The time-reduction dandere2x produces varies based on the user input, as well as the settings used. However, in a benchmark video is shown here, Dandere2x provided a dramatic improvement in time over Video2x (a lossless waifu2x-video upscaler): https://www.youtube.com/watch?v=d1Y4pmQb44k.

| Upscaler  | Time  |
|-----------|-------|
| Dandere2x | 03:37 |
| Video2x   | 18:34 |


Here is are some user-created videos that were produced using older versions of Dandere2x.

https://www.youtube.com/watch?v=sfD_D9KVfzE

https://www.youtube.com/watch?v=VhqRVW_fU5s

https://www.youtube.com/watch?v=w3QBHD47Yr0

### Compression Noise

Being a loss-driven compression algorithm, Dandere2x produced noticeable noise on its own (which can be fixed with filters, which will be discussed later). Likewise, as a result of how convolutional pooling works, compressed blocks have a noticeable discoloration at the edges.

![A picture of Dandere2x Noise](https://i.imgur.com/uF2xk83.png)

*Image: A picture of noise produced by raw Dandere2x. Notice the obvious placement of the blocks in the color gradients.*

However, Reddit user /u/Naizuri77 found that various compression filters can reduce the noticeability of these visual blemishes.

![A picture of Dandere2x reduced using filters](https://i.imgur.com/rVMgy5U.png)

*Image: The same image above, but with a compression-filter applied to reduce the dandere2x compression noise.*


# Program Overview

Dandere2x as a program is still being improved and maintained. My current goal is to provide a more user-friendly and stable experience for the program.



## Current Features

While I consider dandere2x more as a compression algorithm, it stands on its own as a program, with several quality-of-life features. 

![Image of the GUI](https://i.imgur.com/PWe7NzV.png)

*Image: A picture of the dandere2x GUI (old)*

### 1) Quality Customizable

The quality of a dandere2x video is currently customizable, meaning users can trade speed for overall visual fidelity of an upscale. For more in-depth reading, refer to this link: https://github.com/aka-katto/dandere2x/wiki/Settings-and-Their-Meanings


### 2) Interactive GUI

While still in the works, Dandere2x currently has a GUI which allows for a user-friendly experience. I plan on re-making this whenever. 

### 3) Suspend / Resume Session Capabilities

Dandere2x can be started, suspended, then resumed in a later session. This feature is still being tested by users, but for the developer, it seems stable.


### 4) Reduced Disk Usage

Dandere2x has a novel method of minimizing the hard-drive complexity by only referring to files on-disk when needed, and will delete files in real-time to prevent the workspace from being too large. It is possible to allow Dandere2x to upscale a video while keeping the used space under 200mb. 

# Downloads

### Stable Download:

I consider 1.3.1 the most stable build, although a bit older, has the most hours used and encounters the least amount of errors. If you're looking for a more modern dandere2x, consider trying a nightly build-out. 

https://github.com/aka-katto/dandere2x/releases/tag/1.3.1

### Nightly Download:

Anything beyond 1.3.1 I don't consider stable, although users are still finding bugs in my latest additions. Reporting bugs will help bring a future build to become more stable. 

The most recent and stable-ish build is 1.8

https://github.com/aka-katto/dandere2x/releases/tag/1.8

# Development Status

As for me, I'm a college student and I put time into Dandere2x when it's appropriate. I prioritize school + life, but Dandere2x is worked on when I can. If you wish to actively follow my thoughts and developments, I highly encourage you to check out the subreddit at

www.reddit.com/r/dandere2x


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
