import os
import shutil
import time

from fcrelease.logger import get_logger
from fcrelease.config import Config
from fcrelease.checkers import service_checker
from fcrelease.utils import get_indent_spaces


class Manager(object):
    def __init__(self, config: Config, debug=False):
        self._config = config
        self.logger = get_logger(self.__class__.__name__, debug)

    def has_function_check(self, service):
        service_checker(self._config.has_function(service), service)

    def _mkdir(self, path):
        if os.path.isdir(path):
            return
        os.mkdir(path)

    def get_function_dist(self, function):
        return os.path.join(self._config.get_dist(), os.path.basename(function.get_directory()) + "_dist")

    def get_function_dirname(self, function):
        return os.path.basename(function.get_directory())

    def copy_dir(self, src, dst):
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        else:
            shutil.copytree(src, dst)

    def release(self, function_name):
        self.has_function_check(function_name)
        service = self._config.get_function(function_name)

        self._mkdir(self._config.get_dist())

        dist_dir = self.get_function_dist(service)
        service_dist_directory = os.path.join(dist_dir, self.get_function_dirname(service))

        self.logger.debug('copy function directory "%s" => "%s"' % (service.get_directory(), service_dist_directory))
        self.copy_dir(service.get_directory(), service_dist_directory)

        index_src = os.path.join(self._config.get_base_path(), service.get_index_file())
        index_dst = os.path.join(dist_dir, service.get_index_file())

        self.logger.debug('copy function index file "%s" => "%s"' % (index_src, index_dst))
        shutil.copy(index_src, index_dst)

        for requirement in self.get_service_requirements(service):
            requirement_src = os.path.join(self._config.get_lib(), requirement)
            requirement_dst = os.path.join(dist_dir, requirement)

            self.logger.debug('copy requirement "%s" => "%s"', requirement_src, requirement_dst)
            self.copy_dir(src=requirement_src, dst=requirement_dst)

        for depend_service in service.get_functions():
            service_src = os.path.join(self._config.get_base_path(), depend_service)
            service_dst = os.path.join(dist_dir, depend_service)

            self.logger.debug('copy function "%s" => "%s"' % (depend_service, function_name))
            self.copy_dir(service_src, service_dst)

        for module in service.get_modules():
            module_src = os.path.join(self._config.get_base_path(), module)
            module_dst = os.path.join(dist_dir, module)

            self.logger.debug('copy module "%s" => "%s"' % (module, function_name))
            if os.path.isfile(module_src):
                shutil.copy(module_src, module_dst)
            else:
                self.copy_dir(module_src, module_dst)

        self.write_sign_file(dist_dir)

    def get_service_requirements(self, service):
        self.logger.debug("get depend function requirements")

        requirements = []
        for requirement in service.get_requirements():
            requirements.append(requirement)

        for service_name in service.get_functions():
            depend_service = self._config.get_function(service_name)
            self.logger.debug("get function %s requirements" % service_name)
            for depend_service_requirement in depend_service.get_requirements():
                if depend_service_requirement not in requirements:
                    requirements.append(depend_service_requirement)

                    self.logger.debug("add requirement '%s'" % depend_service_requirement)

        return requirements

    def write_sign_file(self, path, message=''):
        with open(os.path.join(path, '.fcrelease'), 'wt') as sign_file:
            sign_file.write("Created by fcrelease at %s.\n" % time.strftime('%F %T'))

            if message != '':
                sign_file.write(message)

    def print_services(self, service_name=None):
        for service in self._config.get_functions():
            if not service_name or service_name == service.get_name():
                print(get_indent_spaces(level=0) + "Function %s:" % service.get_name())
                print(get_indent_spaces() + "Directory: %s" % service.get_directory())
                print(get_indent_spaces() + "Index: %s" % service.get_index())
                print(get_indent_spaces() + "Requirements: [%s]" % ", ".join(service.get_requirements()))
                print(get_indent_spaces() + "Functions: [%s]" % ", ".join(service.get_functions()))
                print(get_indent_spaces() + "Modules: [%s]" % ", ".join(service.get_modules()))
                print("")


