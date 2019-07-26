from .. import keys as K
from .base import (add_type_class, _DbBaseObject, _ParametersProperty, 
                   _DevicesProperty, _SystemsProperty, _CommandsProperty)
from ..database.base import str_path
from .publisher import publish

class System(_DbBaseObject):     
    parameters = _ParametersProperty()
    devices = _DevicesProperty()
    systems = _SystemsProperty()
    commands = _CommandsProperty()
        
    def __init__(self, db, prefix):   
        prefix = str_path(prefix)       
        try:
            tpe = db.query( (prefix, K.TYPE) )
        except KeyError:
            raise ValueError('the sub-database at %r does not have type property'%prefix)
              
        if tpe != K.SYSTEM:
            raise ValueError('(sub)db is not a device but a %s at %r'%prefix)
        self.__dict__['_db'] = db
        self.__dict__['_prefix'] = prefix    
                
    def __str_ascii__(self, p):
                        
        tab = " "*len(self._prefix)                
        txt = [p.write_margin(self._prefix)]
                        
        pp = p.child(tab_str=tab, level=1)
        for sysname, system in self.systems.items():            
            txt.append(publish(system, pp))
                    
        for devname, device in self.devices.items():
            txt.append(publish(device, pp)) 
        
        for pname, param in self.parameters.items():
            txt.append(publish(param, pp)) 
        
        return "\n".join(txt)            
    
system = System
add_type_class(K.SYSTEM, system)


