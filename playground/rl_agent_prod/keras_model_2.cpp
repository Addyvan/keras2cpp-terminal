#include <iostream>
#include <vector>
#include <string>
#include <fdeep/fdeep.hpp>
#include <stdlib.h>

class KerasModel {
    
    public:
        void init(string model_path) {
            const auto model = fdeep::load_model(argv[1]);
        }
    
    
};

extern "C" {
    KerasModel* KerasModel_new(){ return new KerasModel(); }
    void KerasModel_init(KerasModel* kerasmodel, string model_path){ kerasmodel->init(model_path); }
}