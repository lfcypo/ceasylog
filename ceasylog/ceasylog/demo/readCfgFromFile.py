"""
从配置文件加载配置信息
"""

from ceasylog import *

loggerCfg = LoggerConfiger()
loggerCfg.loadFromFile("../demo/config1.json")

logger = Logger(loggerCfg)

logger.debug("调试信息")
logger.info("一般信息")
logger.warn("警告信息")
logger.error("错误信息")
logger.critical("严重错误信息")
