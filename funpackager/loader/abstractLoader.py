from os import path
from funpackager.loader.notFoundConfigException import NotFoundConfigException


class AbstractLoader(object):
    def __init__(self, config_file=''):
        if config_file != '':
            self.set_config_file(config_file)

        self._config_file = config_file

    def set_config_file(self, config_file):
        if not path.isfile(config_file):
            raise NotFoundConfigException('No such config file "%s"' % config_file)

        self._config_file = config_file

    def get_data(self):
        raise TypeError('Not implemented')
