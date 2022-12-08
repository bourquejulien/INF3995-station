import pytest
import grpc
from src.exceptions.custom_exception import CustomException
from src.services.firmware_service.remote_compiler_client import RemoteCompilerClient


@pytest.fixture()
def rc_client(mocker):
    yield RemoteCompilerClient('host')


def test_enter(app, mocker, rc_client):
    rc_client._channel = 'test'
    grpc_mock = mocker.patch('src.services.firmware_service.remote_compiler_client.grpc')
    compiler_pb2_mock = mocker.patch('src.services.firmware_service.remote_compiler_client.compiler_pb2_grpc')

    rc_client.__enter__()


def test_exit(app, mocker, rc_client):
    rc_client.id = 'test'
    rc_client.end_session = mocker.Mock()
    rc_client._channel = mocker.Mock()
    rc_client._channel.__exit__ = mocker.Mock()

    rc_client.__exit__(0, 0, 0)

    rc_client.end_session.assert_called_once()


def test_is_ready(app, mocker, rc_client):
    grpc_mock = mocker.patch('src.services.firmware_service.remote_compiler_client.grpc')
    result = rc_client.is_ready(0)

    grpc_mock.channel_ready_future.assert_called_once()
    assert result


def test_is_ready_error(app, mocker, rc_client):
    grpc_mock = mocker.patch('src.services.firmware_service.remote_compiler_client.grpc')
    grpc_mock.channel_ready_future.side_effect = grpc.FutureTimeoutError()

    result = rc_client.is_ready(0)

    grpc_mock.channel_ready_future.assert_called_once()
    assert not result


def test_start_session(app, mocker, rc_client):
    compiler_pb2_mock = mocker.patch('src.services.firmware_service.remote_compiler_client.compiler_pb2')
    rc_client.stub = mocker.Mock()

    rc_client.start_session()

    rc_client.stub.StartSession.assert_called_once()
    compiler_pb2_mock.StartRequest.assert_called_once()


def test_start_session_error(app, mocker, rc_client):
    compiler_pb2_mock = mocker.patch('src.services.firmware_service.remote_compiler_client.compiler_pb2')
    rc_client.stub = mocker.Mock()
    error = grpc.RpcError()
    error.code = lambda: grpc.StatusCode.INVALID_ARGUMENT
    compiler_pb2_mock.StartRequest.side_effect = error

    try:
        rc_client.start_session()
    except CustomException as e:
        assert e.name == 'RPCError: '

    compiler_pb2_mock.StartRequest.assert_called_once()


def test_end_session(app, mocker, rc_client):
    compiler_pb2_mock = mocker.patch('src.services.firmware_service.remote_compiler_client.compiler_pb2')
    rc_client.stub = mocker.Mock()

    rc_client.end_session()

    rc_client.stub.EndSession.assert_called_once()
    compiler_pb2_mock.CompilerRequest.assert_called_once()


def test_end_session_error(app, mocker, rc_client):
    compiler_pb2_mock = mocker.patch('src.services.firmware_service.remote_compiler_client.compiler_pb2')
    rc_client.stub = mocker.Mock()
    error = grpc.RpcError()
    error.code = lambda: grpc.StatusCode.INVALID_ARGUMENT
    compiler_pb2_mock.CompilerRequest.side_effect = error

    try:
        rc_client.end_session()
    except CustomException as e:
        assert e.name == 'RPCError: '

    compiler_pb2_mock.CompilerRequest.assert_called_once()


def test_edit(app, mocker, rc_client):
    compiler_pb2_mock = mocker.patch('src.services.firmware_service.remote_compiler_client.compiler_pb2')
    rc_client.stub = mocker.Mock()

    rc_client.edit('', [])

    rc_client.stub.Edit.assert_called_once()
    compiler_pb2_mock.EditRequest.assert_called_once()


def test_edit_error(app, mocker, rc_client):
    compiler_pb2_mock = mocker.patch('src.services.firmware_service.remote_compiler_client.compiler_pb2')
    rc_client.stub = mocker.Mock()
    error = grpc.RpcError()
    error.code = lambda: grpc.StatusCode.INVALID_ARGUMENT
    compiler_pb2_mock.EditRequest.side_effect = error

    try:
        rc_client.edit('', [])
    except CustomException as e:
        assert e.name == 'RPCError: '

    compiler_pb2_mock.EditRequest.assert_called_once()


def test_get(app, mocker, rc_client):
    compiler_pb2_mock = mocker.patch('src.services.firmware_service.remote_compiler_client.compiler_pb2')
    rc_client.stub = mocker.Mock()

    rc_client.get('')

    rc_client.stub.Get.assert_called_once()
    compiler_pb2_mock.GetRequest.assert_called_once()


def test_get_error(app, mocker, rc_client):
    compiler_pb2_mock = mocker.patch('src.services.firmware_service.remote_compiler_client.compiler_pb2')
    rc_client.stub = mocker.Mock()
    error = grpc.RpcError()
    error.code = lambda: grpc.StatusCode.INVALID_ARGUMENT
    compiler_pb2_mock.GetRequest.side_effect = error

    try:
        rc_client.get('')
    except CustomException as e:
        assert e.name == 'RPCError: '

    compiler_pb2_mock.GetRequest.assert_called_once()
