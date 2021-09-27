import logging
import logging.config

from datetime import datetime
import os

import yaml
from munch import munchify

logger = logging.getLogger(__name__)

DEFAULT_LOG_CONFIG_FILENAME = 'logconfig.yaml'

def from_file(config_file_path):
    try: 
        with open(config_file_path) as fd:
            conf = yaml.load(fd, Loader=yaml.FullLoader)
        return munchify(conf)
    except IOError:
        logger.info("A configuration file named {} is missing" .format(config_file_path))

def construct_logger(file_name=DEFAULT_LOG_CONFIG_FILENAME, name='news_scraper'): 
    '''
        Constructs a logger from a logging config file
        Arguments: 
        file_name -- name of the logging config file, which sits at the root of the app 
        testing -- boolean for logging testing or production configuration
    '''
    app_root = os.environ['ROOT']
    config_path = os.path.join(app_root, file_name)
    logging_config = from_file(config_path)
    current_date = datetime.now().date()
    file_name = logging_config.handlers.file.filename.format(current_date)
    log_file_path = os.path.join(
        app_root, 'bin', 'log', file_name)

    if not os.path.exists(os.path.dirname(log_file_path)):
        os.makedirs(os.path.dirname(log_file_path))
    if not os.path.exists(log_file_path): 
        with open(log_file_path, 'a'):
            os.utime(log_file_path, None)

    logging_config.handlers.file.filename = log_file_path
    logging.basicConfig(level=logging.INFO)
    logging.config.dictConfig(logging_config)
    logging.getLogger(name)

