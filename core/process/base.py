import time
class ERROR:
    UNKNOWNCMD = "E_UNKNOWNCMD"
    ARGS  = "E_ARGS"
    STATE = "E_STATE"
    SUBSTATE = "E_SUBSTATE"
    BADID = "E_ID"
    REQUIREMENT = "E_REQUIREMENT"
    TIMEOUT = "E_TIMEOUT"
    RUNTIME = "E_RUNTIME"
    PARAMETER = "E_PARAMETER"

def send_error(er,cmd,  msg):
    return {
        'status' : 4, 
        'cmd':cmd, 
        'rtype': er, 
        'message': msg
    }
        
def send(cmd, val, **kwargs):        
    kwargs['cmd'] = cmd
    kwargs['status'] = 0
    kwargs['return'] = val
    kwargs['time']= time.time()    
    return kwargs