#!/usr/bin/env python

import os

from vimapt.data_format import dumps


class BaseCompress(object):
    def __init__(self, source_dir, output_file):
        self.source_dir = source_dir
        self.output_file = output_file
        self.hook_object = None
        self.filter_object = None

    def compress(self):
        """
        Compress directory to file
        :return: None
        """
        raise NotImplementedError

    def scan_dir(self):
        """
        Fetch absolute path of file list of directory
        :return: List of file absolute location
        """
        file_path_list = []
        yid = os.walk(self.source_dir)
        for root_dir, path_list, file_list in yid:
            for f in file_list:
                abspath = os.path.join(root_dir, f)
                file_path_list.append(abspath)
        return file_path_list

    def hook(self, hook_object):
        self.hook_object = hook_object

    def filter(self, filter_object):
        self.filter_object = filter_object
