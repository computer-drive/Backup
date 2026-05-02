from socket import socket
from ..protocol import Protocol
import time
from ..logger import Logger
import json



def recv_exact(conn: socket, size: int):
    data = b""
    while len(data) < size:
        data += conn.recv(size - len(data))
    return data


def handle_client(conn: socket, logger: Logger):
    conn.settimeout(5)

    last_heartbeat = time.time()

    while True:
        try:
            header = recv_exact(conn, 12)
        except TimeoutError:
            logger.warning(json.dumps(
                {
                    "client": conn.getpeername(),
                }
            ), "CLIENT_TIMEOUT") # type: ignore[assignment]
            
            break

        
        if not header:
            break

        protocol = Protocol()
        payload_length = protocol.decode_header(header)

        payload = recv_exact(conn, payload_length)
        protocol.decode_payload(payload)

        if protocol.command == 0x0001:
            last_heartbeat = time.time()
            continue

        if time.time() - last_heartbeat > 10:
            logger.warning(json.dumps(
                {
                    "client": conn.getpeername(),
                    "last_heartbeat": last_heartbeat,
                }
            ), "HEARTBEAT_TIMEOUT") # type: ignore[assignment]
            conn.close()
            break

    

    logger.info(json.dumps(
        {
            "client": conn.getpeername(),
        }
    ), "CLIENT_DISCONNECTED") # type: ignore[assignment]

    conn.close()