class Function(object):
    def __init__(self, name, directory, index, requirements=None, functions=None, modules=None):
        self._name = name
        self._directory = directory
        self._index = index
        self._requirements = requirements
        self._functions = functions
        self._lib = ''
        self._modules = modules

    def get_name(self):
        return self._name

    def get_directory(self):
        return self._directory

    def get_index(self):
        return self._index

    def get_index_file(self):
        return self._name + '_' + self._index.split('.')[0] + '.py'

    def get_index_handler(self):
        return self._index.split('.')[1]

    def get_requirements(self):
        return self._requirements

    def get_functions(self):
        return self._functions

    def set_functions(self, services):
        self._functions = services

    def add_function(self, service):
        if not self._functions:
            self._functions = []
        self._functions.append(service)

    def add_requirement(self, requirement):
        if not self._requirements:
            self._requirements = []
        self._requirements.append(requirement)

    def set_name(self, name):
        self._name = name

    def set_index(self, index):
        self._index = index

    def set_directory(self, directory):
        self._directory = directory

    def set_lib(self, lib):
        self._lib = lib

    def get_lib(self):
        return self._lib

    def set_requirements(self, requirements):
        self._requirements = requirements

    def get_modules(self):
        return self._modules

    def set_modules(self, modules):
        self._modules = modules

