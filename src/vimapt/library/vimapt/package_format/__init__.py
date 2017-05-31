from .vap.Extract import Extract as VAPExtract
from .vap.Compress import Compress as VAPCompress


_COMPRESSOR_MAPPING = {
    'vap': VAPExtract
}

_EXTRACTOR_MAPPING = {
    'vap': VAPCompress
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