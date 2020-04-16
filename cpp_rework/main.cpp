#include <iostream>
#include "frame/Frame.h"
#include "math/MSE_Functions.h"
#include <chrono>

using namespace std::chrono;


//int main() {
//
//
//    auto total_start = high_resolution_clock::now();
//
//    Frame frame1 = Frame("/home/owo/Pictures/Screenshot from 2020-04-09 06-52-23.png");
//    Frame frame2 = Frame("/home/owo/Pictures/Screenshot from 2020-04-12 02-21-12.png");
//
//    int block_size = 30;
//    double sum = 0;
//
//
////#pragma omp parallel for reduction(+:sum)
//    for (int i = 0; i < 3840; i++) {
//        for (int j = 0; j < 3840; j++) {
//            sum += (j * j);
//        }
//    }
//
//
//    auto stop = high_resolution_clock::now();
//    auto duration = duration_cast<microseconds>(stop - total_start);
//    cout << "Calculation time for frame :  " <<  duration.count() << endl;
//    std::cout << "Hello, World!" << std::endl;
//    return 0;
//}

#include <cmath>

int main() {

    auto total_start = high_resolution_clock::now();

    const int size = 10000;
    double sinTable[size];
    double sum = 0;

    #pragma omp parallel for
    for (int n = 0; n < size; ++n) {
        int added_val = 0;
        for(int i = 0; i < size; i++) {
            added_val += n * i;
        }
        sinTable[n] = std::sin(2 * M_PI * added_val);
        sum += sinTable[n];
    }

    auto stop = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(stop - total_start);

    cout << "sum: " << sum  << endl;
    cout << "Calculation time for frame :  " << duration.count() << endl;
    // the table is now initialized
}