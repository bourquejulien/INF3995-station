import grpc

from out import simulation_pb2_grpc, simulation_pb2
from src.config import config


class SimulationDroneClient:
    uri: str

    def __init__(self, uri):
        self.uri = uri
        self.channel = None
        self.stub = None
        self.address = f"{config['argos_url']['host']}:{uri}"

    def identify(self):
        pass

    def start_mission(self):
        self.stub.StartMission(simulation_pb2.MissionRequest(uri=self.uri))

    def end_mission(self):
        self.stub.EndMission(simulation_pb2.MissionRequest(uri=self.uri))

    def connect(self):
        self.channel = grpc.insecure_channel(self.address)
        self.stub = simulation_pb2_grpc.SimulationStub(self.channel)

    def disconnect(self):
        self.channel.close()
