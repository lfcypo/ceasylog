# CEasyLog

一个简单的日志记录工具

更新时间 2024-04-05 

## 介绍

您可以使用CEasyLog来优雅的记录和打印程序运行过程中的日志信息

### 日志的等级

ceasylog把常用的日志情况分成了五大等级

* DEBUG 调试日志
* INFO 一般日志
* WARN 警告日志
* ERROR 错误日志
* CRITICAL 严重错误日志

## 安装

```
pip install ceasylog
```

## 使用方法

### 引入相关的库

```python
from ceasylog import *
```

### 配置CEasyLog

*一般来说仅需配置需要特别设置的项目 约定大于配置*

```python
LoggerCfg = LoggerConfiger()

# 设置名称 缺省default
LoggerCfg.setName("test")

# 设置打印的最小日志等级 缺省INFO
LoggerCfg.setMinPrintLevel(LoggerLevel.WARN)

# 设置打印的最大日志等级 缺省CRITICAL
LoggerCfg.setMaxPrintLevel(LoggerLevel.ERROR)

# 设置存储的最小日志等级 缺省WARN
LoggerCfg.setMinRecordLevel(LoggerLevel.ERROR)

# 设置存储的最大日志等级 缺省CRITICAL
LoggerCfg.setMaxRecordLevel(LoggerLevel.ERROR)

# 设置打印的时间格式 缺省%Y-%m-%d %H:%M:%S.%f
LoggerCfg.setPrintTimeFormat("%Y-%m-%d %H:%M:%S.%f")

# 设置记录的时间格式 缺省%Y-%m-%d %H:%M:%S.%f
LoggerCfg.setRecordTimeFormat("%Y-%m-%d %H:%M:%S.%f")

# 设置记录的文件名 缺省%Y-%m-%d
LoggerCfg.setRecordPathNameFormat("%Y-%m-%d")

# 设置日志记录功能 如果不调用这个函数就不记录到文件 调用的话就传入记录的目标文件地址（推荐绝对路径）
# 记录的文件会根据setRecordPathNameFormat进行格式化 
LoggerCfg.isRecord("/home/user/logs/")
# 例如上面的Demo会生成 /home/user/logs/2024-03-01.log 文件
```

### 根据配置类创建日志记录器

```python
logger = Logger(LoggerCfg)
```

### 开始使用吧

```python
logger.debug("这是一条调试日式")
logger.info("这是一条信息日志")
logger.warn("这是一条警告日志")
logger.error("这是一条错误日志")
logger.critical("这是一条严重错误日志")
```

### 整体流程

```python
from ceasylog import *

LoggerCfg = LoggerConfiger()

LoggerCfg.setName("test")
LoggerCfg.setMinPrintLevel(LoggerLevel.WARN)
LoggerCfg.setMaxPrintLevel(LoggerLevel.ERROR)
LoggerCfg.setMinRecordLevel(LoggerLevel.ERROR)
LoggerCfg.setMaxRecordLevel(LoggerLevel.ERROR)
LoggerCfg.setRecordPathNameFormat("%Y-%m-%d")
LoggerCfg.isRecord("/home/user/logs/")

logger = Logger(LoggerCfg)

logger.debug("这是一条调试日式")
logger.info("这是一条信息日志")
logger.warn("这是一条警告日志")
logger.error("这是一条错误日志")
logger.critical("这是一条严重错误日志")
```

## 更多功能

**注：所有的相关demo都在项目/demo文件夹中**

### 打印异常

您可以用try-except配合ceasylog处理异常

```python
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
        
        # 这里的LoggerLevel.ERROR指的是打印出来的异常为什么日志等级
        # 也可以不传 缺省ERROR

```

### 配置继承

不同的日志记录器之间的配置可以进行继承

```python
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
loggerFather.info("俺是他爹")
loggerChild.info("俺是他崽")

# 另外继承是可以不断继续的 (子可以有孙 孙可以有曾孙.....子子孙孙无穷匮也)

```

### 配置文件

配置文件可以更加方便的设置日志记录

#### 从配置文件加载

```python
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

```

其中配置文件路径可以为绝对路径 或者是相对于主脚本运行目录的相对路径

#### 写入配置文件

一个设置好的配置也可以写入配置文件方便调用

```python
"""
保存配置信息到文件
"""

from ceasylog import *

loggerCfg = LoggerConfiger()
# 一些设置......
loggerCfg.saveToFile("../demo/config2.json")

logger = Logger(loggerCfg)

logger.debug("调试信息")
logger.info("一般信息")
logger.warn("警告信息")
logger.error("错误信息")
logger.critical("严重错误信息")

```

其中配置文件路径可以为绝对路径 或者是相对于主脚本运行目录的相对路径

### 推送信息至网络服务器

ceasylog支持把日志信息推送到您自建的日志服务器上

```python
"""
向网络服务器发送日志信息

注意：ceasylog仅提供一个接口请求门面 具体的服务端请您手动实现
请求的方式使用POST 发送的数据为json
服务端接收到的内容：
{
        "uid": 日志uid, string
        "msg": 日志内容, string
        "level": 日志等级 INFO | DEBUG | WARN | ERROR | CRITICAL, enum(string)
        "time": 记录时间，string(timestamp)
}
请求头默认带Content-Type: application/json, 您可以结合自身业务需要自定义 也可及结合服务端实现鉴权需求
"""

from ceasylog import *

loggerCfg = LoggerConfiger()
loggerCfg.setName(__name__)

# 创建网络配置器
loggerNetworkCfg = LoggerNetworkConfiger()
# 指定目标服务器
loggerNetworkCfg.setEndpoint("http://127.0.0.1:8080/log")
# 可以使用setHeader设置请求头 默认带Content-Type: application/json
# loggerNetworkCfg.setHeader()

# 设置使用网络日志服务器
loggerCfg.setNetwork(loggerNetworkCfg)

logger = Logger(loggerCfg)

logger.debug("调试信息")
logger.info("一般信息")
logger.warn("警告信息")
logger.error("错误信息")
logger.critical("严重错误信息")


# 服务端可参考下面 flask实现

# from flask import Flask, request
# from flask_cors import CORS
#
# app = Flask(__name__)
# CORS(app)
#
# @app.route("/log", methods=['POST'])
# def log():
#     # print(request.headers)
#     print(request.json)
#     return "ok."
#
# if __name__ == '__main__':
#     app.run(port=8080)
```

## 作者

糖星科技@黄旭东

CandyStar@HuangXudong
