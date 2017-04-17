#!/usr/bin/env python

import logging

from .RepositoryConfigParser import RepositoryConfigParser
from .TransporterBase import TransporterBase

logger = logging.getLogger(__file__)


class Dispatcher(RepositoryConfigParser):
    transporter_mapping = {}

    def __init__(self, dot_vim_dir):

        self.DOT_VIM_DIR = dot_vim_dir

        self.REPOSITORY_CONFIG_FILE = os.path.join(self.DOT_VIM_DIR, 'vimapt/source')
        self.REPOSITORY_CONFIG = self.load_repository_config(self.DOT_VIM_DIR)
    
    def dispatch(self):
        try:
            handle_class = self.transporter_mapping[self.REPOSITORY_CONFIG]
        except KeyError as e:
            logger.error("Handle for scheme <%s> is missing", self.REPOSITORY_CONFIG)
            raise e
        else:
            handle = handle_class(self, self.DOT_VIM_DIR)
            return handle

    def register_transporter(self, schema, transporter_class):
        if not issubclass(transporter_class, TransporterBase):
            logger.error("%s is not subclass of %s", transporter_class, TransporterBase)
            raise ValueError("%s is not subclass of %s", transporter_class, TransporterBase)

        self.transporter_mapping[schema] = transporter_class
