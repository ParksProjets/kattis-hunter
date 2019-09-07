"""

Replace general sections.

Copyright (C) 2019, Guillaume Gonnet
This project is under the MIT license.

"""


# Special headers to include in main C++ file.
HEADERS = """

#include <chrono>

"""


# Player class attributes.
ATTRIBUTES = """

void setupEnvSkip(const GameState &pState);

bool mSkipThisEnv = false;
int mCacheNumber = 0;
int mCacheIndex = 0;
int mBaseShift = 1;

"""


# Code to include in every build.
STATIC_CODE = """

void WaitForMs(int target)
{
    auto begin = std::chrono::high_resolution_clock::now();

    while (true) {
        auto end = std::chrono::high_resolution_clock::now();
        auto dur = end - begin;
        auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(dur).count();
        if (ms >= target)
            exit(1);
    }
}

"""
