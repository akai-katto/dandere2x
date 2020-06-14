#include "testcases/BlockMatchingMemoizationTestCases.h"
#include "plugins/block_plugins/block_matching_algorithms/DiamondSearch.h"
#include "plugins/block_plugins/block_matching_algorithms/ExhaustiveSearch.h"

#include <iostream>

int main(){
    Frame input1 = Frame("/home/owo/Documents/git_stuff/tremex_rework/dandere2x-new/samples/frame194.png");
    Frame input2 = Frame("/home/owo/Documents/git_stuff/tremex_rework/dandere2x-new/samples/frame193.png");
    ExhaustiveSearch searcher = ExhaustiveSearch(input1, input2, 30);
//    Block result = searcher.match_block(60,95);

    int x, y, width, height, block_size;
    x = 0;
    y = 0;
    width = 400;
    height = 400;
    block_size = 30;
//
//    for (int x = 0; x < width / block_size; x++) {
//        for (int y = 0; y < height / block_size; y++) {
//            Block result = searcher.match_block(x * block_size,y * block_size);
//        }
//    }
//    cout << "SUM: " << MSE_FUNCTIONS::compute_mse(input1, input2, 50,50,50,50,30) << endl;

//    searcher.match_block(100,100);
//    searcher.match_block(100,100);

    searcher.mse_blocks(100,100,100,105);
    searcher.mse_blocks(100,105,100,100);

    cout << "Computations Saved " << searcher.computations_saved << endl;
    cout << "Total Calls Saved " << searcher.total_calls << endl;
}