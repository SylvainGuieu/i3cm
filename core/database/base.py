import os
from .. import keys as K
PRIVATE_KEYS = (K.TYPE, K.PROTOTYPES, K.DESCRIPTION, 
                K.FILE, K.PROTOTYPE, K.SETUP)


config_path = ["."]

def find_config(name):
    for root in config_path:
        path = os.path.join(root, name)
        if os.path.exists(path):
            return path    
    raise ValueError("cannot found file %r in any of path directories : '%s'"%(name, "', '".join(config_path)))    


def str_path(obj):
    if isinstance(obj, str):
        return obj
    return ".".join( a for a in obj if a)
        
    #return (".".join( sum( (a.split(".") for a in obj), []))).strip('.')

def split_path(path):
    path = str_path(path)
    return path.split(".")

def db_join(*args):
    return (".".join( sum( (a.split(".") for a in args), []))).strip('.')

def dbquery(db, *args):
    return db.query(db_join(*args))
    

    
