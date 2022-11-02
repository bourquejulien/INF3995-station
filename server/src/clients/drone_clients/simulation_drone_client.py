import grpc
from out import simulation_pb2_grpc, simulation_pb2
from src.exceptions.custom_exception import CustomException


class SimulationDroneClient:
    uri: str

    def __init__(self, hostname, uri):
        self.uri = uri
        self.channel = None
        self.stub = None
        self.address = f"{hostname}:{uri}"

    def identify(self):
        try:
            pass
        except grpc.RpcError as e:
            print(e)
            raise CustomException("RPCError: ", e.code()) from e

    def start_mission(self):
        try:
            self.stub.StartMission(simulation_pb2.MissionRequest(uri=self.uri))
        except grpc.RpcError as e:
            print(e)
            raise CustomException("RPCError: ", e.code()) from e

    def end_mission(self):
        try:
            self.stub.EndMission(simulation_pb2.MissionRequest(uri=self.uri))
        except grpc.RpcError as e:
            print(e)
            raise CustomException("RPCError: ", e.code()) from e

    def force_end_mission(self):
        try:
            self.stub.EndMission(simulation_pb2.MissionRequest(uri=self.uri))
        except grpc.grpc.RpcError as e:
            print(e)
            raise CustomException("RPCError: ", e.code()) from e

    def connect(self):
        self.channel = grpc.insecure_channel(self.address)
        self.stub = simulation_pb2_grpc.SimulationStub(self.channel)

    def disconnect(self):
        self.channel.close()

    def get_position(self):
        try:
            reply = self.stub.GetPosition(simulation_pb2.MissionRequest(uri=self.uri))
            return reply
        except grpc.RpcError as e:
            print(e)
            raise CustomException("RPCError: ", e.code()) from e
