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
Dependencies:
* python 3
* cmake
* ffmpeg

Check that you have these installed by running `which cmake`, `which ffmpeg` and `which python3`. Python 3 should be installed by default. You should get an output similar to `/usr/bin/ffmpeg`, else you will need to install these packages through your [package manager](https://wiki.archlinux.org/title/Pacman/Rosetta).

---
Installation:
1. Download the source by [cloning this repository](https://github.com/akai-katto/dandere2x/archive/refs/heads/master.zip) or by going into [releases](https://github.com/akai-katto/dandere2x/releases) and downloading the source from there. Extract the contents of the source file.
2. Navigate to the `src` directory inside the root of Dandere2x.
3. While in `src` on the root directory, run `./linux_setup.sh`. This will download the lastest linux binaries for waifu2x-ncnn-vulkan and realsr-ncnn-vulkan. If you want waifu2x-converter-cpp or waifu2x-caffe, you will have to compile them from source. 
4. Setup a virtual environment with `python3 -m venv .venv`. To activate, run `source .venv/bin/activate`. `.venv` can be exchanged for any path that you prefer. *This step is not strictly necessary, but highly recommended.*
5. Install the Python dependencies with `pip3 install --user -r requirements.txt`
6. Run Dandere2x: `python3 main.py`. Running without any command-line arguments will attempt to start the GUI, if you want to see a complete list of options, use the `--help` argument.

* You can remove the PyQt line from the requirements.txt file, if you aren't going to use the GUI.
* If you can't run `./linux_setup.sh`, try changing its permissions by running `chmod u+x linux_setup.sh`.
---
If you are running Arch, there are [AUR](https://wiki.archlinux.org/title/Arch_User_Repository) packages for all upscaler implementations used in this project, including precompiled binaries for waifu2x-ncnn-vulkan and realsr-ncnn-vulkan. You can easily install them with an [AUR Helper](https://wiki.archlinux.org/title/AUR_helpers), such as [paru](https://github.com/morganamilo/paru).

Example: 
`paru -Syu waifu2x-ncnn-vulkan waifu2x-converter-cpp waifu2x-caffe realsr-ncnn-vulkan`

`./linux_setup.sh` will automatically create a config that uses the upscaler binaries that you have installed, including the ones from the AUR. As long as the binary is in PATH, the script will add it to the config. 

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
