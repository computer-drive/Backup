import struct
from libs.const import *
from dataclasses import dataclass
from .parse import ParseManager

@dataclass
class Protocol:
    magic: int
    command: int
    payload_type: int
    payload_length: int
    reserved: int
    payload: bytes

    def __init__(self, magic: int = None , command: int = None, payload_type: int = None, reserved: int = 0, payload: bytes = b""):
        self.magic = magic
        self.command = command
        self.payload_type = payload_type
        self.reserved = reserved
        self.payload = payload
        self.payload_length = len(self.payload)

    def encode(self) -> bytes:
        '''编码协议数据包'''
        return PROTOCOL_HEADER.pack(
            self.magic,
            self.command,
            self.payload_type,
            self.payload_length,
            self.reserved
        ) + self.payload
    
    def decode_header(self, header: bytes,):
        '''解码协议数据包的Header， 返回Payload长度'''
        header = header[:PROTOCOL_HEADER.size]

        self.magic, self.command, self.payload_type, self.payload_length, self.reserved = PROTOCOL_HEADER.unpack(header)

        return self.payload_length
    
    def decode_payload(self, payload: bytes):
        '''解码协议数据包的Payload'''
        self.payload = payload[:self.payload_length]
        parse_manager = ParseManager()
        self.payload = parse_manager.parse_single(self.payload, self.payload_type)

    def to_dict(self):
        return {
            "magic": self.magic,
            "command": self.command,
            "payload_type": self.payload_type,
            "payload_length": self.payload_length,
            "reserved": self.reserved,
            "payload": self.payload
        }
    
    def check(self, raise_exception: bool = False) -> bool:
        '''检查数据包是否有效'''
        if self.magic >> 12 != 0x5F86C:  # 去除后12位，检查前20位是否为0x5F86C
            if raise_exception:
                raise ValueError("Invalid magic number")
            return False
        elif not(PROTOCOL_LOW_VERSION <= self.magic & 0xFFF <= PROTOCOL_MAX_VERSION):
            if raise_exception:
                raise ValueError("Unsupported protocol version")
            return False
        
        return True
        
    
if __name__ == "__main__":
    protocol = Protocol()
    protocol.magic = 0x12345678
    protocol.command = 1
    protocol.payload_type = 0x01
    protocol.reserved = 0

    payload = b"Hello, World!"
    encoded_data = protocol.encode(payload)

    print("Encoded Data:", encoded_data)

    # 解码协议数据包
    decoded_protocol = Protocol()
    payload_length = decoded_protocol.decode_header(encoded_data)
    decoded_protocol.decode_payload(encoded_data[PROTOCOL_HEADER.size:])

    print("Decoded Protocol:", decoded_protocol.__dict__())
    
    



    


