import time
from .thread import Thread

simulator = None

simulator_dict = {}

def start_simulator():
    global simulator
    simulator = Simulator()
    simulator._livesignal = True
    simulator.start()

def stop_simulator():
    global simulator
    simulator.kill()
    simulator = None

def add_simulator_callback(t, callback):
    global simulator
    if simulator is None or not simulator._livesignal:
        raise ValueError('simulator is not running')
    simulator.callbacks[t] = callback
    
class Simulator(Thread):
    _livesignal = True
    callbacks = None
    
    def __init__(self, delay=0.1):
        self.callbacks = {}
        self.delay = delay
        Thread.__init__(self)
    
    def kill(self):
        self._livesignal = False
    
    def run(self):
        self.callbacks = {}
        callbacks = self.callbacks
        delay = self.delay 
        while self._livesignal:
            t_start = time.time()
            for t, callback in list(callbacks.items()):
                if t<t_start:
                    callback()
                    callbacks.pop(t)
            time.sleep(delay)