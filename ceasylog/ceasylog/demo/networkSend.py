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

