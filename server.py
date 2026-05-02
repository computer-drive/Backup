
from libs.logger import LoggerManager
from libs.protocol import Protocol
import threading
import socket
import json
from libs.server.handler import handle_client
from libs.server.console import command_input
from libs.thread import ThreadManager

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

thread_manager = ThreadManager()

logger_manager = LoggerManager("log.db", thread_manager)
logger = logger_manager.get_logger("server")

def main():
    # 设置停止事件
    stoppend_event = threading.Event()
        
    try:
        server.bind(("127.0.0.1", 8080))
        server.listen(1)
        server.settimeout(5)

        logger.info(json.dumps({"ip": "127.0.0.1", "port":"8080"}), "STARTED", "SERVER")


        # 启动命令线程
        cmd_logger = logger_manager.get_logger("CONSOLE")
        cmd_thread = thread_manager.create_thread(name="CONSOLE", target=command_input, args=(stoppend_event, cmd_logger))
        cmd_thread.start()

        while not stoppend_event.is_set():
            try:
                # 接受客户端连接
                conn, addr = server.accept()
                logger.info(json.dumps({"address": addr}), "CLIENT_CONNECTED", "SERVER")
                
                # 启动处理线程
                thread = thread_manager.create_thread(name="CLIENT", target=handle_client, args=(conn,), kinds="socket")
                thread.start()

            except KeyboardInterrupt:
                conn.close()
                break

            except socket.timeout:
                continue

    except Exception as e:
        logger.error(str(e), "SERVER")
            
    finally:
        # 关闭服务器连接
        logger.info("", "STOPPING_SERVER", "SERVER")
        server.close()

        # 等待所有线程结束
        logger.info("", "STOPPING_SOCKET_THREADS", "SERVER")
        thread_manager.join_threads("socket")

        # 记录服务器停止日志
        logger.info("", "STOPPED", "SERVER")

        # 关闭日志（关闭日志数据库连接）
        logger_manager.close()

    

if __name__ == "__main__":
    main()











