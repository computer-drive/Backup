from ..command import CommandManager
import threading
from ..logger import Logger
from ..thread import ThreadManager


def command_input(stoppend_event: threading.Event, logger: Logger, thread_manager: ThreadManager):
    

    while True:
        try:
            cmd = input(">> ")
        except EOFError:
            stoppend_event.set()
            break

        if not cmd:
            continue

        cmd = cmd.strip().split()

        if cmd[0] == "stop":
            stoppend_event.set()
            print("Stopping...")
            break

        elif cmd[0] == "thread":
            print(thread_manager.get_all_threads())
        
            

                
                


