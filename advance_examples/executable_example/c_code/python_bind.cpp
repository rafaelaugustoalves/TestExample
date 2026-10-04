#include <pybind11/pybind11.h>
#include <main.h>

namespace py = pybind11;

PYBIND11_MODULE(examplepybind, m, pybind11::mod_gil_not_used()) {
    m.def("add_two_numbers", &add_two_numbers, "A function that adds two numbers");
}
