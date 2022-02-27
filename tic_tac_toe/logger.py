import logging
import inspect


def init(level=logging.DEBUG, filename="tic_tac_toe_logs.ini", log_format=""):
    log_format = log_format or "%(asctime)s - %(message)s"

    logging.basicConfig(level=level, filename=filename, format=log_format)


def get_outer_logger():
    return logging.getLogger(
        inspect.currentframe().f_back.f_back.f_globals["__name__"]
    )


def info(msg, *args, **kwargs):
    return get_outer_logger().info(msg, *args, **kwargs)
