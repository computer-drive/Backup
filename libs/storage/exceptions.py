
class InvalidStorageError(Exception):
    def __init__(self, storage_path: str):
        self.storage_path = storage_path
        super().__init__(f"Invalid storage path: {storage_path}")

class StorageFullError(Exception):
    def __init__(self, storage_path: str, current_size:int, max_size: int):
        self.storage_path = storage_path
        self.current_size = current_size
        self.max_size = max_size
        super().__init__(f"Storage '{storage_path}' is full. {current_size} kb/{max_size} kb")
