//
// Created by Tyler on 4/25/2021.
//

#ifndef CPP_REWORK_DANDERE2X_UTILITIES_H
#define CPP_REWORK_DANDERE2X_UTILITIES_H

#include <string>
#include <iostream>
#include <fstream>
#include <chrono>
#include <thread>

namespace dandere2x_utilities {

    bool debug_enabled(){
        return false;
    }

    char separator() {
#ifdef __CYGWIN__
        return '\\';
#else
        return '/';
#endif
    }

    bool file_exists(const std::string &name) {
        std::ifstream f(name.c_str());
        return f.good();
    }

    void write_empty(std::string input);

    void wait_for_file(const std::string &name) {
        int count = 0;
        while (true) {
            if (file_exists(name)) {
                break;
            }
            std::this_thread::sleep_for(std::chrono::milliseconds(100));
            count++;
            if (std::remainder(count, 10) == 0) {
                std::cout << "waiting for file more than 1 sec " << name << std::endl;
                count = 0;
            }
        }
    }

}
#endif //CPP_REWORK_DANDERE2X_UTILITIES_H
