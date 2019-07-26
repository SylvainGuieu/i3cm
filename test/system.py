from i3cm.core import System, config_path

config_path.append('/Users/guieus/python/i3cm/config/')

if __name__ == "__main__":
    I3CM = System.from_config('i3cm.yaml')
    I3CM.MOTORS
    
    I3CM.MOTORS.MOTOR1.OFFSET.set('1.2')
    
    assert I3CM.MOTORS.MOTOR1.OFFSET.get() == 1.2
    
    assert I3CM.MOTORS.MOTOR1.OFFSET.mode == "user"
    
    print(list(I3CM.systems.keys()))
        
    print(I3CM.MOTORS.MOTOR1.description)
    
    print(list(I3CM.MOTORS.commands))
    
    assert I3CM.MOTORS.MOVE_TO.POS.parse('4.5') == 4.5 
    assert I3CM.MOTORS.MOVE_TO.parse_args( {'POS':'5.6', 'ID':'MOTOR1'}) == {'POS':5.6, 'ID':'MOTOR1'}
    
    I3CM.MOTORS.STATE.set('ONLINE')
    I3CM.MOTORS.MOVE_TO.check_requirements(I3CM.MOTORS)
    I3CM.MOTORS.STATE.get()
    
    print(list(I3CM.MOTORS.commands['SET_ONLINE'].replies))
    