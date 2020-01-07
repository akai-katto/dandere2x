# Dandere2x - Fast Waifu2x Video Upscaling

## What is Dandere2x?

Dandere2x reduces the time needed for Waifu2x to upscale animation (sometimes live-action) videos by applying compression techniques. Just as Netflix uses compression to quickly stream videos to your home, Dandere2x uses compression to expedite the waifu2x upscaling process.

## Current Features

- Interpolated video compression
- Minimum Quality Loss (MQL) dictated by DCT quantization
- Weighted blocks (Fade to Black, Fade to White) 
- Interactive GUI
- Suspend / Resume Session Capabilities
- Reduced Disk Usage Mode (reduces the amount of files saved to the disk at a given time)


## How does Dandere2x work?

Dandere2x is a compression algorithm specifically designed to help compress anime so Waifu2x can work faster. In short, Dandere2x looks for redundancies in anime to reduce the time needed to upscale a video. A longer, more in-depth post can be found here. 

https://github.com/aka-katto/dandere2x/wiki/How-Dandere2x-Works

## GUI Preview

![Image of the GUI](https://i.imgur.com/PWe7NzV.png)

## Development Status

Dandere2x has entered it's beta phase, meaning that although development is still happening, the program itself is now stable and usable to others as a beta-release.

If you wish to actively follow my thoughts and developments, I highly encourage you to check out the subreddit at

www.reddit.com/r/dandere2x

For those looking to use Dandere2x, I highly encourage using the latest stable release at 

https://github.com/aka-katto/dandere2x/releases

## Can I help with Dandere2x?

Dandere2x has been very reliant on the community for its development. Testing nightly releases and reporting bugs and crashes has allowed Dandere2x to become usable over many months. 

Feel free to comment your ideas on what can or should be improved on. I'm more than happy to explain some code to you over telegram if you wish to contribute to the project.

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
