"""
打印异常
"""
from ceasylog import *

# 创建日志配置器
loggerCfg = LoggerConfiger()

logger = Logger(loggerCfg)


def hahaha():
    # 手动触发个异常
    return 1 / 0


if __name__ == '__main__':
    try:
        # 捕捉异常
        hahaha()
    except Exception as e:
        # 打印异常
        logger.exception(e, LoggerLevel.ERROR)
