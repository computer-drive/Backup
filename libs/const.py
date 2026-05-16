import struct

DEFAULT_SERVER_CONFIG = {
    "server.address": "0.0.0.0",
    "server.port": 8080,
    "log.database": "log.db",
    "storages.storage": [],
    "storage.index_database": "storage.db",
    "handle_error": {
        "invalid_storage_path": 1,
        "storage_full": 1,
    }
}

DEFAULT_CLIENT_CONFIG = {
    "server.address": "localhost",
    "server.port": 8080
}

LOG_FORMAT = "%(color)s[%(asctime)s/%(class_name)s][%(levelname)s](%(log_type)s) %(message)s%(reset)s"

LOG_DATABASE_NAME = "log.db"

LOG_DATABASE_NEW_SQL = '''
CREATE TABLE IF NOT EXISTS {table_name} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    level INTEGER NOT NULL,                            
    class_name TEXT NOT NULL,
    type TEXT NOT NULL,
    message_type TEXT NOT NULL,
    message TEXT NOT NULL       
    )                     
'''

CLIENT_LOG_FORMAT = "%(color)s%(levelname)s: %(message)s%(reset)s"

PROTOCOL_HEADER = struct.Struct("! I H B I B")


PROTOCOL_LOW_VERSION = 0x001 # 该版本协议的最低版本，兼容该版本及以上版本的协议数据包
PROTOCOL_MAX_VERSION = 0x00F # 该版本协议的最高版本，兼容该版本及以下版本的协议数据包

PROTOCOL_MAGIC = 0x5F86C001

PROTOCOL_PAYLOAD_BINARY = 0x01
PROTOCOL_PAYLOAD_INTEGER = 0x02
PROTOCOL_PAYLOAD_STRING = 0x03
PROTOCOL_PAYLOAD_JSON = 0x04

class ProtocolCommand:


    HEARTBEAT = 0x0001
    TEST = 0x0002
    DISCONNECT = 0x0003
    SERVER_CLOSED = 0x0004

    UNSUPPORTED = 0x0F01
    INVALID_HEADER = 0x0F02
    INVALID_PAYLOAD = 0x0F03

PROTOCOL_COMMAND = ProtocolCommand()

MAX_PAYLOAD_SIZE = 1024 * 1024 * 1024 # 最大payload大小为1GB
    






