from socket import socket
from ..protocol import Protocol
import time
from ..logger import Logger
import json
from ..const import *
import threading

def handle_test(conn: socket, protocol: Protocol, logger: Logger):
    '''解析test命令'''
    logger.debug(protocol.payload, "TEST_COMMAND")

    ## 回复test命令
    conn.send(Protocol(0x5F86C001, PROTOCOL_COMMAND_TEST, PROTOCOL_PAYLOAD_STRING, 0, b"reply").encode())
    


def recv_exact(conn: socket, size: int):
    data = b""
    while len(data) < size:
        data += conn.recv(size - len(data))

        if not data:
            return None
        
    return data


def handle_client(conn: socket, logger: Logger, stop_event: threading.Event):
    # 设置超时时间为5秒
    conn.settimeout(5)

    # 最后一次心跳时间
    last_heartbeat = time.time()

    while not stop_event.is_set():
        try:
            header = recv_exact(conn, 12) # 读取协议头12bytes
        except TimeoutError:
            pass

        
        if not header: # 如果协议头为空，说明客户端关闭了连接
            logger.warning(json.dumps(
        {
            "client": conn.getpeername(),
        }
    ), "NO_HEADER") # type: ignore[assignment]
            break
        
        ## 解析数据包
        protocol = Protocol() # 创建协议对象
        payload_length = protocol.decode_header(header) # 解析协议头

        try:
            payload = recv_exact(conn, payload_length) # 读取payload 
            protocol.decode_payload(payload) # 解析payload
        except TimeoutError:
            pass


        ## 处理命令
        if protocol.command == 0x0001:
            last_heartbeat = time.time()
            continue
        elif protocol.command == 0x0002:
            handle_test(conn, protocol, logger)


        ## 处理心跳
        if time.time() - last_heartbeat > 10:
            print("heartbeat timeout")

            logger.warning(json.dumps(
                {
                    "client": conn.getpeername(),
                    "last_heartbeat": last_heartbeat,
                }
            ), "HEARTBEAT_TIMEOUT") # type: ignore[assignment]

            
            break
        else:
            print("heartbeat test pass")
    
    conn.send(Protocol(0x5F86C001, PROTOCOL_COMMAND_SERVER_CLOSED, PROTOCOL_PAYLOAD_BINARY, 0, b"").encode())

    ## 断开连接
    logger.info(json.dumps(
        {
            "client": conn.getpeername(),
        }
    ), "CLIENT_DISCONNECTED") # type: ignore[assignment]

    conn.close()