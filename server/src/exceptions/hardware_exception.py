from src.exceptions.custom_exception import CustomException


class HardwareException(CustomException):
    def __init__(self, name, message):
        super().__init__(name, message)
