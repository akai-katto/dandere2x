/*
 * Computation class used for various CImage stuff, such as calculating
 * MSE or Variance between two images.
 */

/* 
 * File:   CImageUtils.h
 * Author: linux
 *
 * Created on December 16, 2018, 4:38 PM
 */

#ifndef CIMAGEUTILS_H
#define CIMAGEUTILS_H

#include "../Image/Image.h"

class CImageUtils{
public:
    
    inline static double deltaC(const Image::Color &colorA, const Image::Color &colorB) {

        int r1 = (int) colorA.r;
        int r2 = (int) colorB.r;
        
        int g1 = (int) colorA.g;
        int g2 = (int) colorB.g;
        
        int b1 = (int) colorA.b;
        int b2 = (int) colorB.b;
        
        return sqrt(pow((r2 - r1), 2) + pow((g2 - g1), 2) + pow((b2 - b1), 2));
    }
    
    static Image::Color average(const Image::Color &colorA, const Image::Color &colorB) {
        
        unsigned char r = (unsigned char) sqrt((((int) colorA.r + 1) * ((int) colorB.r)+1));
        unsigned char g = (unsigned char) sqrt((((int) colorA.g+1) * ((int) colorB.g)+1)); 
        unsigned char b = (unsigned char) sqrt((((int) colorA.b+1) * ((int) colorB.b)+1)); 
        
        Image::Color color;
        
        
        
        color.r = r;
        color.g = g;
        color.b = b;
        
        return color;
    }
    
    
    
    
    /**Calculuate psnr
     *
     * See https://en.wikipedia.org/wiki/Peak_signal-to-noise_ratio
     */
    static double calculate(Image &imageA,
    Image &imageB){
        
        double sum = 0;
        
        for(int x = 0; x < imageA.width; x++){
            for(int y = 0; y < imageA.height; y++){
                sum += pow(deltaC(imageA.getColor(x,y), imageB.getColor(x,y)),2);
            }
        }
        
        sum /= (imageA.height * imageA.width);
        
        double result = 20 * log10(255) - 10 * log10(sum);
        return result;
    }
    
    /**
     Calculate a mean square error between two blocks in two different images at two locations
     see https://en.wikipedia.org/wiki/Mean_squared_error
     */
    
    
    inline static double mean(Image &imageA,Image &imageB, 
    int initialX, int initialY,
    int variableX, int variableY, 
    int blockSize) {
        
        double sum = 0;
        try {
            for (int x = 0; x < blockSize; x++)
                for (int y = 0; y < blockSize; y++)
                    sum += deltaC(imageA.getColor(initialX + x, initialY + y),
                            imageB.getColor(variableX + x, variableY + y));
        }
        catch (std::logic_error e) {
            //std::cout << "caught logic error" << std::endl;
            return 9999;
        }
        
        sum /= blockSize * blockSize;
        
        return sum;
    }
    
    inline static double sumAverage(Image &imageA,Image &imageB, 
    int initialX, int initialY,
    int variableX, int variableY, 
    int blockSize) {
        
        double var = mean(imageA, imageB, initialX, initialY, variableX, variableY, blockSize);
        double sum = 0;
        try {
            for (int x = 0; x < blockSize; x++)
                for (int y = 0; y < blockSize; y++)
                    sum += pow(deltaC(imageA.getColor(initialX + x, initialY + y),
                            imageB.getColor(variableX + x, variableY + y)),2);
        }
        catch (std::logic_error e) {
            //std::cout << "caught logic error" << std::endl;
            return 9999;
        }
        
        sum /= blockSize * blockSize;
        
        return sum;
    }
    
};
#endif /* CIMAGEUTILS_H */

