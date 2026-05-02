import logging
import sqlite3
import datetime
import threading
import queue
import sys
from libs.thread import ThreadManager

from .const import *

class Database:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.connection: sqlite3.Connection = None #type: ignore[assignment]


    def connect(self):
        '''
        连接数据库。

        Possible exceptions: 
         - sqlite3.Error: 连接数据库时出现的异常
        '''
        self.connection = sqlite3.connect(self.db_name, check_same_thread=False)

    def close(self):
        '''
        关闭数据库连接。
        '''
        if self.connection:
            self.connection.commit()
            self.connection.close()
    
    def init(self):
        '''
        初始化数据库。
        '''
        self.connect()

        now = datetime.datetime.now()
        self.new_log_table(now.strftime('logs_%Y_%m_%d'))
        
        self.current_table = now.strftime('logs_%Y_%m_%d')

    def new_log_table(self, table_name: str):
        '''
        创建新的数据库表。
        '''
        self.connection.execute(LOG_DATABASE_NEW_SQL.format(table_name=table_name))
        self.connection.commit()

    def execute(self, sql: str, params: tuple = ()):
        '''
        执行SQL语句。
        注意：本方法不主动提交
        '''
        self.connection.execute(sql, params)

def get_current_table_name():
    now = datetime.datetime.now()
    return now.strftime('logs_%Y_%m_%d')



def db_logger_worker(db_name: str, q: queue.Queue):
    db = Database(db_name)
    db.init()

    current_table_name = get_current_table_name()
    db.new_log_table(current_table_name)

    log_buffer_count = 0

    while True:
        log_entry = q.get()
        if log_entry is None:
            q.task_done()
            break

        time_str, level_int, class_name, log_type, message_type, message = log_entry

        if current_table_name != get_current_table_name():
            current_table_name = get_current_table_name()
            db.new_log_table(current_table_name)
        

        db.execute(f'''
INSERT INTO {current_table_name} (timestamp, level, class_name, type, message_type, message)
VALUES (?, ?, ?, ?, ?, ?)
''', (time_str, level_int, class_name, log_type, message_type, message))

        log_buffer_count += 1
        if log_buffer_count >= 100:
            db.connection.commit()
            log_buffer_count = 0
        
        q.task_done()

    db.close()


class LoggerManager:
    def __init__(self, db_name:str, thread_manager: ThreadManager):
        self.db_name = db_name
        self.q = queue.Queue(maxsize=10000)

        self.worker_thread = thread_manager.create_thread(name="LOGGER", target=db_logger_worker, args=(self.db_name, self.q), daemon=False)
        self.worker_thread.start()

    def get_logger(self, name: str):
        return Logger(name, self.q, self.db_name)  

    def close(self):
        logging.shutdown()
        
        self.q.put(None)
        self.q.join()
        self.worker_thread.join()


class Logger(logging.Logger):
    def __init__(self, name: str,  q: queue.Queue, db_name: str = LOG_DATABASE_NAME,):
        super().__init__(name)

        self.db_handler = DatabaseHandler(db_name, q)
        self.addHandler(self.db_handler)

        self.console_handler = logging.StreamHandler(sys.stdout)
        self.console_handler.setFormatter(ConsoleFormatter())
        self.addHandler(self.console_handler)

        self.class_name = name

    def log(self, level: int, msg: str, log_type:str, class_name: str):
        super().log(level, msg, extra={'log_type': log_type, 'class_name': class_name if class_name else self.class_name})

    def warning(self, msg: str, log_type:str, class_name: str = None):#type: ignore
        self.log(logging.WARNING, msg, log_type, class_name)

    def error(self, msg: str, log_type:str, class_name: str = None):#type: ignore
        self.log(logging.ERROR, msg, log_type, class_name)
        
    def critical(self, msg: str, log_type:str, class_name: str = None):#type: ignore
        self.log(logging.CRITICAL, msg, log_type, class_name)

    def info(self, msg: str, log_type:str, class_name: str = None): #type: ignore
        self.log(logging.INFO, msg, log_type, class_name)

    def debug(self, msg: str, log_type:str,  class_name: str = None): #type: ignore
        self.log(logging.DEBUG, msg, log_type, class_name)



class DatabaseHandler(logging.Handler):
    def __init__(self, db_name: str, q: queue.Queue):
        super().__init__()
        self.q = q
        

    

    def emit(self, record: logging.LogRecord):

        time = datetime.datetime.fromtimestamp(record.created)
        
        level = ""
        match record.levelno:
            case logging.DEBUG:
                level = "DEBUG"
            case logging.INFO:
                level = "INFO"
            case logging.WARNING:
                level = "WARNING"
            case logging.ERROR:
                level = "ERROR"
            case logging.CRITICAL:
                level = "CRITICAL"
            case _:
                level = "INFO"

        # 转换时间戳为字符串
        time = datetime.datetime.fromtimestamp(record.created)
        time_str = time.strftime('%Y,%m,%d,%H,%M,%S')

        # 将日志级别转换为整数
        level_int = 0
        match level:
            case 'DEBUG':
                level_int = 0
            case 'INFO':
                level_int = 1
            case 'WARNING':
                level_int = 2
            case 'ERROR':
                level_int = 3
            case 'CRITICAL':
                level_int = 4
            case _:
                level_int = 1


        self.q.put((time_str, level_int, record.class_name, record.log_type, "unknown", record.getMessage())) #type: ignore

        
class ConsoleFormatter(logging.Formatter):
    def __init__(self):
        super().__init__(
            LOG_FORMAT
        )
    def format(self, record: logging.LogRecord) -> str:
        match record.levelno:
            case logging.DEBUG:
                record.levelname = f"\033[94m{record.levelname}\033[0m"
                record.color = ""
            case logging.INFO:
                record.levelname = f"\033[32m{record.levelname}\033[0m"
                record.color = ""
            case logging.WARNING:
                record.color = "\033[93m"
            case logging.ERROR:
                record.color = "\033[91m"
            case logging.CRITICAL:
                record.color = "\033[95m"
            case _:
                record.color = "\033[92m"

        record.reset = "\033[0m"

        return super().format(record)
    
        



    

        
        