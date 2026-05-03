import socket
from libs.const import *
from libs.protocol import Protocol
import time
import threading
import queue


def input_worker(conn: socket.socket):
    while True:
        line = input(">> ")
        if line == "exit":
            break
        else:
            try:
                conn.send(
                    Protocol(0x5F86C001, PROTOCOL_COMMAND.TEST, PROTOCOL_PAYLOAD_STRING, 0, line.encode() ).
                    encode()
                )
                
            except Exception as e:
                import traceback
                traceback.print_exc()

            print("send command.")
                



client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("connecting...")
try:
    client.connect(("127.0.0.1", 8080))
except Exception as e:
    print(e)
    print("connect failed.")
    exit(1)

print("connect success.")

client.send(Protocol(0x5F86C001, PROTOCOL_COMMAND.HEARTBEAT, PROTOCOL_PAYLOAD_BINARY).encode())

q = queue.Queue()
input_worker_thread = threading.Thread(target=input_worker, args=(client,), daemon=True)
input_worker_thread.start()

last_heartbeat = time.time()

client.settimeout(5)

def send_heartbeat():
    global last_heartbeat
    if last_heartbeat + 5 < time.time():
        client.send(Protocol(0x5F86C001, PROTOCOL_COMMAND.HEARTBEAT, PROTOCOL_PAYLOAD_BINARY).encode())
        last_heartbeat = time.time()
        print("sned heartbeat.")

while True:
    try:
        send_heartbeat()

        try:
            header = b''
            while len(header) < 12:
                chunk = client.recv(12 - len(header))
                if not chunk:
                    break
                header += chunk
        except socket.timeout:
            continue
        
        if not header:
            continue    
        
        protocol = Protocol()
        payload_length = protocol.decode_header(header)

        if protocol.command == PROTOCOL_COMMAND.DISCONNECT:
            print("server disconnect.")
            break

        if protocol.command == PROTOCOL_COMMAND.SERVER_CLOSED:
            print("server closed.")
            break

        print(protocol)

        
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        break

client.close()

input_worker_thread.join()

print("disconeected.")

            
    


