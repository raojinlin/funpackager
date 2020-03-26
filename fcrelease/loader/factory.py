import os

from fcrelease.loader.abstractLoader import AbstractLoader
from fcrelease.loader.abstractLoaderFactory import AbstractLoaderFactory
from fcrelease.loader.yamlLoaderFactory import YamlLoaderFactory
from fcrelease.loader.jsonLoaderFactory import JSONLoaderFactory


def get_loader(config_file) -> AbstractLoader:
    file_type = os.path.basename(config_file).split('.')[1]
    if file_type == 'yaml':
        return YamlLoaderFactory(config_file).get_loader()
    elif file_type == 'json':
        return JSONLoaderFactory(config_file).get_loader()
    else:
        return AbstractLoaderFactory(config_file).get_loader()
