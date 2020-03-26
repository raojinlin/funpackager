import yaml

from fcrelease.loader.abstractLoader import AbstractLoader


class YamlLoader(AbstractLoader):
    def __init__(self, config_file=''):
        AbstractLoader.__init__(self, config_file)
        self._data = None

    def get_data(self):
        if not self._data:
            loader = yaml.loader.Loader(open(self._config_file, 'rt'))
            self._data = loader.get_data()

        return self._data

