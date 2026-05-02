from socket import socket
from ..protocol import Protocol
import time
from ..logger import Logger

logger = Logger("ServerHandler", "server.log") # type: ignore[assignment]

def recv_exact(conn: socket, size: int):
    data = b""
    while len(data) < size:
        data += conn.recv(size - len(data))
    return data


def handle_client(conn):
    conn.settimeout(5)

    last_heartbeat = time.time()

    while True:
        header = recv_exact(conn, 12)
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
            logger.warning("Client heartbeat timeout", "SERVER") # type: ignore[assignment]
            conn.close()
            break

    conn.close()