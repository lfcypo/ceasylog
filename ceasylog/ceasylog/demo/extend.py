"""
配置继承的使用
"""

from ceasylog import *

# 父配置
loggerCfgFather = LoggerConfiger()
loggerCfgFather.setName("father")
loggerCfgFather.setPrintTimeFormat("%Y-%m-%d %H:%M:%S")

# 要被继承过去的子配置
loggerCfgChild = LoggerConfiger()
loggerCfgChild.extendBy(loggerCfgFather)
# 这样父配置都被继承过来了
# 修改一下继承的内容
loggerCfgChild.setName("child")

loggerFather = Logger(loggerCfgFather)
loggerChild = Logger(loggerCfgChild)

# 这父子两除了名字外其他都一样
loggerFather.info("俺是他爹er")
loggerChild.info("俺是他崽er")

# 另外继承是可以不断连续的 (子可以有孙 孙可以有曾孙.....子子孙孙无穷匮也)
