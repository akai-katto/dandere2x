#include <iostream>
#include "frame/Frame.h"

int main() {

    Frame frame = Frame("/home/owo/Pictures/screen.png");

    Frame::Color col = frame.get_color(100000,5);

    std::cout << "Hello, World!" << std::endl;
    return 0;
}
