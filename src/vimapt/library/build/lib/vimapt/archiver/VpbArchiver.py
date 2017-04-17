#!/usr/bin/env python

import os

from yaml import dump
from yaml import load

try:
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Dumper

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from .ArchiverBase import ArchiverBase


class VpbArchiver(ArchiverBase):
    def archive(self, input_dir, output_file):
        input_file_list = self.read_file_list_of_dir(input_dir)

        meta_data = []
        body_data = []

        for input_file in input_file_list:
            file_lines = self.read_file_content(input_file)
            relative_file_path = os.path.relpath(input_file, input_dir)

            line_number = len(file_lines)

            # if is not empty file
            if line_number:
                last_line = file_lines[-1]
                if not last_line.endswith("\n"):
                    file_lines[-1] += "\n"
                body_data += file_lines

            meta_data.append([relative_file_path, line_number])

        self.write_package_structure(meta_data, body_data, output_file)

    def unarchive(self, input_file, output_dir):
        meta_data, body_data = self.load_package_structure(input_file)

        start_line = 0
        for file_name, file_length_by_line in meta_data:
            end_point = start_line + file_length_by_line
            list_data = body_data[start_line: end_point]
            file_stream = "\n".join(list_data)

            self.write_to_dir(file_stream, output_dir, file_name)

            start_line += file_length_by_line

    def load_package_structure(self, input_file):
        fd = open(input_file, 'r')
        file_stream = fd.read()
        fd.close()
        meta_stream, body_stream = file_stream.split('\n\n', 1)  # split the meta and data
        meta = self.parse_meta_data(meta_stream)
        body = self.parse_body_data(body_stream)
        return meta, body

    @staticmethod
    def write_package_structure(meta_data, body_data, output_file):
        meta_output = dump(meta_data, Dumper=Dumper)
        ball_output = "".join(body_data)
        output = meta_output + "\n" + ball_output
        fd = open(output_file, 'w')
        fd.write(output)
        fd.close()

    @staticmethod
    def parse_meta_data(meta_stream):
        return load(meta_stream, Loader=Loader)  # load list from meta, use YAML format

    @staticmethod
    def parse_body_data(body_stream):
        return body_stream.split('\n')

    @staticmethod
    def write_to_dir(file_stream, output_dir, file_name):
        ball_dir = os.path.dirname(file_name)
        ball_absolute_dir = os.path.join(output_dir, ball_dir)
        ball_abspath_file = os.path.join(output_dir, file_name)

        # make sure parent directory exists
        if not os.path.isdir(ball_absolute_dir):
            os.makedirs(ball_absolute_dir)

        fd = open(ball_abspath_file, 'w')
        fd.write(file_stream)
        fd.close()

    @staticmethod
    def read_file_list_of_dir(input_dir):
        file_path_list = []
        yid = os.walk(input_dir)
        for root_dir, path_list, file_list in yid:
            for f in file_list:
                abspath = os.path.join(root_dir, f)
                file_path_list.append(abspath)
        return file_path_list

    @staticmethod
    def read_file_content(file_name):
        fd = open(file_name, 'r')
        file_lines = fd.readlines()
        fd.close()
        return file_lines
