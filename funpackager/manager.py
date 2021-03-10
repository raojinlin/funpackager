import os
import shutil
import time

from funpackager.logger import get_logger
from funpackager.config import Config
from funpackager.checkers import service_checker
from funpackager.utils import get_indent_spaces


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

    def get_function_distdir(self, function, tag=None):
        suffix = tag
        if not suffix:
            suffix = 'dist'
        return os.path.join(self._config.get_dist(), os.path.basename(function.get_directory()) + "_" + suffix)

    @staticmethod
    def get_function_dirname(function):
        return os.path.basename(function.get_directory())

    def get_dist_least_tag(self, function):
        """
        :param function: Function
        :return:
        """
        dist_dir = self._config.get_dist()
        dirs = []
        for d in sorted(os.listdir(dist_dir)):
            if d.startswith(function.get_name()):
                dirs.append(d)

        if len(dirs) == 0:
            return "least"

        return dirs.pop().split('_').pop()

    def copy_dir(self, src, dst):
        if os.path.isdir(dst):
            self.logger.debug('rm exists path ' + dst)
            shutil.rmtree(dst)

        shutil.copytree(src, dst, symlinks=True)

    def release(self, function_name, tag=None, message='', publisher=None):
        self.has_function_check(function_name)
        service = self._config.get_function(function_name)

        self._mkdir(self._config.get_dist())

        dist_dir = self.get_function_distdir(service, tag)
        service_dist_directory = os.path.join(dist_dir, self.get_function_dirname(service))

        self.logger.debug('copy function directory "%s" => "%s"' % (service.get_directory(), service_dist_directory))
        self.copy_dir(service.get_directory(), service_dist_directory)

        index_src = os.path.join(self._config.get_base_path(), service.get_index_file())
        index_dst = os.path.join(dist_dir, service.get_index_file())

        self.logger.debug('copy function index file "%s" => "%s"' % (index_src, index_dst))
        shutil.copy(index_src, index_dst)

        requirements, modules = self.get_service_requirements(service)
        for requirement in requirements:
            requirement_src = os.path.join(self._config.get_lib(), requirement)
            requirement_dst = os.path.join(dist_dir, requirement)

            self.logger.debug('copy requirement "%s" => "%s"', requirement_src, requirement_dst)
            self.copy_dir(src=requirement_src, dst=requirement_dst)

        for depend_service in service.get_functions():
            service_src = os.path.join(self._config.get_base_path(), depend_service)
            service_dst = os.path.join(dist_dir, depend_service)

            self.logger.debug('copy function "%s" => "%s"' % (depend_service, function_name))
            self.copy_dir(service_src, service_dst)

        for module in modules:
            module_src = os.path.join(self._config.get_base_path(), module)
            module_dst = os.path.join(dist_dir, module)

            self.logger.debug('copy module "%s" => "%s"' % (module, function_name))
            if os.path.isfile(module_src):
                shutil.copy(module_src, module_dst)
            else:
                self.copy_dir(module_src, module_dst)

        self.write_signed_file(dist_dir, tag=tag, message=message, publisher=publisher)

        return dist_dir

    def get_service_requirements(self, service):
        self.logger.debug("get depend function requirements")

        modules = set(service.get_modules())
        requirements = set(service.get_requirements())

        for service_name in service.get_functions():
            depend_service = self._config.get_function(service_name)
            self.logger.debug("get function %s requirements" % service_name)
            for depend_service_requirement in depend_service.get_requirements():
                if depend_service_requirement not in requirements:
                    requirements.add(depend_service_requirement)

                    self.logger.debug("add requirement '%s'" % depend_service_requirement)

            for depend_module in depend_service.get_modules():
                if depend_module not in modules:
                    modules.add(depend_module)
                    self.logger.debug("add requirement module '%s'" % depend_module)

        return requirements, modules

    def write_signed_file(self, path, filename='.release', publisher='funpackager', tag='', message=''):
        self.logger.debug('written signed file, tag: ' + tag)
        with open(os.path.join(path, filename), 'wt') as sign_file:
            sign_file.write("Created by %s at %s.\n" % (publisher, time.strftime('%F %T')))

            if tag != '':
                sign_file.write("Tag: " + tag)

            if message != '':
                sign_file.write("\n\n")
                sign_file.write(message)

    def print_services(self, service_name=None):
        for service in self._config.get_functions():
            if not service_name or service_name == service.get_name():
                requirements, modules = self.get_service_requirements(service)
                print(get_indent_spaces(level=0) + "Function %s:" % service.get_name())
                print(get_indent_spaces() + "Directory: %s" % service.get_directory())
                print(get_indent_spaces() + "Index: %s" % service.get_index())
                print(get_indent_spaces() + "Requirements: [%s]" % ", ".join(requirements))
                print(get_indent_spaces() + "Functions: [%s]" % ", ".join(service.get_functions()))
                print(get_indent_spaces() + "Modules: [%s]" % ", ".join(modules))
                print(get_indent_spaces() + "Tag: %s" % self.get_dist_least_tag(service))
                print("")


