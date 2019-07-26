from .. import keys as K 
from .base import add_type_class, _BaseParameter, get_parser
from ..database.base import str_path

from . import parser
del parser

from .publisher import publish, ASCII



def _parameter_parsers(db, prefix):
    prefix = str_path(prefix)
    try:
        ptype = db.query( (prefix,K.PTYPE))
    except KeyError:
        ptype = 'str'
    if isinstance(ptype, str):
        ptype = [ptype]   
     
    return tuple(get_parser(p)(db, prefix) for p in ptype)

def _parse_data(parsers, data):
    for p in parsers:
        data = p(data)
    return data

def parse_parameter(db, prefix, data):    
    return _parse_data(_parameter_parsers(db, prefix), data)

class Parameter(_BaseParameter):    
    def __init__(self, db, prefix):
        prefix = str_path(prefix)
        if db.query( (prefix, K.TYPE) ) != K.PARAMETER:
            raise ValueError('%r is not a parameter'%prefix)
        _BaseParameter.__init__(self, db, prefix)         
        try:
            v = self.get()        
        except KeyError:
            pass
        else:
            if v is not None:
                db.set( (prefix,K.VALUE) , self.parse(v))
        
    def get(self):
        return self._db.query( (self._prefix,K.VALUE) )
    
    def set(self, value):
        self._db.set( (self._prefix, K.VALUE), self.parse(value) )
        
    def seq(self, value):
        return [self._prefix, self.parse(value)]       
    
    def __str__(self):
        return self.__str_ascii__(ASCII(0))
        
    def __str_ascii__(self, p):                        
        #tab = " "*len(self._prefix)
        try:
            sval = str(self.get())
        except:
            sval = "ERROR"
                            
        txt = [p.write_margin("%-40s: %s"%(self._prefix,sval))]                                
        
        return "\n".join(txt) 
        
class _BaseParameters:
    def keys(self):
        for k in self._db.query( (self._prefix, K.PARAMETERS) ):
            yield k 
    
    def items(self):
        for k in self.keys():
            yield k, self[k]
    
    def values(self):
        for k in self.keys():
            yield self[k]

class Parameters(_BaseParameters):
    _db = None
    _prefix = None
    def __init__(self, db, prefix):        
        try:
            db.query( (prefix, K.PARAMETERS) )
        except KeyError:
            raise ValueError('(sub)db must must have a "parameters" property at %r'%prefix)    
        self._db = db        
        self._prefix = prefix 
    
    def __getitem__(self, item):   
        # TODO: Check if cash of Parameters are needed 
        prs = self._db.query( (self._prefix, K.PARAMETERS) )            
        if item not in prs:
            raise KeyError(item)
        return parameter(self._db, (self._prefix, item) )

    
# for now parameter is Parameter class
# maybe in the future it will become a function that return a cashed object
# for performance purpose 
parameter = Parameter  
parameters = Parameters

add_type_class(K.PARAMETER, parameter)

