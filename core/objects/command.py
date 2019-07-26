from .. import keys as K 
from .base import (add_type_class, _ArgsProperty,_KeywordsProperty, 
                   _RepliesProperty, _DbBaseObject, _BaseParameter, 
                   _arg_parsers, parse_arg, get_parser
                   )
from ..database.base import str_path

from . import parser
del parser

class Arg(_BaseParameter):            
    def __init__(self, db, prefix):
        prefix = str_path(prefix)
        
        try:
            tpe = db.query( (prefix, K.TYPE) )
        except KeyError:
            raise ValueError('the sub-database at %r does not have type property'%prefix)
        
        if tpe != K.ARG:
            raise ValueError('(sub)db is not an argument at %r'%prefix)
        
        _BaseParameter.__init__(self, db, prefix)
    
    def is_required(self):
        try:
            self._db.query( (self._prefix, 'default') )
        except KeyError:
            return True
        else:
            return False    
    


class Keyword(_BaseParameter):        
    def __init__(self, db, prefix):
        prefix = str_path(prefix)        
        try:
            tpe = db.query( (prefix, K.TYPE) )
        except KeyError:
            raise ValueError('the sub-database at %r does not have type property'%prefix)
        
        if tpe != K.KEYWORD:
            raise ValueError('(sub)db is not a keyword at %r'%prefix)
        _BaseParameter.__init__(self, db, prefix)
        
    

class Reply(_DbBaseObject):
    _db = None
    _prefix = None
    keywords = _KeywordsProperty()
    def __init__(self, db, prefix):
        prefix = str_path(prefix)
        
        try:
            tpe = db.query( (prefix, K.TYPE) )
        except KeyError:
            raise ValueError('the sub-database at %r does not have type property'%prefix)
        
        if tpe != K.REPLY:
            raise ValueError('(sub)db is not a reply at %r'%prefix)
                
        self.__dict__['_db'] = db        
        self.__dict__['_prefix'] = prefix 
    
    def send(self, er, **kwargs):                
        for kname, kdef in self.keywords.items():
            if kname in kwargs:
                kwargs[kname] = kdef.parse(kwargs[kname])
        kwargs.setdefault(K.STATUS, self.status)
        kwargs.setdefault(K.RTYPE, self.rtype)
        
            

class Command(_DbBaseObject):
    _db = None
    _prefix = None
    args = _ArgsProperty()
    replies = _RepliesProperty()
    
    def __init__(self, db, prefix):
        prefix = str_path(prefix)
        
        try:
            tpe = db.query( (prefix, K.TYPE) )
        except KeyError:
            raise ValueError('the sub-database at %r does not have type property'%prefix)
        
        if tpe != K.COMMAND:
            raise ValueError('(sub)db is not a command at %r'%prefix)
            
        self.__dict__['_db'] = db        
        self.__dict__['_prefix'] = prefix 
    
    def process(self, obj, args):
        self.check_requirements(obj)
        self.parse_args(args)
    
    def parse_args(self, args):
        args = dict(args) # make a copy        
        parsed = {}
        for argname, arg in self.args.items():
            if argname not in args:
                if arg.is_required():
                    raise ValueError('for command %r, argument %r is mendatory but missing'%(self._prefix, argname))
                else:
                    parsed[argname] = arg.default
            else:        
                parsed[argname] = arg.parse(args[argname])
                del args[argname]
        
        if args:
            raise ValueError('unknown arguments "%s"'%'", "'.join(args))
        return parsed    
    
    def check_requirements(self, obj):        
        for pname, target_val in self._db.query( (self._prefix, K.REQUIREMENTS) ).items():
            try:
                param = obj[pname]
            except KeyError:
                raise ValueError('BUG: command %r need parameter %r '%(self._prefix, pname))
            val = param.get()
            
            if val!=target_val:
                raise ValueError('command %r require that %r of %r is %r however it is %r'%(self._prefix, pname, obj._prefix, target_val, val))                
    
    @property
    def description(self):
        try:
            return self._db.query( (self._prefix, K.DESCRIPTION) )
        except KeyError:
            return ''
    
    @property
    def requirements(self):
        try:
            return self._db.query( (self._prefix, K.REQUIREMENTS) )
        except KeyError:
            return {}

arg = Arg    
command = Command
reply = Reply
keyword = Keyword
add_type_class(K.ARG, arg)
add_type_class(K.COMMAND, command)
add_type_class(K.REPLY, reply)
add_type_class(K.KEYWORD, command)


    
    
    
            
        

