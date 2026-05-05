from ..logger import Logger
from dataclasses import dataclass
import os
import json
from .exceptions import InvalidStorageError, StorageFullError
@dataclass
class Storage:
    path: str
    max_size: int
    current_size: int = 0

class StorageManager:
    def __init__(self, logger: Logger):
        self.logger = logger
        self.storages: list[Storage] = []


    def add_storage(self, path: str, max_size: int):
        '''
        添加一个存储路径，检查有效性与大小。

        Return: bool 是否成功添加

        Exceptions: 可能会抛出InvalidStorageError或StorageFullError异常。
        '''
        storage = Storage(path, max_size)

        self._check(storage)
        
        self.storages.append(storage)

        return True

    def _check(self, storage: Storage):
        # 检查存储路径是否存在且为目录
        if not (os.path.exists(storage.path) and os.path.isdir(storage.path)):
            # self.logger.error(json.dumps({
            #     "storage_path": storage.path,
            # }), "INVALID_STORAGE")
            raise InvalidStorageError(storage.path)

            return False

        # 检查存储路径大小是否超过最大限制
        storage.current_size = os.path.getsize(storage.path)

        if storage.current_size >= storage.max_size:
            # self.logger.error(json.dumps({
            #     "storage_path": storage.path,
            #     "current_size": storage.current_size,
            #     "max_size": storage.max_size,
            # }), "STORAGE_FULL")
            raise StorageFullError(storage.path, storage.current_size, storage.max_size)

            return False
        
        return True

    

            

        


    
    




        


