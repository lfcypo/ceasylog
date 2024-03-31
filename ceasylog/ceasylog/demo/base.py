"""
基本的日志打印方式
"""

from ceasylog import *

# 创建日志配置器
loggerCfg = LoggerConfiger()
loggerCfg.setName(__name__)
# 可选配置项目（具体请参考README）
# loggerCfg.setMinPrintLevel(LoggerLevel.DEBUG)
# loggerCfg.setMaxPrintLevel(LoggerLevel.ERROR)
# loggerCfg.setMinRecordLevel(LoggerLevel.ERROR)
# loggerCfg.setMaxRecordLevel(LoggerLevel.ERROR)
# loggerCfg.setRecordPathNameFormat("%Y-%m-%d")
# LoggerCfg.isRecord("/home/user/logs/")

logger = Logger(loggerCfg)

logger.debug("调试信息")
logger.info("一般信息")
logger.warn("警告信息")
logger.error("错误信息")
logger.critical("严重错误信息")
