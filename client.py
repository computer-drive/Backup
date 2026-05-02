import socket
from libs.const import *
from libs.protocol import Protocol

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 8080))

print("连接成功")

def send_packet(string: str):
    payload = string.encode()

    packet = Protocol(
        magic=0x5F86C001,
        command=0x0001,
        payload_type=0x03,
        payload=payload,
    )

    client.send(packet.encode())
    print("发送成功") 


while True:
    send_packet(input())


