from funpackager.loader.abstractLoaderFactory import AbstractLoaderFactory
from funpackager.loader.jsonLoader import JSONLoader


class JSONLoaderFactory(AbstractLoaderFactory):
    def get_loader(self):
        return JSONLoader(self._config_file)
