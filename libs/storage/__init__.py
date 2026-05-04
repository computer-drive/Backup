from .storage import StorageManager
from ..config import Config
from ..logger import Logger
import json


def init_storages(config: Config, logger: Logger):
    storages = config.get("storages")

    if storages is None or not isinstance(storages, list):
        logger.critical(json.dumps({
            "storages": storages,
        }), "INVALID_CONFIG")
        return
    
    storage_manager = StorageManager(logger)

    for storage in storages:
        if "path" in storage and "max_size" in storage:
            storage_manager.add_storage(storage["path"], storage["max_size"])
        else:
            logger.critical(json.dumps({
            "storages": storages,
        }), "INVALID_CONFIG")
        return

    return storage_manager
    

        
