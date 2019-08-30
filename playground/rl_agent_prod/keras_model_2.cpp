#include <iostream>
#include <vector>
#include <string>
#include <fdeep/fdeep.hpp>
#include <stdlib.h>

class KerasModel {
    
    private:
        std::string model_path;
        //fdeep::model model;
    public:

        KerasModel () {
            this->model_path = "default";
        }

        KerasModel (const std::string& model_path) {
            std::cout << model_path << std::endl;
            this->model_path = model_path;
        }

        /*
        void init(const std::string& model_path) {
            std::cout << "runs here " << std::endl;
            std::cout << model_path << std::endl;
            this->model = fdeep::load_model(model_path);
        }
        */

    
};



extern "C" {
    KerasModel* KerasModel_new(const std::string& model_path){ return new KerasModel(model_path); }
    //void KerasModel_init(KerasModel* kerasmodel, const std::string& model_path){ kerasmodel->init(model_path); }
}