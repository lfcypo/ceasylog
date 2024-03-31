import os
import platform
import random
import string
import uuid
from datetime import datetime

from colorama import Fore, Style
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


def getTime(timeFormat: str) -> str:
    """
    获取时间
    :param timeFormat: 时间格式
    :return:
    """
    return datetime.now().strftime(timeFormat)


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


def logPrint(msg: str, level: LoggerLevel, config: LoggerConfiger, uid: str, logStyle):
    """
    打印日志
    :param msg: 信息
    :param level: 等级
    :param config: 配置
    :param uid: 唯一标识符
    :param logStyle: logger名称样式
    :return:
    """
    if level.level < config.minPrintLevel.level or level.level > config.maxPrintLevel.level:
        return
    nowTime = getTime(config.printTimeFormat)
    blank = " " * (MAX_BLANK - len(config.name))
    logContent = (f"{Fore.GREEN}{nowTime} {Fore.MAGENTA}{uid} {logStyle}{config.name}{Style.RESET_ALL}{blank} "
                  f"{level.backStyle} {level.msg} {Style.RESET_ALL} {level.frontStyle} {msg}")
    print(logContent)


def logRecord(msg: str, level: LoggerLevel, config: LoggerConfiger, uid: str):
    """
    记录日志到文件
    :param msg: 信息
    :param level: 等级
    :param config: 配置
    :param uid: 唯一标识符
    :return:
    """
    if level.level < config.minRecordLevel.level or level.level > config.maxRecordLevel.level or not config.isRecordB:
        return
    nowTime = getTime(config.recordTimeFormat)
    blank = " " * (MAX_BLANK - len(config.name))
    logContent = f"{nowTime} {uid} {config.name}{blank} {level.msg} {msg}"
    try:
        if not config.recordPath.endswith(getSysFileSplit()):
            recordPath = config.recordPath + getSysFileSplit()
        else:
            recordPath = config.recordPath
        recordFullFileName = recordPath + getTime(config.recordPathNameFormat) + ".log"
        if not os.path.exists(os.path.dirname(recordFullFileName)):
            os.makedirs(os.path.dirname(recordFullFileName))
        with open(recordFullFileName, "a", encoding="utf-8") as logRecordFileObject:
            logRecordFileObject.write(logContent + "\n")
    except Exception as e:
        easyLogBuildInLogger.error("Failed to write log file " + str(e))


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
        self.logStyle = LOG_STYLE[random.randint(0, len(LOG_STYLE) - 1)]

    def debug(self, msg: str):
        uid = getUID()
        logPrint(msg, LoggerLevel.DEBUG, self.config, uid, self.logStyle)
        logRecord(msg, LoggerLevel.DEBUG, self.config, uid)

    def info(self, msg: str):
        uid = getUID()
        logPrint(msg, LoggerLevel.INFO, self.config, uid, self.logStyle)
        logRecord(msg, LoggerLevel.INFO, self.config, uid)

    def warn(self, msg: str):
        uid = getUID()
        logPrint(msg, LoggerLevel.WARN, self.config, uid, self.logStyle)
        logRecord(msg, LoggerLevel.WARN, self.config, uid)

    def error(self, msg: str):
        uid = getUID()
        logPrint(msg, LoggerLevel.ERROR, self.config, uid, self.logStyle)
        logRecord(msg, LoggerLevel.ERROR, self.config, uid)

    def critical(self, msg: str):
        uid = getUID()
        logPrint(msg, LoggerLevel.CRITICAL, self.config, uid, self.logStyle)
        logRecord(msg, LoggerLevel.CRITICAL, self.config, uid)

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
easyLogBuildInLoggerCfg.setName("easyLog_BuildInLogger")
easyLogBuildInLoggerCfg.setMinPrintLevel(LoggerLevel.WARN)
easyLogBuildInLogger = Logger(easyLogBuildInLoggerCfg)
