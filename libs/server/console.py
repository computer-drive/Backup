from ..command import CommandManager
import threading
from ..logger import Logger
from ..thread import ThreadManager
import socket

def command_input(stoppend_event: threading.Event, logger: Logger, thread_manager: ThreadManager, server: socket.socket, stop_event: threading.Event):
    

    while not stoppend_event.is_set():
        try:
            cmd = input(">> ")
        except EOFError:
            stoppend_event.set()
            break

        if not cmd or cmd.isspace():
            continue

        cmd = cmd.strip().split()

        if cmd[0] == "stop":
            stoppend_event.set()
            
            server.close()
            print("Stopping...")
            break

        elif cmd[0] == "thread":
            print(thread_manager.get_all_threads())
        
            

                
                


