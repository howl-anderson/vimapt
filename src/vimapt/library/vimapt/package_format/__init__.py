import os

from .vap.Extract import Extract as VAPExtract
from .vap.Compress import Compress as VAPCompress


_COMPRESSOR_MAPPING = {
    'vap': VAPCompress
}

_EXTRACTOR_MAPPING = {
    'vap': VAPExtract
}

_FILE_EXT_TO_FORMAT_MAPPING = {
    '.vap': 'vap'
}


def get_compressor(package_format):
    try:
        return _COMPRESSOR_MAPPING[package_format]
    except KeyError:
        msg = "No such package format: {}; all valid package formats are: {}."
        raise ValueError(msg.format(package_format, _COMPRESSOR_MAPPING.keys()))


def get_extractor(package_format):
    try:
        return _EXTRACTOR_MAPPING[package_format]
    except KeyError:
        msg = "No such package format: {}; all valid package formats are: {}."
        raise ValueError(msg.format(package_format, _EXTRACTOR_MAPPING.keys()))


def get_extractor_by_detect_file(package_file):
    package_format = get_package_format_by_detect_file(package_file)
    return get_extractor(package_format)


def get_package_format_by_detect_file(package_file):
    _, ext = os.path.splitext(package_file)
    try:
        return _FILE_EXT_TO_FORMAT_MAPPING[ext]
    except KeyError:
        msg = 'File: {}; {} is not a valid ext. All valid ext is {}'
        raise ValueError(msg.format(package_file, ext, _FILE_EXT_TO_FORMAT_MAPPING.keys()))