//
// Created by https://github.com/CardinalPanda
//
//Licensed under the GNU General Public License Version 3 (GNU GPL v3),
//    available at: https://www.gnu.org/licenses/gpl-3.0.txt


/**
 * Description:
 *
 * An iterative 'super' implementation of diamond block matching.
 *
 * https://en.wikipedia.org/wiki/Block-matching_algorithm#Diamond_Search
 *
 *
 * Notes:
 *
 * - Iterative yielded better preformance than recursive
 * - 'Super' since it checks 15 points rather than 9 (decrease in preformance -> better blocks)
 *
 */
#ifndef DANDERE2X_DIAMONDSEARCH_H
#define DANDERE2X_DIAMONDSEARCH_H

#include <vector>
#include <algorithm>    // std::sort
#include "Block.h"
#include "../Image/Image.h"
#include "../Image/Image.h"
#include "../Image/ImageUtils.h"



class DiamondSearch {

public:
    struct Point {
        int x;
        int y;
    };


    //Flags the points that are out of bounds / not within the scope of the image.
    static bool flag_invalid_points(int x_bounds, int y_bounds, Point points[], int size, bool flagged[]) {

        int count = 0;
        for (int i = 0; i < size; i++) {
            if ((points[i].x > x_bounds) || (points[i].x < 0) ||
                (points[i].y > y_bounds) || (points[i].y < 0)) {
                flagged[i] = true;
                count++;
            }
        }

        return count != size;
    }


    /**
     * This is my really hacky solution to Diamond search, where in I implemented my own techniques.
     * https://en.wikipedia.org/wiki/Block-matching_algorithm#Diamond_Search
     *
     *
     */
    // Diamond search but a greater jump radius (15 rather than 9)
    static Block diamond_search_iterative_super(Image &image_A, Image &image_B,
                                                double min_mse,
                                                int initial_x, int initial_y,
                                                int x_origin, int y_origin,
                                                int box_size,
                                                int step_size,
                                                int max_checks) {

        int x_bounds = image_A.width;
        int y_bounds = image_A.height;

        double sum;

        std::vector<Block> blocks = std::vector<Block>();

        //create the points to be used in diamond searching
        Point point_array[15];

        for (int x = 0; x < max_checks; x++) {
            blocks.clear();

            //if we ran out of checks, return what we're at right now
            if (x == max_checks - 1) {
                double sum = ImageUtils::mse(image_A, image_B, initial_x, initial_y, x_origin, y_origin, box_size);
                return Block(initial_x, initial_y, x_origin, y_origin, sum);
            }

            //if step size is 0, return where we are at right now
            if (step_size <= 0) {
                double sum = ImageUtils::mse(image_A, image_B, initial_x, initial_y, x_origin, y_origin, box_size);
                return Block(initial_x, initial_y, x_origin, y_origin, sum);
            }

            //construct the list of "diamond" points to be checked if legal or not
            point_array[0].x = x_origin + step_size;
            point_array[0].y = y_origin;

            point_array[1].x = x_origin + step_size / 2;
            point_array[1].y = y_origin + step_size / 2;

            point_array[2].x = x_origin;
            point_array[2].y = y_origin + step_size;

            point_array[3].x = x_origin - step_size / 2;
            point_array[3].y = y_origin + step_size / 2;

            point_array[4].x = x_origin - step_size;
            point_array[4].y = y_origin;

            point_array[5].x = x_origin + step_size / 2;
            point_array[5].y = y_origin - step_size / 2;

            point_array[6].x = x_origin + step_size;
            point_array[6].y = y_origin;

            point_array[7].x = x_origin;
            point_array[7].y = y_origin;

            point_array[8].x = x_origin + step_size * 2;
            point_array[8].y = y_origin;

            point_array[9].x = x_origin + step_size;
            point_array[9].y = y_origin + step_size;

            point_array[10].x = x_origin;
            point_array[10].y = y_origin + step_size * 2;

            point_array[11].x = x_origin - step_size;
            point_array[11].y = y_origin + step_size;

            point_array[12].x = x_origin - step_size * 2;
            point_array[12].y = y_origin;

            point_array[13].x = x_origin + step_size;
            point_array[13].y = y_origin - step_size;

            point_array[14].x = x_origin + step_size * 2;
            point_array[14].y = y_origin;


            //Create an array that is used to signal if a point is "valid" or not, i.e if it is legal to visit.
            //In other words, we need to know the index of an array is allowed or not.

            bool flag_array[15] = {true};
            bool any_legal_points = flag_invalid_points(x_bounds, y_bounds, point_array, 14, flag_array);

            //flag invalid points returns a boolean if there are no valid points for diamond search to visit
            //therfore, return a 'null' block, (a block with a really high PSNR (peak signal to noise ratio), so it
            //will be ignored by the rest of the system
            if (!any_legal_points) //if the entire
                return Block(0, 0, 0, 0, 99999);

            //cycle through each point (if it's legal that is) and add it to the block vector.
            for (int j = 0; j < 15; j++) {
                if (!flag_array[j]) {
                    sum = ImageUtils::mse(image_A, image_B, initial_x, initial_y, point_array[j].x, point_array[j].y,
                                          box_size);

                    Block block = Block(initial_x, initial_y, point_array[j].x, point_array[j].y, sum);
                    blocks.push_back(block);
                }
            }

            //get the most promising block from the list (the one with the smallest 'sum'
            std::vector<Block>::iterator smallest_block = min_element(blocks.begin(), blocks.end());


            /** If the smallest block we found meets the MSE requirements, stop here*/
            if (smallest_block->sum <= min_mse){
                return *smallest_block;
            }


            /** Testing feature - if the smallest block is garishly larger than the minimum required,
             stop looking. */
            if (smallest_block->sum >= min_mse*min_mse*min_mse*min_mse*min_mse){
                return Block(0, 0, 0, 0, 10000);
            }

            if ((smallest_block->x_end == x_origin) && smallest_block->y_end == y_origin) {
                x_origin = smallest_block->x_end;
                y_origin = smallest_block->y_end;
                step_size /= 2;
                continue;
            }

            x_origin = smallest_block->x_end;
            y_origin = smallest_block->y_end;
        }

        //default
        return Block(0, 0, 0, 0, 10000);
    }


};


#endif //DANDERE2X_DIAMONDSEARCH_H
