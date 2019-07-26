from .base import ERROR, send_error, send
from ..database.base import str_path
import time

def parameter_process(SYS, cmd, args):
    rtime = time.time()
    if cmd == "QUERY":
        try:
            key = str_path(args['PARAMETER'])
        except KeyError:
            return send_error(ERROR.ARGS, cmd, "argument PARAMETER is missing")
        
        try:
            obj = SYS[key]
        except (ValueError, TypeError):
            return send_error(ERROR.PARAMETER, cmd, "%s is not a parameter"%key)
        
        if not hasattr(obj, "get"):
            return send_error(ERROR.PARAMETER, cmd, "%s is not a parameter"%key)
        
        try:
            val = obj.get()
        except Exception as er:
            return send_error(ERROR.PARAMETER, cmd, "problem when getting parameter %s: %s"%(key,er))
        
        return send(cmd, {key:val}, rtime=rtime)
    
        
        
        
        
        
        
        
    
    