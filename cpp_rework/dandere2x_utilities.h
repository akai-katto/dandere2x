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
#include <unistd.h>

// Need to include <windows.h> for mingw64 for sleep.
#ifdef __MINGW64__
#include <windows.h>
#include "easyloggingpp/easylogging++.h"
#endif

namespace dandere2x_utilities {

    bool debug_enabled();

    char separator();

    bool file_exists(const std::string &name);

    void wait_for_file(const std::string &name);

}

#endif //CPP_REWORK_DANDERE2X_UTILITIES_H
