//
// Created by https://github.com/CardinalPanda
//
//Licensed under the GNU General Public License Version 3 (GNU GPL v3),
//    available at: https://www.gnu.org/licenses/gpl-3.0.txt

#ifndef DANDERE2X_IMAGE_H
#define DANDERE2X_IMAGE_H

#include <iostream>
#include <vector>
#include <cmath>
#include <exception>
#include <stdexcept>
#include "stb_image.h"


/*
 * Description:
 *
 * A simple wrapper for the stb_image library for Dandere2x compression.
 *
 * The primary use of this class is to make loading an image and preform computations
 * on an image easier, however, it does not have the capabilities for saving images.
 *
 * Heavily inspired by Princeton's Image API library.
 *
 * https://algs4.cs.princeton.edu/code/edu/princeton/cs/algs4/Picture.java.html
 *
 * More in depth:
 *
 * stb_image loads an image from a string into a very, long array. Preforming
 * computations on an array like this is annoying, so this wrapper makes getting
 * and setting colors easier by having the user go refer to (x,y) coordinates
 * rather than traversing the 1D array.
 *
 *
 * To do:
 *
 * - Implement a writing function (need to get stb_save to work)
 *
 *
 *
 */
class Image {
public:
    struct Color {
        unsigned char r;
        unsigned char g;
        unsigned char b;
    };

    int height;
    int width;

    Image(std::string file_name);

    ~Image();

    Color get_color(int x, int y);

    void set_color(int x, int y, Color color);

private:
    unsigned char *stb_image;

};


#endif //DANDERE2X_IMAGE_H
