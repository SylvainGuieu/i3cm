import threading

class Thread(threading.Thread):
    _livesignal = True
    def __init__(self):
        self._livesignal = True
        threading.Thread.__init__(self)
    
    def kill(self):
        self._livesignal = False
    
    