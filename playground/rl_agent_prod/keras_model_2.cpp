#include <iostream>
#include <vector>
#include <string>
#include <fdeep/fdeep.hpp>
#include <stdlib.h>

class KerasModel {
    //auto model = fdeep::load_model(argv[1]);
    public:
        void bar() {
            std::cout << "Hello" << std::endl;
        }
};

extern "C" {
    KerasModel* KerasModel_new(){ return new KerasModel(); }
    void KerasModel_bar(KerasModel* kerasmodel){ kerasmodel->bar(); }
}