import socket
from src.config import config

class BasicService:

    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(BasicService, cls).__new__(cls)
            cls.__instance.__isInit = False

        return cls.__instance

    def __init__(self):
        if self.__isInit:
            pass
        self.__isInit = True

    def init(self):
        self.__send(("init", "0"))

    def takeoff(self):
        self.__send(("takeoff", "0"))

    @staticmethod
    def __send(data: (str, str)):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((config["argos_url"]["host"], config["argos_url"]["port"]))
            s.sendall(f"{data[0]},{data[1]}".encode("utf-8"))
            data = s.recv(1024)

            print(data.decode("utf-8"))

            return data
