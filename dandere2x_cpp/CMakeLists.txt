cmake_minimum_required(VERSION 3.14)
project(dandere2x_cpp)

set(CMAKE_CXX_STANDARD 14)

set(CMAKE_BUILD_TYPE Release)
set(CMAKE_CXX_FLAGS_RELEASE "-O3")
set(CMAKE_CXX_FLAGS_RELEASE "-ffast-math ${CMAKE_C_FLAGS_RELEASE}")
set(CMAKE_CXX_STANDARD_LIBRARIES "-static-libgcc -static-libstdc++ -lwsock32 -lws2_32 ${CMAKE_CSS_STANDARD_LIBRARIES}")

include_directories(src)
include_directories(src/BlockMatch)
include_directories(src/Dandere2xUtils)
include_directories(src/Image)
include_directories(src/Image/DebugImage)
include_directories(src/PFrame)
include_directories(src/PFrame/Correction)
include_directories(src/PFrame/Difference)

add_executable(dandere2x_cpp
        src/BlockMatch/Block.h
        src/BlockMatch/DiamondSearch.h
        src/Dandere2xUtils/Dandere2xUtils.cpp
        src/Dandere2xUtils/Dandere2xUtils.h
        src/Image/DebugImage/DebugImage.h
        src/Image/DebugImage/lodepng.cpp
        src/Image/DebugImage/lodepng.h
        src/Image/Image.cpp
        src/Image/Image.h
        src/Image/ImageUtils.h
        src/Image/stb_image.h
        src/PFrame/Correction/Correction.cpp
        src/PFrame/Correction/Correction.h
        src/PFrame/Difference/DifferenceBlocks.h
        src/PFrame/Difference/Differences.cpp
        src/PFrame/Difference/Differences.h
        src/PFrame/PFrame.cpp
        src/PFrame/PFrame.h
        src/Driver.h
        src/main.cpp
        CMakeLists.txt)
