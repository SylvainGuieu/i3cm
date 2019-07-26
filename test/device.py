from i3cm.database.db import DataBase
from i3cm.objects.parameter import Parameter

from i3cm.objects.device import Device

if __name__ == "__main__":
    db_m = DataBase.from_config('motors.yaml')
    MOTOR1 = Device(db_m, 'MOTOR1')
        
    MOTOR1.OFFSET.set('1.2')
    assert MOTOR1.OFFSET.get() == 1.2
    
    
    
