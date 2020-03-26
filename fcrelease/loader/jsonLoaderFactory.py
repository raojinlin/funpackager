from fcrelease.loader.abstractLoaderFactory import AbstractLoaderFactory
from fcrelease.loader.jsonLoader import JSONLoader


class JSONLoaderFactory(AbstractLoaderFactory):
    def get_loader(self):
        return JSONLoader(self._config_file)
