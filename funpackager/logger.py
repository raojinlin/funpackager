import logging


def get_logger(name, debug=False):
    log_level = logging.ERROR
    if debug:
        log_level = logging.DEBUG

    logging.basicConfig(format='%(asctime)-15s [%(name)s] %(levelname)s %(message)s', level=log_level)
    return logging.getLogger("fcrelease.%s" % name)
