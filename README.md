# Dandere2x - Fast Waifu2x Video Upscaling

## What is Dandere2x

Dandere2x makes upscaling videos with waifu2x much faster by applying compression techniques. Although the process itself is lossy, dandere2x provides a dramatic speedup in the time needed to upscale a video using waifu2x.


## Development Status

Dandere2x is in development and in research. Much of my current thoughts can be found on my subreddit or on twitter. I highly encourage anyone who needs help / has questions to either submit an Issue on GitHub or ask other users on the subreddit.

https://www.reddit.com/r/Dandere2x/

https://twitter.com/aka_katto

## FAQ

Q: What is the difference between Dandere2x and Video2x?

A: Video2x aims for quality over speed. If you're looking for the best-possible looking video, Video2x is more streamlined and provides lossless upscaling. Dandere2x, on the other hand, is still in development, is (can) much faster than video2x, but at the cost of being lossy. 


Q: How does Dandere2x work?

A: Dandere2x works by trying to recycle redundant information between frames. In anime (or cartoons in general), scenes tend to be very static, and as a result, not every part of a frame needs to be redrawn. Dandere2x identifies these blocks and reuses them to avoid unnecessary computation. 

## Related Resources

[Video2x](https://github.com/k4yt3x/video2x): A lossless video enlarger/video upscaler achieved with waifu2x.

## Credits

This project relies on the following software and projects.

- waifu2x-caffe
- waifu2x
- FFmpeg
- STB Image
