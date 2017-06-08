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
            package_member_list = tar_fd.getmembers()

            allowed_package_number_list = []

            # apply filter hook
            if self.hook_object is not None:
                for member in package_member_list:
                    if self.hook_object(member.name, None):
                        allowed_package_number_list.append(member)
            else:
                allowed_package_number_list = package_member_list

            tar_fd.extractall(self.output_dir, members=allowed_package_number_list)


    def get_file_list(self):
        """
        get file list of a package
        :return: List of file name and length pair
        """
        with tarfile.open(self.input_file, _TARFILE_OPEN_MODE) as tar_fd:
            return tar_fd.getnames()
