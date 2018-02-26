#!/usr/bin/env python
# -*- encoding: utf8 -*-
import logging
import logging.handlers
from conf import settings

'''
handle all the logging works
'''

# 'application' code
'''
logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')
 '''


def logger(log_type):

    # create logger
    _logger = logging.getLogger(log_type)
    _logger.setLevel(settings.LOG_LEVEL)

    # create console handler and set level to debug
    # ch = logging.StreamHandler()
    # ch.setLevel(settings.LOG_LEVEL)

    # create file handler and set level to warning
    log_file = "%s/logs/%s" % (settings.BASE_DIR, settings.LOG_TYPES[log_type])
    fh = logging.handlers.WatchedFileHandler(log_file, encoding='utf-8')

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch and fh
    # ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # add ch and fh to logger
    # _logger.addHandler(ch)
    _logger.addHandler(fh)

    return _logger
