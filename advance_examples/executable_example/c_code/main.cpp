#include <iostream>
#include <stdexcept>
#include <stdlib.h>
#include <string>
#include <main.h>

float main(int argc, char *argv[]) {
    if (argc != 3) {
        std::string message = "Exactly two parameters are required";
        std::cout << message;
        throw std::invalid_argument(message);
    }

    float val1 = std::stof(argv[1]);
    float val2 = std::stof(argv[2]);
    auto result = add_two_numbers(val1, val2);

    std::cout << result;

    return result;
}

float add_two_numbers(float val1, float val2) {
    auto result = val1 + val2;
    return result;
}
