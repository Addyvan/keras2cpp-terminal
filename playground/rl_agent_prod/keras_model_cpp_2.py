from ctypes import cdll
lib = cdll.LoadLibrary('./libfoo.so')

class Foo(object):
    def __init__(self):
        self.obj = lib.KerasModel_new()

    def init(self, model_path):
        lib.KerasModel_init(self.obj, model_path)

if __name__ == "__main__":
    foo = Foo()
    #model = foo.init("./fdeep_ping.json")

    #print(model)