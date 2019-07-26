from i3cm.objects import parameter as pr
from i3cm.database.db import DataBase
import yaml

if __name__ == "__main__":
    _db = {
        'P1.type': 'parameter',
        'P1.value': 6.7, 
        'P1.ptype': ['float', 'int', 'listed'], 
        'P1.list' : [6,7,8], 
        'P2.type' : 'parameter',
        'P2.value' : 5.0,
        'P2.ptype' : ['float', 'bounded'],
        'P2.min' : 0,
        'P2.max' : 10,
        'parameters': ['P1', 'P2']
    }
    
    p = pr.Parameter(DataBase(_db), 'P1')
    p.set(7)
    assert p.get()==7
        
    ps = pr.Parameters(DataBase(_db), '')
    assert ps['P1'].get() == 7
    ps['P1'].set(6.3)
    assert ps['P1'].get() == 6
        
    ps['P2'].set(6.3)
    assert ps['P2'].min == 0
    assert ps['P2'].max == 10
    
    