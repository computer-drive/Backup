from .storage import StorageManager
from ..config import Config
from ..logger import Logger
from .exceptions import InvalidStorageError, StorageFullError
import json
from threading import Event

def init_storages(config: Config, logger: Logger):
    storages = config.get("storages.storage")

    if storages is None or not isinstance(storages, list):
        logger.critical(json.dumps({
            "storages": storages,
        }), "INVALID_CONFIG")
        return
    
    storage_manager = StorageManager(logger)

    # 遍历存储
    for storage in storages:
        # 检查“path”和“max_size”是否存在
        if "path" in storage and "max_size" in storage:
            # 存在，尝试添加存储路径

            try:
                storage_manager.add_storage(storage["path"], storage["max_size"])
            except InvalidStorageError as e:
                # 存储路径错误
                logger.error(json.dumps({
                    "storage_path": e.storage_path,
                }), "INVALID_STORAGE")
                return 
            
            except StorageFullError as e:
                # 存储已满

                logger.error(json.dumps({
                    "storage_path": e.storage_path,
                    "current_size": e.current_size,
                    "max_size": e.max_size,
                }), "STORAGE_FULL")
                return
            
            
            # if not storage_manager.add_storage(storage["path"], storage["max_size"]):
            #     logger.error(json.dumps({
            #         "storage_path": storage["path"],
            #     }), "STORAGE_ADD_FAILED")
            # else:
            #     logger.info(json.dumps({
            #         "storage_path": storage["path"],
            #     }), "STORAGE_ADDED")
            
        else:
            logger.critical(json.dumps({
            "storages": storages,
        }), "INVALID_CONFIG")
            return

    return storage_manager

def storage_worker(logger: Logger, config: Config, stop_event: Event):
    '''
    存储工作线程，负责处理存储相关的任务
    '''
    logger.info("", "LOADING_STORAGES")

    storage_manager = init_storages(config, logger)

    if storage_manager is None:
        logger.debug("StorageManager initialization failed, stopping storage worker", "STORAGE_DEBUG")
        stop_event.set()
        return
    
    logger.debug("StorageManager initialized", "STORAGE_DEBUG")
    
    while not stop_event.is_set():
        pass

        
    
    

        
