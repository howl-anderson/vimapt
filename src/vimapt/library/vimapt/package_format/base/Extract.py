#!/usr/bin/env python

import os
import logging

from vimapt.data_format import loads

logger = logging.getLogger(__name__)


class BaseExtract(object):
    def __init__(self, input_file, output_dir):
        self.input_file = input_file
        self.output_dir = output_dir
        self.hook_object = None
        self.filter_object = None

    def extract(self):
        """
        extract input_file to output_dir
        :return: None
        """
        raise NotImplementedError

    def get_file_list(self):
        """
        get file list of a package
        :return: List of file name and length pair
        """
        raise NotImplementedError

    def hook(self, hook_object):
        """
        Bind hook object. 
        :param hook_object: an executable object take to args (file name and content) and return boolean.
                            Return False means the file is not extract to system, used to protect overwrite.
        :return: None
        """
        self.hook_object = hook_object

    def filter(self, filter_object):
        """
        Bind filter object
        :param filter_object: an executable object take to args (file name and content)
                              and return tuple of file name and content.
                              This object can change the file name and file content.
        :return: None
        """
        self.filter_object = filter_object
