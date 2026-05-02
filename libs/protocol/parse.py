from ..const import *
import json

class ParseManager:
    def __init__(self):
        self.parsers : dict[int, callable] = {}
        
        self.register_parser(0x01, parse_binary)
        self.register_parser(0x02, parse_int)
        self.register_parser(0x03, parse_string)
        self.register_parser(0x04, parse_json)

    def register_parser(self, payload_type: int, parser):
        self.parsers[payload_type] = parser


        
    def parse_single(self, payload: bytes, payload_type: int):
        if payload_type  not in self.parsers:
            raise ValueError(f"Unsupported payload type: {payload_type}")
        
        return self.parsers[payload_type](payload)

def parse_binary(payload: bytes):
    return payload

def parse_int(payload: bytes):
    if len(payload) != 4:
        raise ValueError("Invalid payload length for int type")
    return int.from_bytes(payload, byteorder='big')

def parse_string(payload: bytes):
    return payload.decode('utf-8')

def parse_json(payload: bytes):
    return json.loads(payload.decode('utf-8'))