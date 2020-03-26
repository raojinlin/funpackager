import json

from fcrelease.loader.abstractLoader import AbstractLoader


class JSONLoader(AbstractLoader):
    def __init__(self, conf_file):
        AbstractLoader.__init__(self, conf_file)

        self._data = None

    def get_data(self):
        if not self._data:
            self._data = json.load(open(self._config_file, 'rt'))

        return self._data
      

