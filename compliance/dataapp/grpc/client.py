import grpc
from . import dlp_pb2
from . import dlp_pb2_grpc

def run(input):
    # 连接 rpc 服务器
    conn = grpc.insecure_channel('localhost:10086')
    # 调用 rpc 服务
    client = dlp_pb2_grpc.DlpServiceStub(conn)
    req = client.Dlp(dlp_pb2.intext(msg=input))
    print("python client received: " + req.msg)
    return req.msg


