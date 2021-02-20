FROM ubuntu:19.10

# Since ubuntu 19.10 isn't LTS, use LTS sources for the packages we need.
RUN sed -i "s/archive/old-releases/" /etc/apt/sources.list \
    && sed -i "/security/d" /etc/apt/sources.list \
    && apt-get update

# We need Nvidia Drivers
RUN apt install -y --no-install-recommends apt-utils software-properties-common
RUN add-apt-repository -y ppa:graphics-drivers/ppa
RUN apt-get -y update

# Set nvidia-driver installation to not ask for keyboard configeration
RUN export DEBIAN_FRONTEND="noninteractive" & apt-get install -y keyboard-configuration

# Needed Libraries for Dandere2x
RUN apt install -y --no-install-recommends ffmpeg nvidia-driver-440 python3.8 libvulkan1 libgtk2.0-dev pkg-config

# Needed Library for Building Dandere2x (this will be removed later)
RUN apt-get install -y cmake
RUN apt-get install -y git-core
RUN apt-get install -y build-essential
RUN apt-get install -y libgl1-mesa-glx
RUN apt-get install -y ffmpeg
RUN apt-get install -y wget
RUN apt-get install -y zip

# Move Dandere2x's files to /dandere2x/
RUN mkdir /dandere2x/
RUN git clone --recurse-submodules --progress https://github.com/aka-katto/dandere2x.git /dandere2x/dandere2x

# Begin the building process
RUN cd /dandere2x/dandere2x/src/ && bash /dandere2x/dandere2x/src/linux_setup.sh

# RUN wget https://github.com/nihui/waifu2x-ncnn-vulkan/releases/download/20200606/waifu2x-ncnn-vulkan-20200606-linux.zip
# RUN unzip waifu2x-ncnn-vulkan-20200606-linux.zip
# RUN mv waifu2x-ncnn-vulkan-20200606-linux /dandere2x/dandere2x/src/externals/waifu2x-ncnn-vulkan
# RUN rm waifu2x-ncnn-vulkan-20200606-linux.zip

# Install Python Dependencies (note pyyaml has to be manually installed due to ubuntu:19.10 python3.8 restriction)
# Ubuntu 19.10 will by default use python3.75 rather than the needed 3.8, so we have to manually get pip and refer to python + python as 3.8

RUN wget 'https://bootstrap.pypa.io/get-pip.py' && python3.8 get-pip.py
RUN pip3.8 install -U pip
RUN pip3.8 install -r /dandere2x/dandere2x/src/requirements.txt

WORKDIR /dandere2x/dandere2x/src/
ENTRYPOINT ["python3.8", "/dandere2x/dandere2x/src/main.py"]

ENV NVIDIA_DRIVER_CAPABILITIES all
ENV DEBIAN_FRONTEND teletype
