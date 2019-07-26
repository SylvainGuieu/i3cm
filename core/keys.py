import yaml
_keys = """
SUFFIX    : suffix
PROTOTYPES: prototypes
PROTOTYPE : prototype
MODEL     : model
TYPE      : type
DEVICE    : device
DEVICES   : devices
SETUP     : setup
PROPERTIES: properties
PROPERTY  : property
PARAMETER : parameter
PARAMETERS: parameters
PTYPE     : ptype
VALUE     : value
SUBSYSTEMS: subsystems
SYSTEM    : system
DTYPE     : dtype
FILE      : file 
DESCRIPTION: description
COMMAND : command
COMMANDS : commands
REQUIREMENTS : requirements
ARGS : args
ARG : arg
REPLIES: replies
REPLY: reply
KEYWORD: keyword
KEYWORDS: keywords
STATUS: status
RTYPE : rtype
TIMEOUT: timeout
"""

__all__ = []
for k,v in yaml.load(_keys).items():
    globals()[k] = v
    __all__.append(k)
    
