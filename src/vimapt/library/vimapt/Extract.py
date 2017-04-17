#!/usr/bin/env python

import os

from .data_format.yaml import load


class Extract(object):
    def __init__(self, input_file, output_dir):
        self.input_file = input_file
        self.output_dir = output_dir
        self.hook_object = None
        self.filter_object = None

        fd = open(self.input_file, 'r')
        file_stream = fd.read()
        fd.close()
        self.meta_stream, self.ball_stream = file_stream.split('\n\n', 1)  # split the meta and data

    def extract(self):
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
            start_point += file_length

    def get_file_list(self):
        meta_data = load(self.meta_stream)  # load list from meta, use YAML format
        return meta_data

    def hook(self, hook_object):
        self.hook_object = hook_object

    def filter(self, filter_object):
        self.filter_object = filter_object

if __name__ == "__main__":
    o = Extract("vimapt_1.0-1.vpb", "./output")
    o.extract()
