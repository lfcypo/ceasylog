"""
静态简单的日志记录
Static模式

直接使用默认配置 （名称为空）
不需要单独配置并实例化日志记录器
在一些脚本中非常简单实用
"""

from ceasylog import logger


logger.debug("调试信息")
logger.info("一般信息")
logger.warn("警告信息")
logger.error("错误信息")
logger.critical("严重错误信息")
