cmake_minimum_required(VERSION 3.15)
project(cpp_rework)

set(CMAKE_CXX_STANDARD 17)

add_executable(cpp_rework main.cpp frame/Frame.cpp frame/Frame.h math/MSE_Functions.h math/MSE_Functions.cpp math/SSIM_Function.cpp math/SSIM_Function.h)