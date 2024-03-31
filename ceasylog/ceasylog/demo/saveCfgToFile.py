"""
保存配置信息到文件
"""

from ceasylog import *

loggerCfg = LoggerConfiger()
loggerCfg.loadFromFile("../demo/config1.json")
loggerCfg.saveToFile("../demo/config2.json")

logger = Logger(loggerCfg)

logger.debug("调试信息")
logger.info("一般信息")
logger.warn("警告信息")
logger.error("错误信息")
logger.critical("严重错误信息")
