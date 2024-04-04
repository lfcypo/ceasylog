"""
记录日志到文件
"""

from ceasylog import *

# 创建日志配置器
loggerCfg = LoggerConfiger()
loggerCfg.setName(__name__)
# 日志记录文件名称格式 后缀是log
loggerCfg.setRecordPathNameFormat("%Y-%m-%d")
# 日志记录位置
loggerCfg.isRecord("../demo/log/")

logger = Logger(loggerCfg)

logger.debug("调试信息")
logger.info("一般信息")
logger.warn("警告信息")
logger.error("错误信息")
logger.critical("严重错误信息")
