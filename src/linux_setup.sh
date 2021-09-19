#!/bin/sh

# Requirements...
if ! command -v cmake /dev/null 2>&1; then
    echo "cmake could not be found"
    exit
fi

if ! command -v ffmpeg > /dev/null 2>&1; then
    echo could not find path to ffmpeg binary
    exit
fi

# Create d2x-cpp binary
cd ../dandere2x_cpp
cmake CMakeLists.txt
make

FILE=dandere2x_cpp
if ! test -f "$FILE"; then
    echo "$FILE does not exist.. not sure what's wrong..."
    exit 1
fi

#  get into the src folder from dandere2x_cpp
cd ../src

# create the externals folder and move over the recently made d2x_cpp binary
mkdir -p externals
mv ../dandere2x_cpp/dandere2x_cpp ./externals/dandere2x_cpp

# download waifu2x-ncnn-vulkan and extract it the way d2x expects it
cd externals

if command -v waifu2x-ncnn-vulkan > /dev/null 2>&1; then
    waifu2x_vulkan=$(command -v waifu2x-ncnn-vulkan)
else
    echo "installing latest waifu2x-ncnn-vulkan"
    echo ""
    # download latest waifu2x-ncnn-vulkan and extract it to externals
    curl -s https://api.github.com/repos/nihui/waifu2x-ncnn-vulkan/releases/latest | sed -n 's/.*"browser_download_url": "\(.*ubuntu\.zip\)".*/\1/p' | xargs -n1 curl -o waifu2x-ncnn-vulkan.zip -OL
    unzip -j waifu2x-ncnn-vulkan.zip */waifu2x-ncnn-vulkan
    rm waifu2x-ncnn-vulkan.zip
    waifu2x_vulkan=externals/waifu2x-ncnn-vulkan
fi

if command -v realsr-ncnn-vulkan > /dev/null 2>&1; then
    realsr_vulkan=$(command -v realsr-ncnn-vulkan)
else
    echo "installing latest realsr-ncnn-vulkan"
    echo ""
    # download latest realsr-ncnn-vulkan and extract it to externals
    curl -s https://api.github.com/repos/nihui/realsr-ncnn-vulkan/releases/latest | sed -n 's/.*"browser_download_url": "\(.*ubuntu\.zip\)".*/\1/p' | xargs -n1 curl -o realsr-ncnn-vulkan.zip -OL
    unzip -j realsr-ncnn-vulkan.zip */realsr-ncnn-vulkan
    rm realsr-ncnn-vulkan.zip
    realsr_vulkan=externals/realsr-ncnn-vulkan
fi

if command -v waifu2x-converter-cpp > /dev/null 2>&1; then
    waifu2x_converter_cpp=$(command -v waifu2x-converter-cpp)
else
    # TODO: download latest source waifu2x-converter-cpp and build it to externals
    echo "to use waifu2x-converter-cpp build from source following the instructions in https://github.com/DeadSix27/waifu2x-converter-cpp/blob/master/BUILDING.md and copy the resulting binary to the src/externals directory"
    echo ""
    waifu2x_converter_cpp=externals/waifu2x-converter-cpp
fi

if command -v waifu2x-caffe-cui > /dev/null 2>&1; then
    waifu2x_caffe=$(command -v waifu2x-caffe-cui)
else
    # TODO: download latest source waifu2x-caffe and build it to externals
    echo "to use waifu2x-caffe see build instructions in https://github.com/nagadomi/waifu2x-caffe-ubuntu/blob/ubuntu/INSTALL-linux.md and copy the resulting binary to the src/externals directory"
    echo ""
    waifu2x_caffe=externals/waifu2x-caffe-cui
fi

ffmpeg=$(command -v ffmpeg)
ffprobe=$(command -v ffprobe)
dandere2x_cpp=externals/dandere2x_cpp

# create executable_config file
printf "ffmpeg: \"$ffmpeg\"\nffprobe: \"$ffprobe\"\ndandere2x_cpp: \"$dandere2x_cpp\"\nwaifu2x_vulkan: \"$waifu2x_vulkan\"\nwaifu2x_converter_cpp: \"$waifu2x_converter_cpp\"\nwaifu2x_caffe: \"$waifu2x_caffe\"\nrealsr_ncnn_vulkan: \"$realsr_vulkan\"" > ../config_files/executable_paths.yaml

# create workspace folder (this needs to exist I think?)
mkdir -p workspace
echo "setup successful. install the requirements with pip3 install -r requirements.txt, preferably in a a virtual environment, then run python3 main.py"
