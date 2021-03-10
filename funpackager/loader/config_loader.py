from os import path

from funpackager.loader.factory import get_loader
from funpackager.config import Config
from funpackager.function import Function

from funpackager.checkers import function_directory_checker
from funpackager.checkers import function_depend_checker
from funpackager.checkers import function_index_checker
from funpackager.checkers import function_module_checker
from funpackager.logger import get_logger


class ConfigLoader(object):
    def __init__(self, config_file, debug=False):
        self._loader = get_loader(config_file)
        self.logger = get_logger(self.__class__.__name__, debug)
        self._config_file = config_file
        self._data = None
        self._debug = debug

    def _get_data(self):
        if not self._data:
            self._data = self._loader.get_data()

        return self._data

    def get_real_path(self, p):
        if p.startswith('/'):
            return p

        return path.realpath(path.join(path.dirname(self._config_file), p))

    def get_config(self):
        config = Config(
            self._get_data().get('name'),
            self.get_real_path(self._get_data().get('lib', '')),
            self.get_real_path(self._get_data().get('tests', '')),
            lib_name=self._get_data().get('libName'),
            dist=self.get_real_path(self._get_data().get('dist'))
        )

        self.logger.info('get config from ' + self._config_file)
        for function_dict in self._get_data().get('functions', []):
            directory = self.get_real_path(function_dict.get('directory'))

            function_directory_checker(directory, function_name=function_dict.get('name'))
            function_index_checker(function_dict.get('index'), function_dict.get('name'), path.dirname(directory))
            function_module_checker(function_dict.get('modules', []), function_dict.get('name'), path.dirname(directory))

            service = Function(function_dict.get('name'), directory, function_dict.get('index'))
            service.set_requirements(function_dict.get('requirements', []))
            service.set_functions(function_dict.get('services', []))
            service.set_modules(function_dict.get('modules', []))
            config.add_function(service)

        function_depend_checker(config.get_functions())
        config.set_base_path(path.dirname(config.get_lib()))
        return config
