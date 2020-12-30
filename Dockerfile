FROM ubuntu:19.10

RUN sed -i "s/archive/old-releases/" /etc/apt/sources.list \
    && sed -i "/security/d" /etc/apt/sources.list \
    && apt-get update
    
RUN apt install -y --no-install-recommends apt-utils software-properties-common
RUN add-apt-repository -y ppa:graphics-drivers/ppa
RUN export DEBIAN_FRONTEND="noninteractive" & apt-get install -y keyboard-configuration
RUN apt install -y --no-install-recommends ffmpeg libmagic1 nvidia-cuda-toolkit nvidia-driver-440 python3.8
RUN apt install -y --no-install-recommends libvulkan1

# run installation
RUN apt-get -y update
RUN apt-get install -y cmake
RUN apt-get install -y git-core
RUN apt-get install -y build-essential
RUN apt-get install -y libgl1-mesa-glx
RUN apt-get install -y ffmpeg
RUN apt-get install -y wget
RUN apt-get install -y zip
RUN mkdir /dandere2x/
RUN ls
RUN ls
RUN git clone -b docker --recurse-submodules --progress https://github.com/aka-katto/dandere2x.git /dandere2x/dandere2x
    
RUN ls /dandere2x/dandere2x/
RUN cd /dandere2x/dandere2x/src/ && bash /dandere2x/dandere2x/src/linux_setup.sh

RUN wget https://github.com/nihui/waifu2x-ncnn-vulkan/releases/download/20200606/waifu2x-ncnn-vulkan-20200606-linux.zip
RUN unzip waifu2x-ncnn-vulkan-20200606-linux.zip
RUN mv waifu2x-ncnn-vulkan-20200606-linux /dandere2x/dandere2x/src/externals/waifu2x-ncnn-vulkan
RUN rm waifu2x-ncnn-vulkan-20200606-linux.zip

RUN apt install -y python3-pip
RUN pip3 install -U pip
RUN pip3 install -r /dandere2x/dandere2x/src/requirements.txt
RUN pip3 install pyyaml==5.3

WORKDIR /dandere2x/dandere2x/src/
RUN ls -R /dandere2x/dandere2x/src/
ENTRYPOINT ["python3", "/dandere2x/dandere2x/src/main.py"]

ENV NVIDIA_DRIVER_CAPABILITIES all
ENV DEBIAN_FRONTEND teletype
