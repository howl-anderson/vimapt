#!/usr/bin/env python

import os

from .data_format import dumps


class Compress(object):
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
        ball_file_list = self.scan_dir()
        ball_data = []
        ball_content = []
        for f in ball_file_list:
            fd = open(f, 'r')
            file_lines = fd.readlines()
            fd.close()
            relative_file_path = os.path.relpath(f, self.source_dir)
            if self.filter_object:
                if not self.filter_object(relative_file_path, file_lines):
                    continue
            if self.hook_object:
                f, file_lines = self.hook_object(f, file_lines)
            line_number = len(file_lines)
            # if is not empty file
            if line_number:
                last_line = file_lines[-1]
                if not last_line.endswith("\n"):
                    file_lines[-1] += "\n"
                ball_content += file_lines
            ball_data.append([relative_file_path, line_number])

        meta_output = dumps(ball_data)

        if meta_output[-1] != '\n':
            # if meta data is not tailed with \n, append one to it
            meta_output += '\n'

        ball_output = "".join(ball_content)
        output = meta_output + "\n" + ball_output
        fd = open(self.output_file, 'w')
        fd.write(output)
        fd.close()

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
