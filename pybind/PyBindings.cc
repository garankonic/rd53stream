#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "decode/interface/DecoderBase.h"
#include "decode/interface/SimpleStreamDecoder.h"
#include "encode/interface/EventEncoder.h"
#include "util/ChipIdentifier.h"

namespace py = pybind11;

PYBIND11_MODULE(pybindings, m) {
    m.doc() = "pybind11 example plugin"; // optional module docstring

    py::class_<SimpleStreamDecoder>(m, "SimpleStreamDecoder")
        .def(py::init())
        .def("load_file", &SimpleStreamDecoder::load_file)
        .def("decode", &SimpleStreamDecoder::decode);

    py::class_<ChipIdentifier>(m, "ChipIdentifier")
        .def(py::init<uint16_t, uint16_t, uint16_t, uint16_t>());

    py::class_<EncodedEvent>(m, "EncodedEvent")
        .def(py::init())
        .def("is_empty", &EncodedEvent::is_empty)
        .def("print", &EncodedEvent::print)
        .def("get_next_chip", &EncodedEvent::get_next_chip);

    py::class_<EventEncoder>(m, "EventEncoder")
        .def(py::init<std::string>())
        .def("get_next_event", &EventEncoder::get_next_event);

}
