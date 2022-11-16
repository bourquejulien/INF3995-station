import grpc
from out import compiler_pb2_grpc, compiler_pb2
from src.exceptions.custom_exception import CustomException


class SimulationDroneClient:
    address: str

    def __init__(self, connection_string: str):
        self.channel = None
        self.stub = None
        self.id = None
        self.address = connection_string

    def connect(self):
        self.channel = grpc.insecure_channel(self.address)
        self.stub = compiler_pb2_grpc.CompilerStub(self.channel)

    def disconnect(self):
        self.channel.close()

    def start_session(self):
        try:
            reply = self.stub.StartSession(compiler_pb2.StartRequest())
            self.id = reply.id
        except grpc.RpcError as e:
            raise CustomException("RPCError: ", e.code()) from e

    def end_session(self):
        try:
            self.stub.EndSession(compiler_pb2.CompilerRequest(id=self.id))
        except grpc.RpcError as e:
            raise CustomException("RPCError: ", e.code()) from e

    def edit(self, path: str, file: bytes):
        try:
            self.stub.Edit(compiler_pb2.EditRequest(id=self.id, path=path, file=file))
        except grpc.RpcError as e:
            raise CustomException("RPCError: ", e.code()) from e

    def get(self, path: str):
        try:
            data_block = self.stub.Get(compiler_pb2.GetRequest(id=self.id, path=path))
            return data_block.data.decode("utf-8")
        except grpc.RpcError as e:
            raise CustomException("RPCError: ", e.code()) from e

    def build(self):
        try:
            stream = self.stub.Build(compiler_pb2.CompilerRequest(id=self.id))
            for data_block in stream:
                yield data_block

        except grpc.RpcError as e:
            raise CustomException("RPCError: ", e.code()) from e
