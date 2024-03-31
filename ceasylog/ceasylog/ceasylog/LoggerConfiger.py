import ceasylog.LoggerLevel as LoggerLevel


class LoggerConfiger(object):

    def __init__(self):
        self.__name = "default"

        self.__maxPrintLevel = LoggerLevel.CRITICAL
        self.__minPrintLevel = LoggerLevel.DEBUG
        self.__maxRecordLevel = LoggerLevel.CRITICAL
        self.__minRecordLevel = LoggerLevel.WARN

        self.__printTimeFormat = "%Y-%m-%d %H:%M:%S.%f"
        self.__recordTimeFormat = "%Y-%m-%d %H:%M:%S.%f"
        self.__recordPathNameFormat = "%Y-%m-%d"

        self.__isRecordB = False
        self.__recordPath = "./"

    @property
    def name(self):
        return self.__name

    @property
    def maxPrintLevel(self):
        return self.__maxPrintLevel

    @property
    def minPrintLevel(self):
        return self.__minPrintLevel

    @property
    def maxRecordLevel(self):
        return self.__maxRecordLevel

    @property
    def minRecordLevel(self):
        return self.__minRecordLevel

    @property
    def printTimeFormat(self):
        return self.__printTimeFormat

    @property
    def recordTimeFormat(self):
        return self.__recordTimeFormat

    @property
    def recordPathNameFormat(self):
        return self.__recordPathNameFormat

    @property
    def isRecordB(self):
        return self.__isRecordB

    @property
    def recordPath(self):
        return self.__recordPath

    def loadFromFile(self, path: str):
        import os
        import json
        if not os.path.isabs(path):
            # 拼接解释器运行路径作为绝对路径
            path = os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Could not find LoggerConfiger config file: {path}")
        try:
            with open(path, "r", encoding="utf-8") as fileObject:
                fileContent: str = fileObject.read()
            configObject: dict = json.loads(fileContent)
        except Exception as e:
            raise Exception(f"Could not read LoggerConfiger config file: {path} because {str(e)}")
        for key in configObject.keys():
            value = configObject[key]
            if key == "name":
                self.setName(value)
            elif key == "maxPrintLevel":
                if value == "CRITICAL":
                    value = LoggerLevel.CRITICAL
                elif value == "ERROR":
                    value = LoggerLevel.ERROR
                elif value == "WARN":
                    value = LoggerLevel.WARN
                elif value == "INFO":
                    value = LoggerLevel.INFO
                elif value == "DEBUG":
                    value = LoggerLevel.DEBUG
                else:
                    raise ValueError(f"Paser LoggerConfiger failed: Unknown value {value} for key maxPrintLevel")
                self.setMaxPrintLevel(value)
            elif key == "minPrintLevel":
                if value == "CRITICAL":
                    value = LoggerLevel.CRITICAL
                elif value == "ERROR":
                    value = LoggerLevel.ERROR
                elif value == "WARN":
                    value = LoggerLevel.WARN
                elif value == "INFO":
                    value = LoggerLevel.INFO
                elif value == "DEBUG":
                    value = LoggerLevel.DEBUG
                else:
                    raise ValueError(f"Paser LoggerConfiger failed: Unknown value {value} for key minPrintLevel")
                self.setMinPrintLevel(value)
            elif key == "maxRecordLevel":
                if value == "CRITICAL":
                    value = LoggerLevel.CRITICAL
                elif value == "ERROR":
                    value = LoggerLevel.ERROR
                elif value == "WARN":
                    value = LoggerLevel.WARN
                elif value == "INFO":
                    value = LoggerLevel.INFO
                elif value == "DEBUG":
                    value = LoggerLevel.DEBUG
                else:
                    raise ValueError(f"Paser LoggerConfiger failed: Unknown value {value} for key maxRecordLevel")
                self.setMaxRecordLevel(value)
            elif key == "minRecordLevel":
                if value == "CRITICAL":
                    value = LoggerLevel.CRITICAL
                elif value == "ERROR":
                    value = LoggerLevel.ERROR
                elif value == "WARN":
                    value = LoggerLevel.WARN
                elif value == "INFO":
                    value = LoggerLevel.INFO
                elif value == "DEBUG":
                    value = LoggerLevel.DEBUG
                else:
                    raise ValueError(f"Paser LoggerConfiger failed: Unknown value {value} for key minPrintLevel")
                self.setMinRecordLevel(value)
            elif key == "printTimeFormat":
                self.setPrintTimeFormat(value)
            elif key == "recordTimeFormat":
                self.setRecordTimeFormat(value)
            elif key == "recordPathNameFormat":
                self.setRecordPathNameFormat(value)
            elif key == "isRecord":
                self.isRecord(value)
            else:
                raise KeyError(f"Paser LoggerConfiger failed: Unknown key {key}")

    def saveToFile(self, path: str):
        import os
        import json
        # 存储为配置文件的内容
        if self.isRecordB:
            configObject = {
                "name": self.name,
                "maxPrintLevel": self.maxPrintLevel.des,
                "minPrintLevel": self.minPrintLevel.des,
                "maxRecordLevel": self.maxRecordLevel.des,
                "minRecordLevel": self.minRecordLevel.des,
                "printTimeFormat": self.printTimeFormat,
                "recordTimeFormat": self.recordTimeFormat,
                "recordPathNameFormat": self.recordPathNameFormat,
                "isRecord": self.recordPath
            }
        else:
            configObject = {
                "name": self.name,
                "maxPrintLevel": self.maxPrintLevel.des,
                "minPrintLevel": self.minPrintLevel.des,
                "maxRecordLevel": self.maxRecordLevel.des,
                "minRecordLevel": self.minRecordLevel.des,
                "printTimeFormat": self.printTimeFormat,
            }
        configContent: str = json.dumps(configObject, indent=4, ensure_ascii=False)
        if not os.path.isabs(path):
            # 拼接解释器运行路径作为绝对路径
            path = os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        if os.path.exists(path):
            os.remove(path)
        try:
            with open(path, "w", encoding="utf-8") as fileObject:
                fileObject.write(configContent)
        except OSError as e:
            raise OSError(f"Could not save LoggerConfiger config file: {path} because {str(e)}")

    def extendBy(self, father):
        if isinstance(father, LoggerConfiger):
            self.__name = f"default (extends by {father.name})"

            self.__maxPrintLevel = father.maxPrintLevel
            self.__minPrintLevel = father.minPrintLevel
            self.__maxRecordLevel = father.maxRecordLevel
            self.__minRecordLevel = father.minRecordLevel

            self.__printTimeFormat = father.printTimeFormat
            self.__recordTimeFormat = father.recordTimeFormat
            self.__recordPathNameFormat = father.recordPathNameFormat

            self.__isRecordB = father.isRecordB
            self.__recordPath = father.recordPath

    def setName(self, name: str):
        self.__name = name.strip()

    def setMaxPrintLevel(self, maxPrintLevel):
        self.__maxPrintLevel = maxPrintLevel

    def setMinPrintLevel(self, minPrintLevel):
        self.__minPrintLevel = minPrintLevel

    def setMaxRecordLevel(self, maxRecordLevel):
        self.__maxRecordLevel = maxRecordLevel

    def setMinRecordLevel(self, minRecordLevel):
        self.__minRecordLevel = minRecordLevel

    def setPrintTimeFormat(self, printTimeFormat: str):
        self.__printTimeFormat = printTimeFormat

    def setRecordTimeFormat(self, recordTimeFormat: str):
        self.__recordTimeFormat = recordTimeFormat

    def setRecordPathNameFormat(self, printTimeFormat: str):
        self.__printTimeFormat = printTimeFormat

    def isRecord(self, path: str):
        self.__isRecordB = True
        self.__recordPath = path

    def setRecordPath(self, recordPath: str):
        self.__recordPath = recordPath
