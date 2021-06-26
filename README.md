<p align="center">
    <img src="https://i.imgur.com/ixiaGqT.jpgg" alt="Dandere2x Logo, Made by Tremeschin" width="200" height="200">
</p>

<h3 align="center">Dandere2x!</h3>
<p align="center">
  A faster way to upscale videos using waifu2x using video compression technology.
  <br>
  <br>
  <a href="https://github.com/aka-katto/dandere2x/wiki/How-Dandere2x-Works/"><strong>Click here to read how Dandere2x works! </strong></a>
  <br>
  <a href="https://www.reddit.com/r/Dandere2x/">Subreddit</a>
  ·
  <a href="https://github.com/aka-katto/dandere2x/releases/tag/2.0">Download</a>
  ·
  <a href="https://www.youtube.com/watch?v=5grmGE5al2A">Tutorial</a>
</p>

# Dandere2x's Motivation and Big Idea 

Waifu2x (https://github.com/nagadomi/waifu2x) is a powerful tool for upscaling anime-styled images to a higher resolution. It does this using a convolutional neural network, which can bring greater visual fidelity to images by removing the noise produced from resolution upscaling or compression.

![Image of a Waifu2x Upscale](https://i.imgur.com/irRaQ07.png)

*Image: An image of lower resolution ( left ) being brought to a higher resolution using waifu2x (right). Source: Wikipedia*


While waifu2x may take 2-4 seconds on a modern graphics card to produce a higher resolution image, this becomes problematic when upscaling frames in a video, as one video-second can take multiple minutes to process. Considering the number of visual redundancies found in anime, having an algorithm to identify these redundancies and recycling them would prove to be an effective time-reducing step to help upscale videos to higher resolutions. Dandere2x does this by applying I-frame and p-frame compression to anime-styled videos to reduce the work needed by the GPU.


![Image of I-Frame Compression](https://upload.wikimedia.org/wikipedia/commons/thumb/6/64/I_P_and_B_frames.svg/1920px-I_P_and_B_frames.svg.png)
*Image: Different compression types being visualized with PacMan. Dandere2x uses P-Frames to speed waifu2x up. Source: Wikipedia*

You can read more about how Dandere2x does this <a href="https://github.com/aka-katto/dandere2x/wiki/How-Dandere2x-Works/"><strong>here. </strong></a>

# Docker Usage

The image repo can be found here: https://hub.docker.com/r/akaikatto/dandere2x

The dandere2x docker is ready to be tested. Below are generic instructions on how to use the image, as it's a bit "sharp-around-the-edges".

```
# be cd'd into the directory of the video you wish to upscale. 
$ cd video_directory
$ ls
[your_video.mkv]
$ docker pull akaikatto/dandere2x
$ docker run --rm -it --gpus all -v $PWD:/host akaikatto/dandere2x -p singleprocess -ws ./workspace/ -i /host/[your_video.mkv] -o /host/[your_output.mkv]
```

Replace `[your_video.mkv]` with your video, the docker image will treat the current working directory as the input area / output area for your file. 

For example, my command is 
```
$ docker run --rm -it --gpus all -v $PWD:/host akaikatto/dandere2x -p singleprocess -ws ./workspace/ -i /host/yn_moving.mkv -o /host/yn_moving_upscaled.mkv
```

Assert that you have `nvidia-container-toolkit` installed on your respective machine in order to correctly utilize the image. 

# Downloads

## The latest version can be found here

https://github.com/akai-katto/dandere2x/releases/tag/3.3

## Linux

This is a bit undermaintained, but a known working verison is found here: https://www.reddit.com/r/Dandere2x/comments/i9xn56/linux_rerelease_other_announcements/

I'm juggling to get the linux version more reliably maintained. 

# Related Resources

[Video2x](https://github.com/k4yt3x/video2x): A lossless video enlarger/video upscaler achieved with waifu2x.

# Credits

This project relies on the following software and projects.

- waifu2x-caffe
- waifu2x
- ffmpeg
- STB Image
- waifu2x-ncnn-vulkan
- waifu2x-converter-cpp-deadsix 
