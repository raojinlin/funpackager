from funpackager.loader.abstractLoaderFactory import AbstractLoaderFactory
from funpackager.loader.abstractLoader import AbstractLoader
from funpackager.loader.yamlLoader import YamlLoader


class YamlLoaderFactory(AbstractLoaderFactory):
    def get_loader(self) -> AbstractLoader:
        return YamlLoader(self._config_file)

