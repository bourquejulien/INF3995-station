from grpc import StatusCode

from src.exceptions.custom_exception import CustomException


class SimulationException(CustomException):
    _code: int
    uri: str

    def __init__(self, name, code, uri):
        self._code = code
        self.uri = uri
        super().__init__(name, code)

    @property
    def unavailable(self):
        return self._code == StatusCode.UNAVAILABLE
