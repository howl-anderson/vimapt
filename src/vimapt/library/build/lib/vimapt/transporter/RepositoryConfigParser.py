#!/usr/bin/env python

import logging
import os
import urlparse

logger = logging.getLogger(__file__)


class RepositoryConfigParser(object):
    @staticmethod
    def load_repository_config(dot_vim_dir):
        repository_config_file = os.path.join(dot_vim_dir, 'vimapt/source')

        with open(repository_config_file, 'r') as fd:
            config = fd.read()
            config = config.strip()
            return urlparse.urlparse(config)
