#!/usr/bin/env python

import os
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


class Extract():
    def __init__(self, input_file, output_dir):
        self.input_file = input_file
        self.output_dir = output_dir
        self.hook_object = False
        self.filter_object = False

        fd = open(self.input_file, 'r')
        file_stream = fd.read()
        fd.close()
        self.meta_stream, self.ball_stream = file_stream.split('\n\n', 1)

    def extract(self):
        meta_data = self.get_file_list()
        ball_lines = self.ball_stream.split('\n')
        start_point = 0
        for file, filelines in meta_data:
            end_point = start_point + filelines
            list_data = ball_lines[start_point: end_point]
            file_stream = "\n".join(list_data)
            if self.filter_object:
                if not self.filter_object(file, file_stream):
                    continue
            if self.hook_object:
                file, file_stream = self.hook_object(file, file_stream)
            ball_dir = os.path.dirname(file)
            ball_absdir = os.path.join(self.output_dir, ball_dir)
            ball_abspath_file = os.path.join(self.output_dir, file)
            if not os.path.isdir(ball_absdir):
                os.makedirs(ball_absdir)
            fd = open(ball_abspath_file, 'w')
            fd.write(file_stream)
            fd.close()
            start_point += filelines

    def get_file_list(self):
        meta_data = load(self.meta_stream, Loader=Loader)
        return meta_data

    def hook(self, hook_object):
        self.hook_object = hook_object

    def filter(self, filter_object):
        self.filter_object = filter_object
