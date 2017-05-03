import logging
import os

home_dir = os.path.expanduser('~')

log_file = os.path.join(home_dir, '.vim/vimapt/log/vimapt.log')

logging.basicConfig(filename=log_file, level=logging.INFO)
logger = logging.getLogger(__name__)
