from fcrelease.loader.abstractLoaderFactory import AbstractLoaderFactory
from fcrelease.loader.abstractLoader import AbstractLoader
from fcrelease.loader.yamlLoader import YamlLoader


class YamlLoaderFactory(AbstractLoaderFactory):
    def get_loader(self) -> AbstractLoader:
        return YamlLoader(self._config_file)

