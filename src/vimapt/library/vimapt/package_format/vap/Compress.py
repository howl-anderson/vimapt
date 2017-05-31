#!/usr/bin/env python

import os
import tarfile

from ..base.Compress import BaseCompress
from vimapt.data_format import dumps

_TARFILE_OPEN_MODE = 'w:gz'


class Compress(BaseCompress):
    def __init__(self, *args, **kwargs):
        super(Compress, self).__init__(*args, **kwargs)

    def compress(self):
        """
        Compress directory to file
        :return: None
        """
        file_list = self.scan_dir()
        rel_file_list = [os.path.relpath(i, self.source_dir) for i in file_list]
        with tarfile.open(self.output_file, _TARFILE_OPEN_MODE) as tar_fd:
            for i, file_name in enumerate(file_list):
                tar_fd.add(file_name, rel_file_list[i])
