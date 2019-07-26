from .. import keys as K
from ..database.db import DataBase
from ..database.base import str_path
from .publisher import ASCII

type2class_loockup = {}
def type2class(tpe):
    try:
        cl = type2class_loockup[tpe]
    except KeyError:
        raise ValueError("Bug unknown type %s"%tpe)
    return cl

def add_type_class(tpe, cl):
    type2class_loockup[tpe] = cl

parser_loockup = {}
def add_parser(name, f):
    parser_loockup[name] = f

def get_parser(name):
    return parser_loockup[name]

def read_obj(db, prefix):
    prefix = str_path(prefix)
    try:
        tpe = db.query((prefix, K.TYPE))
    except KeyError:
        try:
            aval = db.query( prefix )
        except KeyError:
            raise KeyError(prefix)
        else:
            return aval
    else:        
        obj = type2class(tpe)(db, prefix)
        return obj 


def _arg_parsers(db, prefix):
    prefix = str_path(prefix)
    
    try:
        ptype = db.query( (prefix,'ptype') )
    except KeyError:
        ptype = 'str'
    if isinstance(ptype, str):
        ptype = [ptype]   
     
    return tuple(get_parser(p)(db, prefix) for p in ptype)

def _parse_data(parsers, data):
    for p in parsers:
        data = p(data)
    return data

def parse_arg(db, prefix, data):    
    return _parse_data(_arg_parsers(db, prefix), data)


class _BaseParameter:
    _parsers = tuple()
    _db = None
    _prefix = None
        
    def __init__(self, db, prefix):
        prefix = str_path(prefix)                
        self.__dict__['_db'] = db        
        self.__dict__['_parsers'] = _arg_parsers(db, prefix)        
        self.__dict__['_prefix'] = prefix 
    def __getattr__(self, attr):
                
        pf = self.__dict__['_prefix']
        
        try:
            return self.__dict__['_db'].query( (pf, attr) )
        except KeyError:
            raise AttributeError('%s is not a valid attribute (not in database) at %r'%(attr, pf))
    
    def __setattr__(self, attr, value):                
        raise AttributeError('%s attribute does not exists or read only at %r'%(attr, self.__dict__['_prefix']))        
    
    def parse(self, value):
        return _parse_data(self._parsers, value)
    
        
class _DbBaseObject(object):
    @classmethod
    def from_config(cl, file):
        db = DataBase.from_config(file)
        return cl(db, '')
    
    def update(self, __d__={}, **kwargs):
        db = self.__dict__['_db']
        pf = self.__dict__['_prefix']
        
        d = dict(__d__, **kwargs)
        for key in d:
            try:
                tpe = db.query( (pf, key, K.TYPE) )
            except:
                raise KeyError('""%s" does not point to valide subsatabase at %r'%(key, pf))
            if tpe != K.PARAMETER:
                raise ValueError("cannot update %r, this is not a parameter but a %s at %r"%(key, tpe, pf))        
    
    def __getitem__(self, item):
        item = str_path(item)                
        
        db = self.__dict__['_db']
        pf = self.__dict__['_prefix']
        try:
            db.query( (pf, item, K.TYPE) )
        except:
            raise KeyError('""%s" does not point to valide subsatabase at %r'%(item, pf))
        return read_obj(db, (pf,item))        
        
    def __setitem__(self, item):
        raise KeyError("Cannot set an parameter directly (too ambigous) use update method or o[K].set(val)")
        
    def __getattr__(self, attr):
        try:
            val = super().__getattribute__(attr)
        except AttributeError:
            return read_obj(self.__dict__['_db'], (self._prefix, attr))            
        else:              
            return val
    
    def __setattr__(self, attr, value):
        try:
            super().__getattr__(attr)
        except AttributeError:            
            raise AttributeError('%r attribute does not exists or readonly at %r'(attr, self._prefix))            
        else:                        
            super().__setattr__(attr, value)          
        
    def __str__(self):
        return self.__str_ascii__(ASCII(0))
    
    def __str_ascii__(self, p):
        return str(self._db)
    

class _ParametersProperty:
    def __get__(self, master, cls=None):
        if master is None: 
            return self
        return _Parameters(master._db, master._prefix)
                
class _Parameters:
    def __init__(self, db, prefix):
        self._db = db
        self._prefix = prefix
    
    def __iter__(self):
        for pname in self._db.query( (self._prefix, K.PARAMETERS) ):
            yield pname
    
    def __getitem__(self, item):
        if item not in self._db.query( (self._prefix, K.PARAMETERS) ):
            raise KeyError(item)
        return type2class(K.PARAMETER)(self._db, (self._prefix, item))

    def __setitem__(self, item, val):
        raise TypeError('items are read only')
    
    def keys(self):
        for pname in self._db.query( (self._prefix, K.PARAMETERS) ):
            yield pname
    
    def items(self):
        for pname in self.keys():
            yield pname, type2class(K.PARAMETER)(self._db, (self._prefix, pname))
        
    def values(self): 
        for pname in self.keys():
            yield type2class(K.PARAMETER)(self._db, (self._prefix, pname))    

class _DevicesProperty:
    def __get__(self, master, cls=None):
        if master is None: 
            return self
        return _Devices(master._db, master._prefix)
                
class _Devices:
    
    def __init__(self, db, prefix):
        self._db = db
        self._prefix = prefix    
    
    def __iter__(self):
        for pname in self._db.query( (self._prefix, K.DEVICES) ):
            yield pname
    
    def __getitem__(self, item):
        if item not in self._db.query( (self._prefix, K.DEVICES) ):
            raise KeyError(item)
        return type2class(K.DEVICE)(self._db, (self._prefix, item))

    def __setitem__(self, item, val):
        raise TypeError('items are read only')
    
    def keys(self):
        for pname in self._db.query( (self._prefix, K.DEVICES) ):
            yield pname
    
    def items(self):
        for pname in self.keys():
            yield pname, type2class(K.DEVICE)(self._db, (self._prefix, pname))
        
    def values(self): 
        for pname in self.keys():
            yield type2class(K.DEVICE)(self._db, (self._prefix, pname))
        


class _SystemsProperty:
    def __get__(self, master, cls=None):
        if master is None: 
            return self
        return _Systems(master._db, master._prefix)
                

                
class _Systems:
    
    def __init__(self, db, prefix):
        self._db = db
        self._prefix = prefix
    
    def __iter__(self):
        for pname in self._db.query( (self._prefix, K.SUBSYSTEMS) ):
            yield pname
    
    def __getitem__(self, item):
        if item not in self._db.query( (self._prefix, K.SUBSYSTEMS) ):
            raise KeyError(item)
        return type2class(K.SYSTEM)(self._db, (self._prefix, item))
        
    def __setitem__(self, item, val):
        raise TypeError('items are read only')
    
    
    def keys(self):
        for pname in self._db.query( (self._prefix, K.SUBSYSTEMS) ):
            yield pname
            
    def items(self):
        for pname in self.keys():
            yield pname, type2class(K.SYSTEM)(self._db, (self._prefix, pname))
        
    def values(self): 
        for pname in self.keys():
            yield type2class(K.SYSTEM)(self._db, (self._prefix, pname))
    
class _ArgsProperty:
    def __get__(self, master, cls=None):
        if master is None: 
            return self
        return _Args(master._db, master._prefix)

class _Args:
    
    def __init__(self, db, prefix):
        self._db = db
        self._prefix = prefix
    
    def __iter__(self):
        for pname in self._db.query( (self._prefix, K.ARGS) ):
            yield pname
    
    def __getitem__(self, item):
        if item not in self._db.query( (self._prefix, K.ARGS) ):
            raise KeyError(item)
        return type2class(K.ARG)(self._db, (self._prefix, item))

    def __setitem__(self, item, val):
        raise TypeError('items are read only')
    
    
    def keys(self):
        for pname in self._db.query( (self._prefix, K.ARGS) ):
            yield pname
            
    def items(self):
        for pname in self.keys():
            yield pname, type2class(K.ARG)(self._db, (self._prefix, pname))
        
    def values(self): 
        for pname in self.keys():
            yield type2class(K.ARG)(self._db, (self._prefix, pname))




class _RepliesProperty:
    def __get__(self, master, cls=None):
        if master is None: 
            return self
        return _Replies(master._db, master._prefix)

class _Replies:
    
    def __init__(self, db, prefix):
        self._db = db
        self._prefix = prefix
    
    def __iter__(self):
        for pname in self._db.query( (self._prefix, K.REPLIES) ):
            yield pname
    
    def __getitem__(self, item):
        if item not in self._db.query( (self._prefix, K.REPLIES) ):
            raise KeyError(item)
        return type2class(K.REPLY)(self._db, (self._prefix, item))
    
    def __setitem__(self, item, val):
        raise TypeError('items are read only')
    
    
    def keys(self):
        for pname in self._db.query( (self._prefix, K.REPLIES) ):
            yield pname
            
    def items(self):
        for pname in self.keys():
            yield pname, type2class(K.REPLY)(self._db, (self._prefix, pname))
        
    def values(self): 
        for pname in self.keys():
            yield type2class(K.REPLY)(self._db, (self._prefix, pname))

class _KeywordsProperty:
    def __get__(self, master, cls=None):
        if master is None: 
            return self
        return _Keywords(master._db, master._prefix)

class _Keywords:    
    def __init__(self, db, prefix):
        self._db = db
        self._prefix = prefix
    
    def __iter__(self):
        for pname in self._db.query( (self._prefix, K.KEYWORDS) ):
            yield pname
    
    def __getitem__(self, item):
        if item not in self._db.query( (self._prefix, K.KEYWORDS) ):
            raise KeyError(item)
        return type2class(K.KEYWORD)(self._db, (self._prefix, item))
    
    def __setitem__(self, item, val):
        raise TypeError('items are read only')
    
    
    def keys(self):
        for pname in self._db.query( (self._prefix, K.KEYWORDS) ):
            yield pname
            
    def items(self):
        for pname in self.keys():
            yield pname, type2class(K.KEYWORD)(self._db, (self._prefix, pname))
        
    def values(self): 
        for pname in self.keys():
            yield type2class(K.KEYWORD)(self._db, (self._prefix, pname))


class _CommandsProperty:
    def __get__(self, master, cls=None):
        if master is None: 
            return self
        return _Commands(master._db, master._prefix)
            
                                
class _Commands:    
    def __init__(self, db, prefix):
        self._db = db
        self._prefix = prefix
    
    def __iter__(self):
        for pname in self._db.query( (self._prefix, K.COMMANDS) ):
            yield pname
    
    def __getitem__(self, item):
        if item not in self._db.query( (self._prefix, K.COMMANDS) ):
            raise KeyError(item)
        return type2class(K.COMMAND)(self._db, (self._prefix, item))

    def __setitem__(self, item, val):
        raise TypeError('items are read only')
    
            
    def keys(self):
        for pname in self._db.query( (self._prefix, K.COMMANDS) ):
            yield pname
            
    def items(self):
        for pname in self.keys():
            yield pname, type2class(K.COMMAND)(self._db, (self._prefix, pname))
        
    def values(self): 
        for pname in self.keys():
            yield type2class(K.COMMAND)(self._db, (self._prefix, pname))
