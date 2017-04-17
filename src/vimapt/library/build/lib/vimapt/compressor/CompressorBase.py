class CompressorBase(object):
    def __init__(self, scheme):
        self.scheme = scheme

    def compress(self, input_file, output_file):
        return NotImplementedError

    def decompress(self, input_file, output_file):
        return NotImplementedError
