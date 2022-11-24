import grpc
from out import simulation_pb2_grpc, simulation_pb2
from src.exceptions.custom_exception import CustomException


class SimulationDroneClient:
    uri: str

    def __init__(self, hostname, uri):
        self.uri = uri
        self._channel = None
        self._stub = None
        self._address = f"{hostname}:{uri}"

    def is_ready(self, timeout: int):
        try:
            grpc.channel_ready_future(self._channel).result(timeout=timeout)
            return True
        except grpc.FutureTimeoutError:
            return False

    def connect(self):
        self._channel = grpc.insecure_channel(self._address)
        self._stub = simulation_pb2_grpc.SimulationStub(self._channel)

    def disconnect(self):
        self._channel.close()

    def identify(self):
        try:
            pass
        except grpc.RpcError as e:
            print(e)
            raise CustomException("RPCError: ", e.code()) from e

    def start_mission(self):
        try:
            self._stub.StartMission(simulation_pb2.MissionRequest(uri=self.uri))
        except grpc.RpcError as e:
            print(e)
            raise CustomException("RPCError: ", e.code()) from e

    def end_mission(self):
        try:
            self._stub.EndMission(simulation_pb2.MissionRequest(uri=self.uri))
        except grpc.RpcError as e:
            print(e)
            raise CustomException("RPCError: ", e.code()) from e

    def force_end_mission(self):
        try:
            self._stub.EndMission(simulation_pb2.MissionRequest(uri=self.uri))
        except grpc.RpcError as e:
            print(e)
            raise CustomException("RPCError: ", e.code()) from e

    def get_telemetrics(self):
        try:
            reply = self._stub.GetTelemetrics(simulation_pb2.MissionRequest(uri=self.uri))
            return reply
        except grpc.RpcError as e:
            print(e)
            raise CustomException("RPCError: ", e.code()) from e

    def get_distances(self):
        try:
            reply = self._stub.GetDistances(simulation_pb2.MissionRequest(uri=self.uri))
            return reply
        except grpc.RpcError as e:
            print(e)
            raise CustomException("RPCError: ", e.code()) from e

    def get_logs(self):
        try:
            reply = self._stub.GetLogs(simulation_pb2.MissionRequest(uri=self.uri))
            return reply
        except grpc.RpcError as e:
            print(e)
            raise CustomException("RPCError: ", e.code()) from e
