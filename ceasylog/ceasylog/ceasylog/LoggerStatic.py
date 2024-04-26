from ceasylog.Logger import Logger
from ceasylog.LoggerConfiger import LoggerConfiger

loggerCfg = LoggerConfiger()
loggerCfg.setName("")

logger = Logger(loggerCfg)


def debug(msg: str):
    logger.debug(msg)


def info(msg: str):
    logger.info(msg)


def warn(msg: str):
    logger.warn(msg)


def error(msg: str):
    logger.error(msg)


def critical(msg: str):
    logger.critical(msg)


def exception(e: BaseException):
    logger.exception(e)
