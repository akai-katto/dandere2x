//
// Created by https://github.com/CardinalPanda
//
//Licensed under the GNU General Public License Version 3 (GNU GPL v3),
//    available at: https://www.gnu.org/licenses/gpl-3.0.txt

#ifndef DANDERE2X_CPP_EXHAUSTIVESEARCH_H
#define DANDERE2X_CPP_EXHAUSTIVESEARCH_H

#include <vector>
#include <algorithm>    // std::sort
#include <iostream>

#include "Block.h"
#include "../Image/Image.h"
#include "../Image/Image.h"
#include "../Image/ImageUtils.h"

using namespace std;


class ExhaustiveSearch {
public:

    std::vector<Block::Point> static createSearchVector(int centx, int centy, int width, int height, int maxBox) {

        std::vector<Block::Point> list = std::vector<Block::Point>();

        for (int x = centx - maxBox; x < centx + maxBox; x++) {
            for (int y = centy - maxBox; y < centy + maxBox; y++) {
                if ((x > 0 || x < width) || (y > 0 || y < height)) {
                    Block::Point point;
                    point.x = x;
                    point.y = y;
                    list.push_back(point);
                }
            }
        }

        return list;

    }


// Diamond search but a greater jump radius (15 rather than 9)
    static Block
    exhaustive_search(Image &desired_image, Image &input_image, int initial_x, int initial_y, int block_size) {
        int searchRadius = 25;
        vector<Block::Point> test = createSearchVector(initial_x, initial_y, 1920, 1080, searchRadius);
        vector<Block> blockSum = vector<Block>();

        //find initial disp
        for (int x = 0; x < test.size(); x++) {
            double average = ImageUtils::mse(desired_image, input_image, initial_x, initial_y, test[x].x, test[x].y,
                                             block_size); //seperate var for debuggin
            Block b = Block(initial_x, initial_y, test[x].x, test[x].y,
                  average);
            blockSum.push_back(b);

        }

        auto smallestBlock = std::min_element(blockSum.begin(), blockSum.end());
        return *smallestBlock;
    }

};


#endif //DANDERE2X_CPP_EXHAUSTIVESEARCH_H
