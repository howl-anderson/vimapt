import zlib


class GzCompressor(object):
    def __init__(self, scheme):
        self.scheme = scheme

    def compress(self, input_file, output_file):
        data_stream = self.load_file_content(input_file)
        compressed_data_stream = zlib.compress(data_stream)
        self.write_file_content(compressed_data_stream, output_file)

    def decompress(self, input_file, output_file):
        compressed_data_stream = self.load_file_content(input_file)
        data_stream = zlib.decompress(compressed_data_stream)
        self.write_file_content(data_stream, output_file)

    @staticmethod
    def load_file_content(input_file):
        with open(input_file, 'rb') as fd:
            return fd.read()

    @staticmethod
    def write_file_content(data_stream, output_file):
        with open(output_file, 'wb') as fd:
            fd.write(data_stream)
