import json

default_server_config = {
    "server.address": "0.0.0.0",
    "server.port": 8080,
    "log.database": "log.db"
}

default_client_config = {

}

class Config:
    def __init__(self, config_file: str = "config.json", is_server: bool = True):
        self.config_file = config_file
        self.config = self.load()
        self.is_server = is_server
    
    def load(self):
        with open(self.config_file, "r") as f:
            config = json.load(f)

        return config
    def save_config(self):
        with open(self.config_file, "w") as f:
            json.dump(self.config, f, indent=4)

    def get(self, key: str):
        if self.is_server:
            return self.config.get(key, default_server_config.get(key))
        return self.config.get(key, default_client_config.get(key))
    
    def set(self, key, value):
        self.config[key] = value
    
    def save(self):
        with open(self.config_file, "w") as f:
            json.dump(self.config, f, indent=4)

    def reload(self):
        self.config = self.load()

    


