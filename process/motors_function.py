import time
from ..core.process import add_simulator_callback, simulator_dict
import numpy as np

# this is a simulator for the motors function 
# to be replaced by real function 

N=4
simulator_dict['motors_currents'] = {i:0.0 for i in range(N)}

def read_current(bit):
    return simulator_dict['motors_currents'][bit]+np.random.random()/10.
        
def move_to(bit, pos):
    simulator_dict['motors_currents'][bit] = 10
    print("SIMULATOR: moving b%s to position %s"%(bit, pos))
    
    def callback():
        simulator_dict['motors_currents'][bit] = 0.0
        print("SIMULATOR: b%s arrived to position %s"%(bit, pos))          
    # simulate 4 seconds to arrive
    add_simulator_callback(time.time()+4, callback)

