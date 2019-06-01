import logging
import sys
import os

from logging.handlers import TimedRotatingFileHandler

from config import LOGS_DIR

LOG_FILE_NAME = 'rasp_sec.log'

LOG_FILE_PATH=os.path.join(LOGS_DIR, LOG_FILE_NAME)

timed_file_handler = TimedRotatingFileHandler(LOG_FILE_PATH, when='midnight', interval=1)

timed_file_handler.suffix = '%Y%m%d'

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)-5.5s] %(asctime)s: %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        timed_file_handler,
    ],
)

logger = logging.getLogger()

def LOGI(msg):
    logger.info(msg)

def LOGE(msg):
    logger.error(msg)
