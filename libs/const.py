import struct

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

PROTOCOL_HEADER = struct.Struct("! I H B I B")


PROTOCOL_LOW_VERSION = 0x001 # 该版本协议的最低版本，兼容该版本及以上版本的协议数据包
PROTOCOL_MAX_VERSION = 0x00F # 该版本协议的最高版本，兼容该版本及以下版本的协议数据包

PROTOCOL_MAGIC = 0x5F86C001

PROTOCOL_PAYLOAD_BINARY = 0x01
PROTOCOL_PAYLOAD_INTEGER = 0x02
PROTOCOL_PAYLOAD_STRING = 0x03
PROTOCOL_PAYLOAD_JSON = 0x04

PROTOCOL_COMMAND_HEARTBEAT = 0x0001
PROTOCOL_COMMAND_TEST = 0x0002
PROTOCOL_COMMAND_DISCONNECT = 0x0003
PROTOCOL_COMMAND_SERVER_CLOSED = 0x0004



