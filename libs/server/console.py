from ..command import CommandManager
import threading
from ..logger import Logger



def command_input(stoppend_event: threading.Event, logger: Logger):
    

    while True:
        cmd = input(">> ")

        match cmd:
            case "stop":
                stoppend_event.set()
                break
            case "":
                continue
            case _:
                print("Unknown command")
            

                
                


