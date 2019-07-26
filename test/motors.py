from i3cm.core import System, config_path
from i3cm.core.process import start_simulator, stop_simulator, simulator_dict

from i3cm.process.motors import motors_process

from i3cm.process import motors_function as mf
import time

config_path.append('/Users/guieus/python/i3cm/config')
if __name__ == "__main__":
    start_simulator()
    I3CM = System.from_config('i3cm.yaml')
    
    motors_process(I3CM.MOTORS, "SET_ONLINE", {})
    
    print(motors_process(I3CM.MOTORS, "MOVE_TO", {"ID":"MOTOR1", "POS":45.6}))
    time.sleep(1.5)
    print(I3CM.MOTORS.MOTOR1.SUBSTATE)
    print(I3CM.MOTORS.MOTOR1.CURRENT)
    motors_process(I3CM.MOTORS, "WAIT", {}, timeout=10)
    
    motors_process(I3CM.MOTORS, "SET_OFFLINE", {})
    stop_simulator()
    
    