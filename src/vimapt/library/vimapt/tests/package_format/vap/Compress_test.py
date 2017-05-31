import unittest
import os
import tempfile

from vimapt.package_format.vap.Compress import Compress


class CompressTest(unittest.TestCase):
    def test_compress(self):
        """
        
        :return: 
        """
        workspace_dir = os.path.join(os.path.abspath(os.path.realpath(__file__)),
                                     'test_data_for_compress')

        input_dir = os.path.join(workspace_dir, 'input')
        output_file = os.path.join(workspace_dir, 'output.vap')

        Compress(source_dir=input_dir, output_file=output_file).compress()
