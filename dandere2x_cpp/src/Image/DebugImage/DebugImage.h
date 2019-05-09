
//
// Created by https://github.com/CardinalPanda
//
//Licensed under the GNU General Public License Version 3 (GNU GPL v3),
//    available at: https://www.gnu.org/licenses/gpl-3.0.txt

#ifndef DANDERE2X_DEBUGIMAGE_H
#define DANDERE2X_DEBUGIMAGE_H

#include <cmath>
#include "lodepng.h"
#include "../Image.h"
#include <iostream>
#include <vector>

#include <exception>
#include <stdexcept>


//Simple wrapper to save images using PNG's.

class DebugImage {
public:

   static DebugImage create_debug_from_image(Image &input) {

        DebugImage out_image = DebugImage(input.width, input.height);

        for(int x = 0; x < input.width; x++){
            for(int y = 0; y < input.height; y++){
                out_image.setColor(x,y,input.get_color(x,y));
            }
        }

        return out_image;
    }

    int height;
    int width;
    std::vector<unsigned char> input;

    static double deltaC(const Image::Color &colorA, const Image::Color &colorB) {
        int r1 = (int) colorA.r;
        int r2 = (int) colorB.r;

        int g1 = (int) colorA.g;
        int g2 = (int) colorB.g;

        int b1 = (int) colorA.b;
        int b2 = (int) colorB.b;

        return sqrt(pow((r2 - r1), 2) + pow((g2 - g1), 2) + pow((b2 - b1), 2));
    }


    DebugImage(const char *filename) {
        std::vector<unsigned char> input; //the raw pixels
        unsigned width, height;

        //decode
        unsigned error = lodepng::decode(input, width, height, filename);

        //if there's an error, display it
        if (error) std::cout << "decoder error " << error << ": " << lodepng_error_text(error) << std::endl;


        this->input = input;
        this->height = height;
        this->width = width;
        //the pixels are now in the vector "image", 4 bytes per pixel, ordered RGBARGBA..., use it as texture, draw it, ...
    }

    DebugImage(std::string filename) {
        std::vector<unsigned char> input; //the raw pixels
        unsigned width, height;

        //decode
        unsigned error = lodepng::decode(input, width, height, filename.c_str());

        //if there's an error, display it
        if (error) std::cout << "decoder error " << error << ": " << lodepng_error_text(error) << std::endl;


        this->input = input;
        this->height = height;
        this->width = width;
        //the pixels are now in the vector "image", 4 bytes per pixel, ordered RGBARGBA..., use it as texture, draw it, ...
    }


    //used to create an empty image
    DebugImage(unsigned height, unsigned width) {
        this->height = width;
        this->width = height;
        input = std::vector<unsigned char>(height * width * 4);
        for (int x = 0; x < height * width; x++) {
            input[x * 4] = 0;
            input[x * 4 + 1] = 0;
            input[x * 4 + 2] = 0;
            input[x * 4 + 3] = 255;
        }
    }

    DebugImage(){
    }

    Image::Color getColor(int x, int y) {
        if (x > width - 1 || y > height - 1 || x < 0 || y < 0){
            throw std::invalid_argument("invalid");
        }


        Image::Color color;
        color.r = input[x * 4 + 4 * y * width];
        color.g = input[x * 4 + 4 * y * width + 1];
        color.b = input[x * 4 + 4 * y * width + 2];

        return color;
    }

    Image::Color getColorNoThrow(int x, int y) {
        if (x > width - 1 || y > height - 1 || x < 0 || y < 0){
            Image::Color color;
            color.r = 0;
            color.g = 0;
            color.b = 0;
        }

        Image::Color color;
        color.r = input[x * 4 + 4 * y * width];
        color.g = input[x * 4 + 4 * y * width + 1];
        color.b = input[x * 4 + 4 * y * width + 2];

        return color;
    }

    void setColor(int x, int y, Image::Color color) {
        if (x > width - 1 || y > height - 1 || x < 0 || y < 0){

            std::cout << "ERROR, set color out of bounds!";
            throw std::invalid_argument("set color has invalid dimensions");
        }


        input[x * 4 + 4 * y * width] = color.r;
        input[x * 4 + 4 * y * width + 1] = color.g;
        input[x * 4 + 4 * y * width + 2] = color.b;

    }


    void save(const char* dest){
        std::vector<unsigned char> png;

        unsigned error = lodepng::encode(png, this->input, this->width, this->height);
        if (!error) lodepng::save_file(png, dest);

        //if there's an error, display it
        if (error) std::cout << "encoder error " << error << ": " << lodepng_error_text(error) << std::endl;
    }

    void save(std::string dest){
        std::vector<unsigned char> png;

        unsigned error = lodepng::encode(png, this->input, this->width, this->height);
        if (!error) lodepng::save_file(png, dest.c_str());

        //if there's an error, display it
        if (error) std::cout << "encoder error " << error << ": " << lodepng_error_text(error) << std::endl;
    }


};


#endif //DANDERE2X_DEBUGIMAGE_H
