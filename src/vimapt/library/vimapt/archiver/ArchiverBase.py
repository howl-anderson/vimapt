class ArchiverBase(object):
    def __init__(self, scheme):
        self.scheme = scheme

    def archive(self, input_dir, output_file):
        return NotImplementedError

    def unarchive(self, input_file, output_dir):
        return NotImplementedError
