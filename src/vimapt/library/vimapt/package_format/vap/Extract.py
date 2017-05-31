#!/usr/bin/env python

import os
import logging
import tarfile

from ..base.Extract import BaseExtract
from vimapt.data_format import loads

logger = logging.getLogger(__name__)

_TARFILE_OPEN_MODE = 'r:gz'


class Extract(BaseExtract):
    def __init__(self, *args, **kwargs):
        super(Extract, self).__init__(*args, **kwargs)

    def extract(self):
        """
        extract input_file to output_dir
        :return: None
        """
        with tarfile.open(self.input_file, _TARFILE_OPEN_MODE) as tar_fd:
            tar_fd.extractall(self.output_dir)


    def get_file_list(self):
        """
        get file list of a package
        :return: List of file name and length pair
        """
        with tarfile.open(self.input_file, _TARFILE_OPEN_MODE) as tar_fd:
            return tar_fd.getnames()
