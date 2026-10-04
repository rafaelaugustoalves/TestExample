cmake_minimum_required(VERSION 4.4)

project(ExecutableExample)

SET(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}")
SET(CMAKE_LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}")
SET(CMAKE_ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}")
SET(CMAKE_PDB_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}")

add_executable(SumNumbers)
target_sources(SumNumbers PRIVATE main.cpp)
target_compile_features(SumNumbers PRIVATE cxx_std_11)
target_include_directories(SumNumbers PRIVATE ${CMAKE_SOURCE_DIR})

find_package(Python COMPONENTS Interpreter Development)
find_package(pybind11 CONFIG)

pybind11_add_module(examplepybind main.cpp python_bind.cpp)
target_include_directories(examplepybind PUBLIC ${CMAKE_SOURCE_DIR})
