"""
日志的回调函数
"""

from ceasylog import *


# 回调函数
# ceasylog会传入两个参数： 日志类型：LoggerLevel 日志内容: str
def handler(logType, logMsg):
    # 可以在这里做你的回调操作 比如发到什么信息统计平台 或者微信消息推送啥的操作
    print("回调操作日志", logType, logMsg)


# 创建日志配置器
loggerCfg = LoggerConfiger()
loggerCfg.setName(__name__)
# 传函数 注意函数名称后面不要加括号
loggerCfg.setHandleFunc(handler)

logger = Logger(loggerCfg)

logger.debug("调试信息")
logger.info("一般信息")
logger.warn("警告信息")
logger.error("错误信息")
logger.critical("严重错误信息")
