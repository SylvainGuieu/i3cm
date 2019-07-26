from i3cm.database import config_parser as cp
from i3cm.database.db import DataBase
import yaml


config_path = []

if __name__ == "__main__":
    import yaml 
    d = yaml.load(open(cp.config_path('i3cm.yaml')).read())
    db = {}
    cp.read(d, db)    
    
    for k, v in db.items():
        print("%-50s"%k, v) 
    
    db = DataBase.from_config('i3cm.yaml')
    assert db.query('MOTORS.MOTOR1.ID.value') == 1
    