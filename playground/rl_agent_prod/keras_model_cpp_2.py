from ctypes import cdll
lib = cdll.LoadLibrary('./libfoo.so')

class Foo(object):
    def __init__(self):
        self.obj = lib.KerasModel_new()

    def bar(self):
        lib.KerasModel_bar(self.obj)

if __name__ == "__main__":
    foo = Foo()
    foo.bar()