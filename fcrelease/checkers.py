# encoding: utf-8

import subprocess
from os import path


def function_directory_checker(directory, function_name):
    error_msg = 'No such directory "%s", in service: %s'
    if not path.isdir(directory):
        raise NoSuchDirectoryInFunctionException(error_msg % (directory, function_name))


def function_depend_checker(functions):
    func_dist = {}
    for function in functions:
        func_dist[function.get_name()] = function.get_functions()

    for function in func_dist:
        depend = func_dist[function]
        for dep in depend:
            if dep == function:
                raise SelfReferenceFunctionException('self reference function: "%s"' % dep)

            if not dep or dep not in func_dist:
                raise NoSuchFunctionException('depend function "%s" not in functions(%s)' %
                                              (dep, ", ".join(func_dist.keys())))


def function_index_checker(index, function_name, base_path=''):
    if not index:
        raise TypeError('argument index required')

    index_file, handler = index.split('.')
    if not index_file.endswith('.py'):
        index_file += ".py"

    # index 文件 = <service_name>_<index>
    index_file = function_name + "_" + index_file
    index_file_path = path.join(base_path, index_file)
    if not path.isfile(index_file_path):
        raise NotFoundIndexFileException('No such index file "%s" in function: "%s"' % (index_file, function_name))

    grep = subprocess.Popen(['grep', '-q', '\\<def %s\\>' % handler, index_file_path], stdout=subprocess.PIPE)
    grep.communicate()

    if grep.returncode != 0:
        raise NoSuchHandlerException('no such handler "%s" in file "%s"' % (handler, index_file_path))


def function_module_checker(modules, function_name, base_path=''):
    for module in modules:
        module_path = path.join(base_path, module)

        if not path.exists(module_path):
            raise NoSuchModuleInFunctionException('no such module "%s" in "%s"' % (module, function_name))


def service_checker(exists, service):
    if not exists:
        raise UnknownFunctionException('unknown function "%s"' % service)


class NoSuchModuleInFunctionException(Exception):
    pass


class NoSuchHandlerException(Exception):
    pass


class NotFoundIndexFileException(Exception):
    pass


class SelfReferenceFunctionException(Exception):
    pass


class NoSuchFunctionException(Exception):
    pass


class NoSuchDirectoryInFunctionException(Exception):
    pass


class FunctionCircularReferenceException(Exception):
    pass


class UnknownFunctionException(Exception):
    pass
