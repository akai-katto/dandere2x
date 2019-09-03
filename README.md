# Dandere2x - Fast Waifu2x Video Upscaling

## What is Dandere2x

Dandere2x reduces the time needed for Waifu2x to upscale animation (sometimes live-action) videos by applying compression techniques. Just as Netflix uses compression to quickly stream videos to your home, Dandere2x uses compression to expedite the waifu2x upscaling process.


## Links 

Documentation:

https://dandere2x.readthedocs.io/

Subreddit:

https://www.reddit.com/r/Dandere2x/

Telegram Server:

https://t.me/joinchat/KTRznBIPPNCbHkUqnwT8pA

Patreon:

https://www.patreon.com/dandere2x

## Current Features

- Interpolated Video Compression
- Minimum Quality Loss (MQL) dictated by DCT quantization. 
- Weighted Blocks (Fade to Black, Fade to White) 
- Real-time Video Encoding
- Interactive GUI


## How does Dandere2x work?

Dandere2x is a compression algorithm specifically designed to help compress anime so Waifu2x can work faster. In short, Dandere2x looks for redundancies in Anime to reduce the time needed to upscale a video. A longer, more in-depth post can be found here. 

https://github.com/aka-katto/dandere2x/wiki/How-Dandere2x-Works

## GUI Preview

![Image of the GUI](https://i.imgur.com/PWe7NzV.png)

## Development Status

Dandere2x is in development and research, primarily by a single individual (the author). Currently, Dandere2x is in beta-candidate testing, which the author hopes to release as a beta release.

Updates, thoughts, and progress can be found in the form of posts on the Dandere2x subreddit:

https://www.reddit.com/r/Dandere2x/


## Can I help with Dandere2x?

Dandere2x has been very reliant on the community for its development. Testing newest and nightly releases and reporting bugs and crashes has allowed Dandere2x to become usable over many months. 

Furthermore, the read the docs are underdocumented, and some of the code can be messy. Contributing your thoughts and ideas to either would go a long way - feel free to comment your ideas on what can or should be improved on. 

## FAQ

Q: What is the difference between Dandere2x and Video2x?

A: Video2x aims for quality over speed. If you're looking for the best-possible looking video, Video2x is more streamlined and provides lossless upscaling. Dandere2x, on the other hand, is still in development, is much faster than video2x, but at the cost of being lossy. 


Q: How does Dandere2x work?

A: https://github.com/aka-katto/dandere2x/wiki/How-Dandere2x-Works

## Related Resources

[Video2x](https://github.com/k4yt3x/video2x): A lossless video enlarger/video upscaler achieved with waifu2x.

## Credits

This project relies on the following software and projects.

- waifu2x-caffe
- waifu2x
- FFmpeg
- STB Image
- waifu2x-vulkan
- waifu2x-converter-cpp-deadsix 

Code was used from the following projects

- Video2x
