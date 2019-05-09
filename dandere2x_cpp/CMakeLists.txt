#I build this on cygwin
cmake_minimum_required(VERSION 3.14)
project(dandere2x)

set(CMAKE_BUILD_TYPE Release)
set(CMAKE_CXX_FLAGS_DEBUG "-g")
set(CMAKE_CXX_FLAGS_RELEASE "-O3")


set(CMAKE_CXX_FLAGS_RELEASE "-ffast-math ${CMAKE_C_FLAGS_RELEASE}")
set(CMAKE_CXX_STANDARD_LIBRARIES "-static-libgcc -static-libstdc++ -lwsock32 -lws2_32 ${CMAKE_CSS_STANDARD_LIBRARIES}")

add_executable(dandere2x src/main.cpp src/Image/stb_image.h src/Image/Image.cpp src/Image/Image.h src/BlockMatch/DiamondSearch.h src/BlockMatch/Block.h src/Image/ImageUtils.h src/PFrame/PFrame.cpp src/PFrame/PFrame.h src/Dandere2xUtils/Dandere2xUtils.h src/PFrame/Difference/DifferenceBlocks.h src/PFrame/Difference/Differences.cpp src/PFrame/Difference/Differences.h src/PFrame/Correction/Correction.cpp src/PFrame/Correction/Correction.h src/Dandere2xUtils/Dandere2xUtils.cpp src/Driver.h src/Image/DebugImage/lodepng.cpp src/Image/DebugImage/lodepng.h src/Image/DebugImage/DebugImage.h)