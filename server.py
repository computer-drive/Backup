
from libs.logger import LoggerManager
from libs.protocol import Protocol
import threading
import socket
import json
from libs.server.handler import handle_client
from libs.server.console import command_input
from libs.thread import ThreadManager
from libs.config import Config
from libs.storage import storage_worker

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    thread_manager = ThreadManager()

    config = Config("config.json", True)
    
    logger_manager = LoggerManager(config.get("log.database"), thread_manager)
    logger = logger_manager.get_logger("server")

    # 设置停止事件
    stop_event = threading.Event()

    # 存储层线程
    storage_logger=  logger_manager.get_logger("STORAGE")
    storage_thread = thread_manager.create_thread(name="STORAGE", target=storage_worker, args=(storage_logger, config, stop_event))
    storage_thread.start()
    
    # 命令输入线程
    cmd_logger = logger_manager.get_logger("CONSOLE")
    cmd_thread = thread_manager.create_thread(name="CONSOLE", target=command_input,
                                                   args=(stop_event, cmd_logger, thread_manager, server, stop_event),
                                                daemon=True
                                              )
    cmd_thread.start()
    
    try:
        if stop_event.is_set():
            raise KeyboardInterrupt
        server.bind((
            config.get("server.address"),
            config.get("server.port")
            ))
        
        server.listen(5)
        server.settimeout(10)

        logger.info(json.dumps({"ip": config.get("server.address"), "port": config.get("server.port")}), "STARTED", "SERVER")


        while not stop_event.is_set():
            try:
                # 接受客户端连接
                conn, addr = server.accept()
                logger.info(json.dumps({"address": addr}), "CLIENT_CONNECTED", "SERVER")

                # 创建日志
                handler_logger = logger_manager.get_logger(f"CLIENT_{addr[0]}_{addr[1]}")
                
                # 启动处理线程
                thread = thread_manager.create_thread(name="CLIENT", target=handle_client, args=(conn,handler_logger, stop_event), kinds="socket")
                thread.start()

            except KeyboardInterrupt:
                
                conn.close()
                break

            except socket.timeout:
                continue

            except OSError:
                continue

    except KeyboardInterrupt:
        pass

    except Exception as e:
        logger.error(str(e), "SERVER")
            
    finally:
        try:
            # 关闭服务器连接
            logger.info("", "STOPPING_SERVER", "SERVER")
            server.close()

            # 等待所有线程结束

            logger.info("", "STOPPING_SOCKET_THREADS", "SERVER")
            thread_manager.join_threads("socket")

            # 等待存储层线程结束
            thread_manager.join_thread("STORAGE")
            
            # 等待命令线程结束
            # thread_manager.join_thread("CONSOLE")

            # 记录服务器停止日志
            logger.info("", "STOPPED", "SERVER")

            # 关闭日志（关闭日志数据库连接）
            logger_manager.close()
        except KeyboardInterrupt:
            pass

    

if __name__ == "__main__":
    main()











