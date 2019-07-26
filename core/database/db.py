from . import config_parser as cp
from .base import str_path

class EMPTY:
    pass

class DataBase:
    def __init__(self, d):
        self._d = d
    
    def query(self, key):        
        return self._d[str_path(key)]
    
    def queries(self, key_list):
        """ return a key/value pair inside a dictionary from a list of keys"""
        return {key:self._d[str_path(key)] for key in key_list}
    
    def selfupdate(self, key_list):
        """ selfupdate is used only if the data base is a mirror of a remote database 
        
        The keys in the given key_list will be updated 
        """
        pass 
    
    def set(self, key, value):
        self._d[str_path(key)] = value 
    
    def update(self, __d__={}, **kwargs):
        self._d.update(__d__, **kwargs)
            
    def __str__(self):
        # TODO: str of DataBase object        
        return "\n".join( "%-50s: %s"%(key, item) for key, item in self._d.items())
    
    @classmethod
    def from_config(cl, d):
        _db = {}
        cp.read(d, _db)
        return cl(_db)
    