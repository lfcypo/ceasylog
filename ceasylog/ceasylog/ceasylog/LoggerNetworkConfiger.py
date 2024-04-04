class LoggerNetworkConfiger(object):
    def __init__(self):
        self.__endpoint = "http://127.0.0.1:8080"
        self.__header = {"Content-Type": "application/json"}

    @property
    def endpoint(self):
        return self.__endpoint

    @property
    def header(self):
        return self.__header

    def setEndpoint(self, endpoint: str):
        if not endpoint.startswith("http://") or endpoint.startswith("https://"):
            raise Exception("Invalid endpoint: endpoint MUST start with http:// or https://")
        self.__endpoint = endpoint

    def setHeader(self, header: dict):
        self.__header = header
