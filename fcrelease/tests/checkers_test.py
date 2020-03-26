import unittest

from fcrelease.function import Function
from fcrelease.checkers import function_directory_checker, function_depend_checker


class TestCheckers(unittest.TestCase):
    def test_service_directory_checker(self):
        function_directory_checker('./loader', 'test service')
        function_directory_checker('/', 'root service')

    def test_service_depend_checker(self):
        services = {
            'a': ['b'],
            'b': ['c'],
            'c': []
        }

        s = []
        for k in services:
            v = services[k]
            service = Function(k, '/', '')
            service.set_functions(v)
            s.append(service)

        function_depend_checker(s)
