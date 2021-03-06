# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import dlp_pb2 as dlp__pb2


class DlpServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Dlp = channel.unary_unary(
                '/rpcpb.DlpService/Dlp',
                request_serializer=dlp__pb2.intext.SerializeToString,
                response_deserializer=dlp__pb2.outtext.FromString,
                )


class DlpServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Dlp(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DlpServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Dlp': grpc.unary_unary_rpc_method_handler(
                    servicer.Dlp,
                    request_deserializer=dlp__pb2.intext.FromString,
                    response_serializer=dlp__pb2.outtext.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'rpcpb.DlpService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class DlpService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Dlp(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/rpcpb.DlpService/Dlp',
            dlp__pb2.intext.SerializeToString,
            dlp__pb2.outtext.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
