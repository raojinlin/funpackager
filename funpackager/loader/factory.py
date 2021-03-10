import os

from funpackager.loader.abstractLoader import AbstractLoader
from funpackager.loader.abstractLoaderFactory import AbstractLoaderFactory
from funpackager.loader.yamlLoaderFactory import YamlLoaderFactory
from funpackager.loader.jsonLoaderFactory import JSONLoaderFactory


def _get_file_type(config_file):
    config_name = os.path.basename(config_file)
    if '.' in config_name:
        return config_name.split('.')[1]
    else:
        return ''


def get_loader(config_file) -> AbstractLoader:
    file_type = _get_file_type(config_file)

    if file_type == 'yaml':
        return YamlLoaderFactory(config_file).get_loader()
    elif file_type == 'json':
        return JSONLoaderFactory(config_file).get_loader()
    else:
        return AbstractLoaderFactory(config_file).get_loader()
