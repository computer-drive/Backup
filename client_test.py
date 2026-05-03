from libs.client.logger import get_logger
from libs.config import Config
import datetime
from PyQt5.QtWidgets import QApplication

log_file = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".log"
logger = get_logger("client", log_file=log_file)

config = Config("client_config.json", False)


if __name__ == "__main__":
    app = QApplication([])


    app.exec_()







            
    


