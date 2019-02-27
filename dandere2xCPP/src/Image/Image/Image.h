//
// Created by linux on 11/11/18.
//

#ifndef LODEPNG_IMAGE_H
#define LODEPNG_IMAGE_H
#include <cmath>

#define STB_IMAGE_IMPLEMENTATION
#include "../Image/stb_image.h"

#include <iostream>
#include <vector>

#include <exception>
#include <stdexcept>


//a wrapper for the stb_image library
//so code can be ported between java / c++ faster.
//also readible
class Image {
public:
    
    struct Color {
        unsigned char r;
        unsigned char g;
        unsigned char b;
    };
    
    int height;
    int width;
    unsigned char* input;

    static double deltaC(const Color &colorA, const Color &colorB) {
        int r1 = (int) colorA.r;
        int r2 = (int) colorB.r;
        
        int g1 = (int) colorA.g;
        int g2 = (int) colorB.g;
        
        int b1 = (int) colorA.b;
        int b2 = (int) colorB.b;
        
        return sqrt(pow((r2 - r1), 2) + pow((g2 - g1), 2) + pow((b2 - b1), 2));
    }
    

    Image(std::string filename) {
    	unsigned char* rgb; //the raw pixels
        int width, height, bpp;
        //decode
        input = stbi_load( filename.c_str(), &width, &height, &bpp, 3 );

        this->input = input;
        this->height = height;
        this->width = width;
        //the pixels are now in the vector "image", 4 bytes per pixel, ordered RGBARGBA..., use it as texture, draw it, ...
    }
    
    ~Image(){
    	stbi_image_free(input);
    }


    Image(int x, int y) {

    }

    Image(){

    }
    
    Color getColor(int x, int y) {
        if (x > width - 1 || y > height - 1 || x < 0 || y < 0){
            throw std::invalid_argument("invalid dimensions");
        }


        Color color;
        color.r = input[x * 3 + 3 * y * width];
        color.g = input[x * 3 + 3 * y * width + 1];
        color.b = input[x * 3 + 3 * y * width + 2];
        
        return color;
    }
    
    Color getColorNoThrow(int x, int y) {
        if (x > width - 1 || y > height - 1 || x < 0 || y < 0){
            Color color;
            color.r = 0;
            color.g = 0;
            color.b = 0;
        }
        
        Color color;
        color.r = input[x * 3 + 3 * y * width];
        color.g = input[x * 3 + 3 * y * width + 1];
        color.b = input[x * 3 + 3 * y * width + 2];

        return color;
    }
    
    void setColor(int x, int y, Color color) {
        if (x > width - 1 || y > height - 1 || x < 0 || y < 0){

            std::cout << "ERROR, set color out of bounds!";
            throw std::invalid_argument("set color has invalid dimensions");
        }
        
        
        input[x * 3 + 3 * y * width] = color.r;
        input[x * 3 + 3 * y * width + 1] = color.g;
        input[x * 3 + 3 * y * width + 2] = color.b;
        
    }
    

    
    //currently deprecated as saving is no longer handled through
    //c++, but rather java.
    void save(const char* dest, int input = 50){

    }

    void save(std::string dest, int input = 50){

    }
    
    


};


#endif //LODEPNG_IMAGE_H
