#!/bin/bash

# this file will compile and move the 
# dandere2x_cpp binary to the correct
# default path. obviously by the name
# of this file, this is Linux/sh only

# note this have a few dependencies
# mostly cmake, make and a compiler
# I don't know much about these tbh

# you should have them by defaults
# I can say that for an Arch based 
# system everything is in the base
# devel package and for Ubuntu sys
# the package build-essential IIRC

# the script auto cds into its root path
# so you can run this from outside paths
# without any problem and it should work

# to run this script "sh build_linux.sh"

DIRECTORY=$(cd `dirname $0` && pwd)

cd $DIRECTORY

mkdir -p externals

cd ../dandere2x_cpp

cmake CMakeLists.txt
make -j$(expr $(nproc) \+ 1)

mv ../dandere2x_cpp/dandere2x_cpp ../src/externals/dandere2x_cpp

printf "\n  Done!\n\n"