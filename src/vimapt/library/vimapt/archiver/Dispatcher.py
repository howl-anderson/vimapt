import logging

from .ArchiverBase import ArchiverBase

logger = logging.getLogger(__file__)


class Dispatcher(object):
    archiver_mapping = {}

    def dispatch(self, scheme):
        try:
            handle_class = self.archiver_mapping[scheme]
        except KeyError as e:
            logger.error("Handle for scheme <%s> is missing", scheme)
            raise e
        else:
            handle = handle_class(self, scheme)
            return handle

    def register_archiver(self, schema, archiver_class):
        if not issubclass(archiver_class, ArchiverBase):
            logger.error("%s is not subclass of %s", archiver_class, ArchiverBase)
            raise ValueError("%s is not subclass of %s", archiver_class, ArchiverBase)

        self.archiver_mapping[schema] = archiver_class
