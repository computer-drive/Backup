LOG_FORMAT = "%(color)s[%(asctime)s/%(class_name)s][%(levelname)s](%(log_type)s) %(message)s%(reset)s"

LOG_DATABASE_NEW_SQL = '''
CREATE TABLE IF NOT EXISTS {table_name} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    level INTEGER NOT NULL,                            
    class_name TEXT NOT NULL,
    type TEXT NOT NULL,
    message_type TEXT NOT NULL,
    message TEXT NOT NULL       
    )                     
'''