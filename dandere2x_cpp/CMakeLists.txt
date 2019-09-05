cmake_minimum_required(VERSION 3.10.2)
project(dandere2x_cpp)

set(CMAKE_CXX_STANDARD 14)

set(CMAKE_BUILD_TYPE Release)
set(CMAKE_CXX_FLAGS_RELEASE "-O3")
set(CMAKE_CXX_FLAGS_RELEASE "-ffast-math ${CMAKE_C_FLAGS_RELEASE}")

find_package(OpenMP)
if (OPENMP_FOUND)
    set (CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
    set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
    set (CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
endif()


# enable this flag if compiling with mingw.
# note mingw doesn't work at the moment - rename(..,..) doesn't overwrite file
# which is needed by d2x.

#set(CMAKE_CXX_STANDARD_LIBRARIES "-static-libgcc -static-libstdc++ -lwsock32 -lws2_32 ${CMAKE_CSS_STANDARD_LIBRARIES}")

include_directories(src)
include_directories(src/BlockMatch)
include_directories(src/Dandere2xUtils)
include_directories(src/Image)
include_directories(src/Image/DebugImage)
include_directories(src/PFrame)
include_directories(src/Plugins/Correction)
include_directories(src/Plugins/PFrame/Residual)

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
        src/Plugins/Correction/Correction.cpp
        src/Plugins/Correction/Correction.h
        src/Plugins/PFrame/Residual/ResidualBlocks.h
        src/Plugins/PFrame/Residual/Residual.cpp
        src/Plugins/PFrame/Residual/Residual.h
        src/Plugins/PFrame/PFrame.cpp
        src/Plugins/PFrame/PFrame.h
        src/Driver.h
        src/main.cpp
        CMakeLists.txt src/Plugins/Fade/Fade.h src/Plugins/Fade/Fade.cpp src/BlockMatch/ExhaustiveSearch.h)
