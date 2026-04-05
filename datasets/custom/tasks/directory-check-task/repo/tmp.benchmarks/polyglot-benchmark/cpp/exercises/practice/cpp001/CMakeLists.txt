cmake_minimum_required(VERSION 3.10)
project(cpp001)
set(CMAKE_CXX_STANDARD 20)

find_package(GTest REQUIRED)

add_executable("cpp001"
    cpp001_test.cpp
)

target_compile_options(cpp001 PRIVATE -include${CMAKE_CURRENT_SOURCE_DIR}/cpp001.cpp)

target_link_libraries("cpp001"
    GTest::GTest
    GTest::Main
    pthread
)