from .. import keys as K
from .base import add_type_class, _DbBaseObject, _ParametersProperty
from ..database.base import str_path
from .publisher import publish

class Device(_DbBaseObject):  
    _db = None
    _prefix = None  
    
    parameters = _ParametersProperty()
    
    def __init__(self, db, prefix):
        prefix = str_path(prefix)
        try:
            tpe = db.query( (prefix, K.TYPE) )
        except KeyError:
            raise ValueError('the sub-database at %r does not have type property'%prefix)
        
        if tpe != K.DEVICE:
            raise ValueError('(sub)db is not a device at %r'%prefix)
        self.__dict__['_db'] = db
        self.__dict__['_prefix'] = prefix
    
    def __str_ascii__(self, p):
                        
        tab = " "*len(self._prefix)                
        txt = [p.write_margin(self._prefix)]
                        
        pp = p.child(tab_str=tab, level=1)        
        
        for pname, param in self.parameters.items():
            txt.append(publish(param, pp)) 
        
        return "\n".join(txt) 
            
device = Device 
add_type_class(K.DEVICE, device)

# class Devices:
#     def __init__(self, db):
#         if not db.has(DEVICES):
#             raise ValueError('db has no %s attribute'%DEVICE)
#         self.db = db
# 
#     def __iter__(self):
#         for device in self.db.get(DEVICES):
#             yield Device(db.subdb(device))
# 
#     def __getitem__(self, device):
#         if not device in self.db.get(DEVICES):
#             raise KeyError('cannot find device %s'%device)
# 
#         try:
#             dtype = self.db.get(DTYPE)
#         except KeyError:
#             cl = Device
#         else:
#             cl = get_device_class(dtype)
# 
#         return cl(self.db.subdb(device))
# 
#     def __setitem__(self, key, value):
#         raise KeyError('readonly item')
# 
    