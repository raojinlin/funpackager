from fcrelease.loader.abstractLoader import AbstractLoader


class AbstractLoaderFactory(object):
    def __init__(self, config_file):
        self._config_file = config_file

    def get_loader(self) -> AbstractLoader:
        return AbstractLoader()
