import logging

from .CompressorBase import CompressorBase

logger = logging.getLogger(__file__)


class Dispatcher(object):
    compressor_mapping = {}

    def dispatch(self, scheme):
        try:
            handle_class = self.compressor_mapping[scheme]
        except KeyError as e:
            logger.error("Handle for scheme <%s> is missing", scheme)
            raise e
        else:
            handle = handle_class(self, scheme)
            return handle

    def register_compressor(self, schema, compressor_class):
        if not issubclass(compressor_class, CompressorBase):
            logger.error("%s is not subclass of %s", compressor_class, CompressorBase)
            raise ValueError("%s is not subclass of %s", compressor_class, CompressorBase)

        self.compressor_mapping[schema] = compressor_class
