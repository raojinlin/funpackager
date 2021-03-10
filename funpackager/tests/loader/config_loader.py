import unittest
import os

from fcrelease.loader.config_loader import ConfigLoader

base_path = os.path.dirname(__file__)


class TestConfigLoader(unittest.TestCase):

    def test_get_config(self):
        """Config loader get config test"""
        config_loader = ConfigLoader('../config.yaml')

        config = config_loader.get_config()
        self.assertEqual(config.get_name(), 'print services')
        self.assertEqual(len(config.get_functions()), 3)


if __name__ == '__main__':
    unittest.main()
