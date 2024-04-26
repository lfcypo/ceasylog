import os
import platform
import random
import string
import threading
import time
import traceback
import uuid
from datetime import datetime

import requests
from colorama import Style
from colorama import init as coloramaInit

from ceasylog.LoggerConfiger import *

coloramaInit(autoreset=True)

# Surprise Mother F**K LMX

LOG_STYLE = [
    Fore.LIGHTYELLOW_EX,
    Fore.LIGHTBLUE_EX,
    Fore.LIGHTCYAN_EX,
    Fore.LIGHTGREEN_EX,
    Fore.LIGHTMAGENTA_EX,
]

MAX_BLANK = 35


def getStyle(name: str):
    """获取样式"""
    styleMap = {
        LOG_STYLE[0]: ["a", "b", "c", "d", "u", "0", "8", "9"],
        LOG_STYLE[1]: ["e", "f", "g", "h", "v", "1", "7"],
        LOG_STYLE[2]: ["i", "j", "k", "l", "w", "2", "6"],
        LOG_STYLE[3]: ["m", "n", "o", "p", "x", "3", "5"],
        LOG_STYLE[4]: ["q", "r", "s", "t", "y", "z", "4"],
    }
    startWith = name[:1].lower()
    for i in styleMap.keys():
        if startWith in styleMap[i]:
            return i
    return LOG_STYLE[random.randint(0, len(LOG_STYLE) - 1)]


def getTime(timeFormat1: str, timeFormat2: str) -> tuple[str, str, str]:
    """
    获取时间
    :param timeFormat2:
    :param timeFormat1:
    :return:
    """
    now = datetime.now()
    return now.strftime(timeFormat1), now.strftime(timeFormat2), str(time.time())


def getSysFileSplit():
    """
    获取操作系统的文件分隔符
    :return:
    """
    if platform.system() == "Windows":
        return "\\"
    else:
        return "/"


def getUID():
    """
    生成唯一标识符
    :return:
    """
    randomString = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    uniqueId = str(uuid.uuid4())[:6] + randomString
    return uniqueId


def logPrint(msg: str, level: LoggerLevel, config: LoggerConfiger, uid: str, logStyle, nowTime: str):
    """
    打印日志
    :param nowTime: 时间
    :param msg: 信息
    :param level: 等级
    :param config: 配置
    :param uid: 唯一标识符
    :param logStyle: logger名称样式
    :return:
    """
    if level.level < config.minPrintLevel.level or level.level > config.maxPrintLevel.level:
        return
    blank = " " * (MAX_BLANK - len(config.name))
    logContent = (f"{Fore.GREEN}{nowTime} {Fore.MAGENTA}{uid} {logStyle}{config.name}{Style.RESET_ALL}{blank} "
                  f"{level.backStyle} {level.msg} {Style.RESET_ALL} {level.frontStyle} {msg}")
    print(logContent)


def logRecord(msg: str, level: LoggerLevel, config: LoggerConfiger, uid: str, nowTime: str):
    """
    记录日志到文件
    :param nowTime: 时间
    :param msg: 信息
    :param level: 等级
    :param config: 配置
    :param uid: 唯一标识符
    :return:
    """
    if level.level < config.minRecordLevel.level or level.level > config.maxRecordLevel.level or not config.isRecordB:
        return
    blank = " " * (MAX_BLANK - len(config.name))
    logContent = f"{nowTime} {uid} {config.name}{blank} {level.msg} {msg}"
    try:
        if not config.recordPath.endswith(getSysFileSplit()):
            recordPath = config.recordPath + getSysFileSplit()
        else:
            recordPath = config.recordPath
        recordFullFileName = recordPath + getTime(config.recordPathNameFormat, "")[0] + ".log"
        if not os.path.isabs(recordFullFileName):
            # 拼接解释器运行路径作为绝对路径
            recordFullFileName = os.path.join(os.path.dirname(os.path.abspath(__file__)), recordFullFileName)
        if not os.path.exists(os.path.dirname(recordFullFileName)):
            os.makedirs(os.path.dirname(recordFullFileName))
        with open(recordFullFileName, "a", encoding="utf-8") as logRecordFileObject:
            logRecordFileObject.write(logContent + "\n")
    except Exception as e:
        easyLogBuildInLogger.error("Failed to write log file " + str(e))


def logNetworkSender(msg: str, level: LoggerLevel, config: LoggerConfiger, uid: str, nowTime: str):
    if not config.isRecordNetworkB:
        return
    payload = {
        "uid": uid,
        "msg": msg,
        "level": level.des,
        "time": nowTime
    }

    def sendRequests(endpoint: str, data: dict, headers: dict):
        try:
            response = requests.post(endpoint, json=data, headers=headers, timeout=10)
            if response.status_code != 200:
                easyLogBuildInLogger.error("Failed to send log to " + endpoint + " " + str(response.status_code))
                return
            response.close()
        except Exception as e:
            easyLogBuildInLogger.error("Failed to send log to " + endpoint + " " + str(e))
            return

    threading.Thread(target=sendRequests,
                     args=(config.networkRecordCfg.endpoint, payload, config.networkRecordCfg.header)).start()


class Logger(object):
    """
    日志记录器
    """

    def __init__(self, config: LoggerConfiger):
        """
        :param config: 配置信息
        """
        self.config = config
        # 超过长度的名称省略
        if len(self.config.name) > MAX_BLANK:
            self.config.setName(self.config.name[:(MAX_BLANK - 13)] + "..." + self.config.name[-10:])
        # self.logStyle = LOG_STYLE[random.randint(0, len(LOG_STYLE) - 1)]
        self.logStyle = getStyle(self.config.name)

    def debug(self, msg: str):
        uid = getUID()
        nowTimePrint, nowTimeRecord, timeStamp = getTime(self.config.printTimeFormat, self.config.recordTimeFormat)
        logPrint(msg, LoggerLevel.DEBUG, self.config, uid, self.logStyle, nowTimePrint)
        logRecord(msg, LoggerLevel.DEBUG, self.config, uid, nowTimeRecord)
        self.config.handleFunc(LoggerLevel.DEBUG, msg)
        logNetworkSender(msg, LoggerLevel.DEBUG, self.config, uid, timeStamp)
        return uid

    def info(self, msg: str):
        uid = getUID()
        nowTimePrint, nowTimeRecord, timeStamp = getTime(self.config.printTimeFormat, self.config.recordTimeFormat)
        logPrint(msg, LoggerLevel.INFO, self.config, uid, self.logStyle, nowTimePrint)
        logRecord(msg, LoggerLevel.INFO, self.config, uid, nowTimeRecord)
        self.config.handleFunc(LoggerLevel.INFO, msg)
        logNetworkSender(msg, LoggerLevel.INFO, self.config, uid, timeStamp)
        return uid

    def warn(self, msg: str):
        uid = getUID()
        nowTimePrint, nowTimeRecord, timeStamp = getTime(self.config.printTimeFormat, self.config.recordTimeFormat)
        logPrint(msg, LoggerLevel.WARN, self.config, uid, self.logStyle, nowTimePrint)
        logRecord(msg, LoggerLevel.WARN, self.config, uid, nowTimeRecord)
        self.config.handleFunc(LoggerLevel.WARN, msg)
        logNetworkSender(msg, LoggerLevel.WARN, self.config, uid, timeStamp)
        return uid

    def error(self, msg: str):
        uid = getUID()
        nowTimePrint, nowTimeRecord, timeStamp = getTime(self.config.printTimeFormat, self.config.recordTimeFormat)
        logPrint(msg, LoggerLevel.ERROR, self.config, uid, self.logStyle, nowTimePrint)
        logRecord(msg, LoggerLevel.ERROR, self.config, uid, nowTimeRecord)
        self.config.handleFunc(LoggerLevel.ERROR, msg)
        logNetworkSender(msg, LoggerLevel.ERROR, self.config, uid, timeStamp)
        return uid

    def critical(self, msg: str):
        uid = getUID()
        nowTimePrint, nowTimeRecord, timeStamp = getTime(self.config.printTimeFormat, self.config.recordTimeFormat)
        logPrint(msg, LoggerLevel.CRITICAL, self.config, uid, self.logStyle, nowTimePrint)
        logRecord(msg, LoggerLevel.CRITICAL, self.config, uid, nowTimeRecord)
        self.config.handleFunc(LoggerLevel.CRITICAL, msg)
        logNetworkSender(msg, LoggerLevel.CRITICAL, self.config, uid, timeStamp)
        return uid

    def exception(self, e: BaseException, level: LoggerLevel = LoggerLevel.ERROR):
        if not isinstance(e, BaseException):
            return
        exceptionBaseInfo = traceback.format_exc(limit=None, chain=True)
        exceptionBaseInfoList = exceptionBaseInfo.split("\n")
        exceptionInfo = ""
        for i in range(len(exceptionBaseInfoList)):
            i -= 1
            if i == 0:
                exceptionInfo = exceptionBaseInfoList[i]
                continue
            exceptionInfo = (exceptionInfo + "\n" + " " * (
                    len(
                        getTime(
                            self.config.printTimeFormat,
                            self.config.recordTimeFormat
                        )[0]
                    ) + 1
                    + len(getUID())
                    + 1
                    + MAX_BLANK
                    + 8
            ) + exceptionBaseInfoList[i])
        exceptionLoggerCfg = LoggerConfiger()
        exceptionLoggerCfg.extendBy(self.config)
        exceptionLoggerCfg.setName(self.config.name)
        exceptionLoggerCfg.setMaxPrintLevel(level)
        exceptionLoggerCfg.setMinPrintLevel(level)
        exceptionLoggerCfg.setMaxRecordLevel(level)
        exceptionLoggerCfg.setMinRecordLevel(level)
        exceptionLogger = Logger(exceptionLoggerCfg)
        if level == LoggerLevel.DEBUG:
            exceptionLogger.debug(exceptionInfo)
        elif level == LoggerLevel.INFO:
            exceptionLogger.info(exceptionInfo)
        elif level == LoggerLevel.WARN:
            exceptionLogger.warn(exceptionInfo)
        elif level == LoggerLevel.ERROR:
            exceptionLogger.error(exceptionInfo)
        elif level == LoggerLevel.CRITICAL:
            exceptionLogger.critical(exceptionInfo)

    # def d(self, msg):
    #     self.debug(msg)
    #
    # def i(self, msg):
    #     self.info(msg)
    #
    # def w(self, msg):
    #     self.warn(msg)
    #
    # def e(self, msg):
    #     self.error(msg)
    #
    # def c(self, msg: str):
    #     self.critical(msg)


easyLogBuildInLoggerCfg = LoggerConfiger()
easyLogBuildInLoggerCfg.setName("ceasylog_BuildInLogger")
easyLogBuildInLoggerCfg.setMinPrintLevel(LoggerLevel.WARN)
easyLogBuildInLogger = Logger(easyLogBuildInLoggerCfg)
