import logging
import logging.config

def get_logger(logname = '', confname = 'cfg/log.conf'):
    logging.config.fileConfig(confname)
    
    if (logname):
        return logging.getLogger(logname)
    else:
        return logging.getLogger()
