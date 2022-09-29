import grpc

from out import simulation_pb2_grpc, simulation_pb2
from src.clients.drone_clients.drone_client import DroneClient


class SimDroneClient(DroneClient):
    def __init__(self, uri):
        self.uri = uri
        self.channel = None
        self.stub = None
        self.address = f"{config['argos_url']['host']}:{uri}"

    def identify(self):
        pass

    def start_mission(self):
        response = self.stub.StartMission(simulation_pb2.MissionRequest(uri=self.uri))

    def end_mission(self):
        response = self.stub.EndMission(simulation_pb2.MissionRequest(uri=self.uri))

    def connect(self):
        self.channel = grpc.aio.insecure_channel(self.address)
        self.stub = simulation_pb2_grpc.SimulationStub(self.channel)

    def disconnect(self):
        self.channel.close()
