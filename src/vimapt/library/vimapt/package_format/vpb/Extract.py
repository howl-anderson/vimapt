#!/usr/bin/env python

import os
import logging

from vimapt.data_format import loads
from vimapt.package_format.base.Extract import BaseExtract

logger = logging.getLogger(__name__)


class Extract(BaseExtract):
    def __init__(self, *args, **kwargs):
        super(Extract, self).__init__(*args, **kwargs)

        self._extract_meta_info()

    def _extract_meta_info(self):
        fd = open(self.input_file, 'r')
        file_stream = fd.read()
        fd.close()
        self.meta_stream, self.ball_stream = file_stream.split('\n\n', 1)  # split the meta and data

    def extract(self):
        """
        extract input_file to output_dir
        :return: None
        """
        meta_data = self.get_file_list()
        ball_lines = self.ball_stream.split('\n')
        start_point = 0
        for file_name, file_length in meta_data:
            end_point = start_point + file_length
            list_data = ball_lines[start_point: end_point]
            file_stream = "\n".join(list_data)
            if self.filter_object:  # unfinished part
                # hook to filter_object
                if not self.filter_object(file_name, file_stream):
                    # this file will be ignored
                    start_point += file_length

                    logger.info("package <%s>: <%s> was passed.", self.input_file, file_name)

                    continue
            if self.hook_object:  # unfinished part
                # hook to hook_object
                file_name, file_stream = self.hook_object(file_name, file_stream)
            ball_dir = os.path.dirname(file_name)
            ball_absolute_dir = os.path.join(self.output_dir, ball_dir)
            ball_abspath_file = os.path.join(self.output_dir, file_name)
            if not os.path.isdir(ball_absolute_dir):
                os.makedirs(ball_absolute_dir)
            fd = open(ball_abspath_file, 'w')
            fd.write(file_stream)
            fd.close()

            logger.info("package <%s>: <%s> was write.", self.input_file, ball_abspath_file)

            start_point += file_length

    def get_file_list(self):
        """
        get file list of a package
        :return: List of file name and length pair
        """
        meta_data = loads(self.meta_stream)  # load list from meta, use YAML format
        return [i[0] for i in meta_data]
