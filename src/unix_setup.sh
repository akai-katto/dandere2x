#!/usr/bin/env bash
OS='linux'

if [[ $OSTYPE =~ "darwin" ]]; then
    OS='macos'
fi

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
cd ../dandere2x_cpp || exit 1
cmake CMakeLists.txt
make

FILE=dandere2x_cpp
if ! test -f "$FILE"; then
    echo "$FILE does not exist.. not sure what's wrong..."
    exit 1
fi

#  get into the src folder from dandere2x_cpp
cd ../src || exit 1

# create the externals folder and move over the recently made d2x_cpp binary
mkdir -p externals
mv ../dandere2x_cpp/dandere2x_cpp ./externals/dandere2x_cpp

# download waifu2x-ncnn-vulkan and extract it the way d2x expects it
cd externals || exit 1


# download latest waifu2x-ncnn-vulkan and extract it to externals
if [[ $OS == 'linux' ]]; then
    echo -e "installing latest waifu2x-ncnn-vulkan for linux\n"
    curl -s https://api.github.com/repos/nihui/waifu2x-ncnn-vulkan/releases/latest | sed -n 's/.*"browser_download_url": "\(.*ubuntu\.zip\)".*/\1/p' | xargs -n1 curl -o waifu2x-ncnn-vulkan.zip -OL
else
    echo -e "installing latest waifu2x-ncnn-vulkan for mac\n"
    curl -s https://api.github.com/repos/nihui/waifu2x-ncnn-vulkan/releases/latest | sed -n 's/.*"browser_download_url": "\(.*macos\.zip\)".*/\1/p' | xargs -n1 curl -o waifu2x-ncnn-vulkan.zip -OL
fi
unzip waifu2x-ncnn-vulkan.zip
rm waifu2x-ncnn-vulkan.zip
find . -name 'waifu2x*' -maxdepth 1 -exec mv {} waifu2x-ncnn-vulkan \;


# Waifu2x NCNN Vulkan
if [[ $OS == 'linux' ]]; then
    echo -e "installing latest realsr-ncnn-vulkan for linux\n"
    curl -s https://api.github.com/repos/nihui/realsr-ncnn-vulkan/releases/latest | sed -n 's/.*"browser_download_url": "\(.*ubuntu\.zip\)".*/\1/p' | xargs -n1 curl -o realsr-ncnn-vulkan.zip -OL
else
    echo -e "installing latest realsr-ncnn-vulkan for mac\n"
    curl -s https://api.github.com/repos/nihui/realsr-ncnn-vulkan/releases/latest | sed -n 's/.*"browser_download_url": "\(.*macos\.zip\)".*/\1/p' | xargs -n1 curl -o realsr-ncnn-vulkan.zip -OL
fi

unzip realsr-ncnn-vulkan.zip
rm realsr-ncnn-vulkan.zip
find . -name 'realsr*' -maxdepth 1 -exec mv {} realsr-ncnn-vulkan \;

# create executable_config file
# printf "ffmpeg: \"$ffmpeg\"\nffprobe: \"$ffprobe\"\ndandere2x_cpp: \"$dandere2x_cpp\"\nwaifu2x_vulkan: \"$waifu2x_vulkan\"\nwaifu2x_converter_cpp: \"$waifu2x_converter_cpp\"\nwaifu2x_caffe: \"$waifu2x_caffe\"\nrealsr_ncnn_vulkan: \"$realsr_vulkan\"" > ../config_files/executable_paths.yaml

# create workspace folder (this needs to exist I think?)
cd .. 
mkdir -p workspace
echo "setup successful. install the requirements with pip3 install -r requirements.txt, preferably in a a virtual environment, then run python3 main.py"
