class Config(object):
    def __init__(self, name, lib, tests=None, functions=None, lib_name='', dist='', base_path=''):
        self._name = name
        self._lib = lib
        self._tests = tests
        self._functions = functions
        self._lib_name = lib_name
        self._dist = dist
        self._base_path = base_path

    def get_name(self):
        return self._name

    def get_lib(self):
        return self._lib

    def get_functions(self):
        return self._functions

    def set_functions(self, services):
        self._functions = services

    def add_function(self, service):
        if not self._functions:
            self._functions = []

        self._functions.append(service)

    def has_function(self, service_name):
        if not self._functions or len(self._functions) == 0:
            return False

        for service in self._functions:
            if service.get_name() == service_name:
                return True

        return False

    def get_function(self, service):
        if self.has_function(service):
            for s in self._functions:
                if s.get_name() == service:
                    return s
        return None

    def get_lib_name(self):
        return self._lib_name

    def set_lib_name(self, name):
        self._lib_name = name

    def get_dist(self):
        return self._dist

    def set_dist(self, dist):
        self._dist = dist

    def set_base_path(self, path):
        self._base_path = path

    def get_base_path(self):
        return self._base_path

