from socket import socket
from ..protocol import Protocol
import time
from ..logger import Logger
import json
from ..const import *
import threading
import traceback

def handle_test(conn: socket, protocol: Protocol, logger: Logger, ):
    '''解析test命令'''
    if not protocol.check():
        conn.send(
            Protocol(
                PROTOCOL_MAGIC,
                PROTOCOL_COMMAND.UNSUPPORTED,
                PROTOCOL_PAYLOAD_BINARY,
            ).encode()
        )
        logger.warning(json.dumps(
            {
                "client": conn.getpeername(),
                "magic": protocol.magic
            }
        ), "UNUPPORTED") # type: ignore[assignment]
        return False
    
    ## 回复test命令
    conn.send(Protocol(0x5F86C001, PROTOCOL_COMMAND.TEST, PROTOCOL_PAYLOAD_STRING, 0, b"reply").encode())

    return True
    


def recv_exact(conn: socket, size: int, stop_event: threading.Event = None):
    data = b""
    conn.settimeout(5)

    while len(data) < size:
    
        
        try:
            chunk = conn.recv(size - len(data))
            if not chunk:
                # print("no data received")
                return None
            data += chunk
            
        except TimeoutError:
            # print("timeout")
            pass

        except ConnectionResetError:
            # print("connection reset")
            return None
        
        if stop_event and stop_event.is_set():
            # print("stop event set")
            return None
        
    return data


def handle_client(conn: socket, logger: Logger, stop_event: threading.Event):
    # 设置超时时间为5秒
    conn.settimeout(5)

    # 最后一次心跳时间
    last_heartbeat = time.time()

    while not stop_event.is_set():
        try:
            header = recv_exact(conn, 12,stop_event) # 读取协议头12bytes
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

        if not protocol.check():
            conn.send(Protocol(
                PROTOCOL_MAGIC,
                PROTOCOL_COMMAND.INVALID_HEADER,
                PROTOCOL_PAYLOAD_BINARY,
            ).encode())
            continue

        if payload_length > MAX_PAYLOAD_SIZE:
            conn.send(Protocol(
                PROTOCOL_MAGIC,
                PROTOCOL_COMMAND.INVALID_PAYLOAD,
                PROTOCOL_PAYLOAD_BINARY,
            ).encode())
            continue
        
        try:
            payload = recv_exact(conn, payload_length, stop_event) # 读取payload 
                
        except TimeoutError:
            pass

        
        try:
            protocol.decode_payload(payload) # 解析payload
        except Exception as e:
            logger.error(json.dumps(
                {
                    "client": conn.getpeername(),
                    "exception": e.__class__.__name__,
                    "detail": str(e),
                    "traceback": traceback.format_exc(),
                }
            ), "DECODE_PAYLOAD_ERROR") # type: ignore[assignment]
            continue 

        ## 处理命令
        if protocol.command == 0x0001:
            last_heartbeat = time.time()
            continue
        elif protocol.command == 0x0002:
            if not handle_test(conn, protocol, logger):
                break


        ## 处理心跳
        if time.time() - last_heartbeat > 10:
            # print("heartbeat timeout")

            logger.warning(json.dumps(
                {
                    "client": conn.getpeername(),
                    "last_heartbeat": last_heartbeat,
                }
            ), "HEARTBEAT_TIMEOUT") # type: ignore[assignment]

            
            break
        else:
            pass
            # print("heartbeat test pass")
    
    conn.send(Protocol(0x5F86C001, PROTOCOL_COMMAND.SERVER_CLOSED, PROTOCOL_PAYLOAD_BINARY, 0, b"").encode())

    ## 断开连接
    logger.info(json.dumps(
        {
            "client": conn.getpeername(),
        }
    ), "CLIENT_DISCONNECTED") # type: ignore[assignment]

    conn.close()