#include <iostream>
#include <vector>
#include <string>
#include <fdeep/fdeep.hpp>
#include <stdlib.h>

class KerasModel {
    
    //fdeep::model model;
    public:

        void init(const std::string& model_path) {
            std::cout << "runs here " << std::endl;
            std::cout << model_path << std::endl;
            auto model = fdeep::load_model(model_path);
        }


    
    
};

extern "C" {
    KerasModel* KerasModel_new(){ return new KerasModel(); }
    void KerasModel_init(KerasModel* kerasmodel, const std::string& model_path){ kerasmodel->init(model_path); }
}