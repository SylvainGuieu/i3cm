from .. import keys as K
import os
import yaml
from .base import  db_join, PRIVATE_KEYS, find_config

DEFAULT_TIMEOUT = 5*60.


def _load_if_string(d):
    if isinstance(d, str):
        with open(find_config(d)) as f:
            d = yaml.load(f.read())
    return d
    
def _load(d, prototypes):    
    
    d = _load_if_string(d)
    if K.PROTOTYPE in d:
        if not d[K.PROTOTYPE] in prototypes:
            raise ValueError('Unknown prototype %r'%d[K.PROTOTYPE])
        df =  _load(prototypes[d[K.PROTOTYPE]], prototypes)
        for key, value in df.items():
            d.setdefault(key, value)
    
    if K.FILE in d:
        file = d[K.FILE]
        df = _load(file, prototypes)
        if K.TYPE in d and K.TYPE in df and d[K.TYPE]!=df[K.TYPE]:
            raise Exception('including file %r as a %s however this is a %s'%(file, d[K.TYPE], df[K.TYPE]))
        for key, value in df.items():
            d.setdefault(key, value)                    
    return d

def _read_setup(setups, db,  root , suffix):
    """ read everything under setups
    setups shoud be key/value pairs, the key should point to parameter relative 
    to where it starts (root)        
    """
    setup = _load_if_string(setups)
    for k,v in setup.items():
        nk = db_join(root, suffix, k)
        if not  db_join(nk, K.TYPE) in db:
            raise ValueError('error in setup unknown key %s'%nk)
        if db[db_join(nk, K.TYPE)]!= K.PARAMETER:
            raise ValueError('error in setup %r is not a parameter'%nk)        
        db[db_join(nk, K.VALUE)] = v   

def _check_root_type(db, root, new_type, valid_rtypes):
    if not root: 
        return None
    
    rtype = db.get(db_join(root, K.TYPE), '')
    if not rtype:
        print(db)
        raise ValueError("BUG: (sub)database must define a type at %r"%root)
    if rtype not in valid_rtypes:
        raise ValueError('A %r can only be included in %r and not in a %r'%(new_type, valid_rtypes, rtype))


def _add_prototypes(d, prototypes):
    if K.PROTOTYPES in d:        
        for prototype_name, prototype_def in d[K.PROTOTYPES].items():
            prototype_def = _load(prototype_def, prototypes)
            prototypes[prototype_name] = prototype_def
    


def read(d, db, root="", prototypes=None, suffix="", type=None):
    prototypes = {} if prototypes is None else prototypes
    d = _load(d, prototypes)
    type = d.get(K.TYPE, type)
    
    if type is None:            
        raise ValueError("config has no type %s"%d)
    try:
        reader = type_reader_loockup[type] 
    except KeyError:
        raise ValueError("unknown type %r in %r"%(type, db_join(root, suffix)))
    
    reader(d, db, root=root, prototypes=prototypes, suffix=suffix)
    
    
    
def read_system(d, db, root= "", prototypes=None, suffix=""):
    prototypes = {} if prototypes is None else prototypes
    
    _check_root_type(db, root, K.SYSTEM, [K.SYSTEM])
        
    d = _load(d, prototypes)
    path = db_join(root, suffix)
    db[db_join(path, K.TYPE)] = K.SYSTEM
    
    
    _add_prototypes(d, prototypes)
            
    if suffix:
        db.setdefault(db_join(root, K.SUBSYSTEMS), []).append(suffix)
    
    
    for sub_name, sub_def in d.items():
        if sub_name in PRIVATE_KEYS:
            db[db_join(path,sub_name)] = sub_def
        else:
            read(sub_def, db, path, prototypes=prototypes, suffix=sub_name)
            
    setups = d.get(K.SETUP, {})
    _read_setup(setups, db,  root, suffix)
    
    # some required property for the data base a list of subsystem, device, and parameters 
    # This is used only when the system has no subsystem, device or parameter
    db.setdefault(db_join(path, K.SUBSYSTEMS), [])
    db.setdefault(db_join(path, K.DEVICES), [])
    db.setdefault(db_join(path, K.PARAMETERS), [])
    

def read_device(d, db, root="", prototypes=None, suffix=""):    
    prototypes = {} if prototypes is None else prototypes
    
    _check_root_type(db, root, K.DEVICE, [K.SYSTEM])
    
    d = _load(d, prototypes)
    path = db_join(root, suffix)
    db[db_join(path, K.TYPE)] = K.DEVICE
    
    
    _add_prototypes(d, prototypes)
        
    
    if suffix:
        db.setdefault(db_join(root, K.DEVICES), []).append(suffix)
    
    for sub_name, sub_def in d.items():        
        if sub_name in PRIVATE_KEYS:
            db[db_join(path,sub_name)] = sub_def
        else:
            read(sub_def, db, path, prototypes=prototypes, suffix=sub_name)    
    
    setups = d.get(K.SETUP, {})
    _read_setup(setups, db,  root, suffix)
                        
    
    # some required property for the data base a list of  devices, and parameters 
    # This is used only when the system has no  device oa parameter
    db.setdefault(db_join(path, K.DEVICES), [])
    db.setdefault(db_join(path, K.PARAMETERS), [])    
    
    
def read_parameter(d, db, root="", prototypes=None, suffix=""):
    prototypes = {} if prototypes is None else prototypes
    
    _check_root_type(db, root, K.PARAMETER, [K.SYSTEM, K.DEVICE])
    
    d = _load(d, prototypes)
    path = db_join(root, suffix)
    db[db_join(path, K.TYPE)] = K.PARAMETER
    
    if suffix:
        db.setdefault(db_join(root, K.PARAMETERS), []).append(suffix)
                         
    path = db_join(root, suffix)
    db[db_join(path, K.PTYPE)] = d.get(K.PTYPE, 'str')
                
    for k,v in d.items():
        db[db_join(path, k)] = v
    if not db_join(path, K.VALUE) in db:
        db[db_join(path, K.VALUE)] = None
    
def read_command(d, db, root="", prototypes=None, suffix=""):
    prototypes = {} if prototypes is None else prototypes
    
    _check_root_type(db, root, K.COMMAND, [K.SYSTEM])
    
    d = _load(d, prototypes)
    path = db_join(root, suffix)
    db[db_join(path, K.TYPE)] = K.COMMAND
    
    if suffix:
        db.setdefault(db_join(root, K.COMMANDS), []).append(suffix)
                         
    path = db_join(root, suffix)
    
    db[db_join(path, K.DESCRIPTION)]  = d.get(K.DESCRIPTION, '')
    db[db_join(path, K.REQUIREMENTS)] = d.get(K.REQUIREMENTS, {})    
    
    for argname, argdef in d.get(K.ARGS, {}).items():
        read_command_arg(argdef, db, path, prototypes=prototypes, suffix=argname)
    
    for rname, rdef in d.get(K.REPLIES, {}).items():
        read_command_reply(rdef, db, path, prototypes=prototypes, suffix=rname)
    
    db.setdefault(db_join(path, K.ARGS), [])
    db.setdefault(db_join(path, K.DESCRIPTION), '')
    db.setdefault(db_join(path, K.TIMEOUT), DEFAULT_TIMEOUT)
    
    db.setdefault(db_join(path, K.REPLIES), [])

def read_command_arg(d, db, root="", prototypes=None, suffix=""):
    prototypes = {} if prototypes is None else prototypes
    
    _check_root_type(db, root, K.ARG, [K.COMMAND])
    
    d = _load(d, prototypes)
    path = db_join(root, suffix)
    
    db[db_join(path, K.TYPE)] = K.ARG
        
    if suffix:
        db.setdefault(db_join(root, K.ARGS), []).append(suffix)
    
    db[db_join(path, K.PTYPE)] = d.get(K.PTYPE, 'str')
                        
    for k,v in d.items():        
        db[db_join(path, k)] = v    

def read_command_reply(d, db, root="", prototypes=None, suffix=""):
    prototypes = {} if prototypes is None else prototypes
    
    _check_root_type(db, root, K.REPLY, [K.COMMAND])
    
    d = _load(d, prototypes)
    path = db_join(root, suffix)
    
    db[db_join(path, K.TYPE)] = K.REPLY
        
    if suffix:
        db.setdefault(db_join(root, K.REPLIES), []).append(suffix)
    
    keywords = db.get(K.REPLIES, {})
    for kname, kdef in keywords.items():
        read_reply_keyword(kdef, db, path, prototypes=prototypes, suffix=kname)
    
    db.setdefault(db_join(path, K.KEYWORDS), [])
    db.setdefault(db_join(path, K.STATUS), 0)
    db.setdefault(db_join(path, K.DESCRIPTION), '')
    db.setdefault(db_join(path, K.RTYPE), suffix)
    
def read_reply_keyword(d, db, root="", prototypes=None, suffix=""):
    prototypes = {} if prototypes is None else prototypes
    
    _check_root_type(db, root, K.KEYWORD, [K.REPLY])
    
    d = _load(d, prototypes)
    path = db_join(root, suffix)
    
    db[db_join(path, K.TYPE)] = K.KEYWORD
        
    if suffix:
        db.setdefault(db_join(root, K.KEYWORDS), []).append(suffix)
    
    db[db_join(path, K.PTYPE)] = d.get(K.PTYPE, 'str')
                        
    for k,v in d.items():        
        db[db_join(path, k)] = v                           
        
type_reader_loockup = {
    K.SYSTEM: read_system, 
    K.DEVICE: read_device, 
    K.PARAMETER: read_parameter, 
    K.COMMAND: read_command, 
    K.ARG: read_command_arg, 
    K.REPLY: read_command_reply, 
    K.KEYWORD : read_reply_keyword,
}
