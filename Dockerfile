FROM ubuntu:22.04 as BASEWAIFUX2CPP

ENV DEBIAN_FRONTEND noninteractive

# We need Nvidia Drivers
RUN apt-get -y update
RUN apt -y install ocl-icd-opencl-dev
RUN apt -y install libopencv-dev libopencv-imgcodecs-dev libopencv-imgproc-dev libopencv-core-dev
RUN apt -y install nvidia-cuda-toolkit
RUN apt install -y --no-install-recommends apt-utils software-properties-common gpg-agent
RUN add-apt-repository universe
RUN apt-get -y update

# Needed Library for Building Dandere2x (this will be removed later)
RUN apt-get install -y cmake
RUN apt-get install -y git-core
RUN apt-get install -y build-essential

WORKDIR /dandere2x
RUN git clone "https://github.com/DeadSix27/waifu2x-converter-cpp"
WORKDIR /dandere2x/waifu2x-converter-cpp
RUN mkdir out
WORKDIR /dandere2x/waifu2x-converter-cpp/out
RUN cmake ..
RUN make -j4


FROM ubuntu:22.04

# We need Nvidia Drivers
RUN apt-get -y update
RUN apt install -y --no-install-recommends apt-utils software-properties-common gpg-agent
RUN add-apt-repository universe
RUN apt-get -y update

# Set nvidia-driver installation to not ask for keyboard configeration
RUN apt-get install -y keyboard-configuration
ENV DEBIAN_FRONTEND noninteractive

# Needed Libraries for Dandere2x
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update
RUN apt-get install python3.8 -y

RUN apt install -y --no-install-recommends ffmpeg nvidia-driver-440 libvulkan1 libgtk2.0-dev pkg-config

# Dependencies for waifu2x-converter-cpp
RUN apt -y install libopencv-dev libopencv-imgcodecs-dev libopencv-imgproc-dev libopencv-core-dev

# Needed Library for Building Dandere2x (this will be removed later)
RUN apt-get install -y cmake
RUN apt-get install -y git-core
RUN apt-get install -y build-essential
RUN apt-get install -y libgl1-mesa-glx
RUN apt-get install -y ffmpeg
RUN apt-get install -y wget
RUN apt-get install -y zip


# Move Dandere2x's files to /dandere2x/
#RUN mkdir /dandere2x/
#RUN git clone --recurse-submodules --progress https://github.com/devedse/dandere2x.git /dandere2x/dandere2x
COPY . /dandere2x/dandere2x

# Begin the building process
RUN cd /dandere2x/dandere2x/src/ && bash /dandere2x/dandere2x/src/unix_setup.sh

# RUN wget https://github.com/nihui/waifu2x-ncnn-vulkan/releases/download/20200606/waifu2x-ncnn-vulkan-20200606-linux.zip
# RUN unzip waifu2x-ncnn-vulkan-20200606-linux.zip
# RUN mv waifu2x-ncnn-vulkan-20200606-linux /dandere2x/dandere2x/src/externals/waifu2x-ncnn-vulkan
# RUN rm waifu2x-ncnn-vulkan-20200606-linux.zip

RUN apt-get install python3-distutils python3-apt python3-pip -y
RUN pip3 install -r /dandere2x/dandere2x/src/requirements.txt

COPY --from=BASEWAIFUX2CPP /dandere2x/waifu2x-converter-cpp/out /dandere2x/dandere2x/src/externals/waifu2x-converter-cpp
COPY --from=BASEWAIFUX2CPP /dandere2x/waifu2x-converter-cpp/models_rgb /usr/local/share/waifu2x-converter-cpp/

WORKDIR /dandere2x/dandere2x/src/
ENTRYPOINT ["python3", "/dandere2x/dandere2x/src/main.py"]

ENV NVIDIA_DRIVER_CAPABILITIES all
ENV DEBIAN_FRONTEND teletype
