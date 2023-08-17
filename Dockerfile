FROM docker.io/nvidia/cuda:12.2.0-base-ubuntu22.04

RUN apt-get update

# Needed Libraries for Dandere2x
RUN apt install -y --no-install-recommends \
    libglvnd0 \
    libgl1 \
    libglx0 \
    libegl1  \
    libgles2  \
    libxcb1-dev \
    ffmpeg \
    python3.10 \
    vulkan-tools \
    libgtk2.0-dev \
    pkg-config

# Needed Library for Building Dandere2x (this will be removed later)
RUN apt-get install -y cmake
RUN apt-get install -y curl
RUN apt-get install -y git-core
RUN apt-get install -y build-essential
RUN apt-get install -y libgl1-mesa-glx
RUN apt-get install -y ffmpeg
RUN apt-get install -y python3-pip
RUN apt-get install -y wget
RUN apt-get install -y zip

#set VULKAN_SDK_VERSION as a build-arg=`curl https://vulkan.lunarg.com/sdk/latest/linux.txt`
ARG VULKAN_SDK_VERSION
# Download the Vulkan SDK and extract the headers, loaders, layers and binary utilities
RUN wget -q --show-progress \
    --progress=bar:force:noscroll \
    https://sdk.lunarg.com/sdk/download/latest/linux/vulkan_sdk.tar.gz \
    -O /tmp/vulkansdk-linux-x86_64-${VULKAN_SDK_VERSION}.tar.gz \ 
    && echo "Installing Vulkan SDK ${VULKAN_SDK_VERSION}" \
    && mkdir -p /opt/vulkan \
    && tar -xf /tmp/vulkansdk-linux-x86_64-${VULKAN_SDK_VERSION}.tar.gz -C /opt/vulkan \
    && mkdir -p /usr/local/include/ && cp -ra /opt/vulkan/${VULKAN_SDK_VERSION}/x86_64/include/* /usr/local/include/ \
    && mkdir -p /usr/local/lib && cp -ra /opt/vulkan/${VULKAN_SDK_VERSION}/x86_64/lib/* /usr/local/lib/ \
    && cp -a /opt/vulkan/${VULKAN_SDK_VERSION}/x86_64/lib/libVkLayer_*.so /usr/local/lib \
    && mkdir -p /usr/local/share/vulkan/explicit_layer.d \
    && cp /opt/vulkan/${VULKAN_SDK_VERSION}/x86_64/etc/vulkan/explicit_layer.d/VkLayer_*.json /usr/local/share/vulkan/explicit_layer.d \
    && mkdir -p /usr/local/share/vulkan/registry \
    && cp -a /opt/vulkan/${VULKAN_SDK_VERSION}/x86_64/share/vulkan/registry/* /usr/local/share/vulkan/registry \
    && cp -a /opt/vulkan/${VULKAN_SDK_VERSION}/x86_64/bin/* /usr/local/bin \
    && ldconfig \
    && rm /tmp/vulkansdk-linux-x86_64-${VULKAN_SDK_VERSION}.tar.gz && rm -rf /opt/vulkan

# Setup the required capabilities for the container runtime    
ENV NVIDIA_DRIVER_CAPABILITIES compute,graphics,utility

# Enable Vulkan for nVidia cards
COPY src/config_files/nvidia_icd.x86_64.json /etc/vulkan/icd.d/
COPY src/config_files/10_nvidia.json /usr/share/glvnd/egl_vendor.d/
# Move Dandere2x's files to /dandere2x/
RUN mkdir /dandere2x/
RUN git clone --recurse-submodules --progress https://github.com/aka-katto/dandere2x.git /dandere2x/dandere2x

# Begin the building process
RUN cd /dandere2x/dandere2x/src/ && bash /dandere2x/dandere2x/src/unix_setup.sh

RUN pip3 install -r /dandere2x/dandere2x/src/requirements.txt

WORKDIR /dandere2x/dandere2x/src/
ENTRYPOINT ["python3", "/dandere2x/dandere2x/src/main.py"]

ENV NVIDIA_DRIVER_CAPABILITIES all
ENV DEBIAN_FRONTEND teletype
