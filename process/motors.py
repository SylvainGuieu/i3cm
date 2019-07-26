from ..core.process import ERROR, send_error, send, Thread
import time

from . import motors_function as mf

ERROR_LOOCKUP = {}



motorsThread = None


def motors_process(SYS, cmd, args, timeout=None):
    global motorsThread
    rtime = time.time()
    
    try:
        CMD = SYS.commands[cmd]
    except KeyError:
        return send_error(ERROR.UNKNOWNCMD, '', "command {cmd} not understood".format(cmd=cmd))
    
    try:
        args = CMD.parse_args(args)
    except ValueError as er:
        return send_error(ERROR.ARGS, cmd, "Error when reading arguments : {er}".format(er=er))
    
    timeout = CMD.timeout if timeout is None else timeout 
    
    # check requirements to execute the command usualy the STATE is checked 
    # requirement are defined in the config files
    try:
        CMD.check_requirements(SYS)
    except ValueError as er:
        return send_error(ERROR.REQUIREMENT, cmd, "Error when executing {cmd} : {er}".format(cmd=cmd, er=er))
    
    if cmd == "SET_ONLINE":
        state = SYS['STATE'].get()
        
        if state == "ONLILNE":
            return send_error(ERROR.STATE, cmd, "Trying to get motors process ONLINE while already ONLINE")
        if state == "ERROR":
            return send_error(ERROR.STATE, cmd, "Trying to get motors process ONLINE from ERROR")
        
        try:
            motorsThread = MotorsThread(SYS)            
        except Exception as er:
            return send_error(ERROR.STATE, cmd, "Trying to get motors process OFFLINE : {er}".format(er))
                
        try:
            SYS['STATE'].set('ONLINE')
        except Exception as er:
            return send_error(ERROR.STATE, cmd, "Trying to get motors process OFFLINE : {er}".format(er))
        
        
        for MOTOR in SYS.devices.values():
            MOTOR['STATE'].set('ONLINE')
            MOTOR['SUBSTATE'].set('IDL')
        
        motorsThread.start()
        return send(cmd, SYS['STATE'].get(), rtime=rtime, STATE=SYS['STATE'].get())
        
    if cmd == "SET_OFFLINE":
        if motorsThread:
            motorsThread.kill()
            motorsThread = None
        try:
            SYS['STATE'].set('OFFLINE')
        except Exception as er:
            return send_error(ERROR.STATE, cmd, "Trying to get motors process OFFLINE : {er}".format(er))        
        return send(cmd, SYS['STATE'].get(), rtime=rtime)
    
    
    if cmd == "MOVE_TO":
        try:
            MOTOR = SYS[args['ID']]
        except:
            return send_error(ERROR.BADID, cmd, "Motor with id %s does not exists"%args['ID'])
        
        substate = MOTOR['SUBSTATE'].get()
        if substate != "IDL":
            return send_error(ERROR.SUBSTATE, cmd, "Can move %s while in state %r"%(args['ID'], substate))
        
        MOTOR['SUBSTATE'].set('MOVING')
        try:
            mf.move_to(MOTOR['BIT_ADDRESS'].get(), args['POS'])
        except Exception as er:
            MOTOR['SUBSTATE'].set('ERROR')
            return send_error(ERROR.RUNTIME, cmd, "When trying to move %s : %s"%(args['ID'], er))
        
        return send(cmd, None, rtime=rtime)
        
        
    if cmd == "WAIT":
                
        substates = [MOTOR['SUBSTATE'] for MOTOR in SYS.devices.values()]
        p = args['CYCLE']
        timeout = timeout
        
        while True:
            c = 0
            for substate  in substates: 
                st = substate.get()
                if st == "ERROR":
                    return send_error(ERROR.SUBSTATE, cmd, "%s is in ERROR"%(args['ID']))
                if st == "IDL":
                    c += 1
            
            if c==4:
                return send(cmd, '', rtime=rtime)
            
            if (time.time()-rtime)>timeout:
                return send_error(ERROR.TIMEOUT, cmd, "TIMEOUT (%s s) when waiting for movement to end"%timeout)            
            time.sleep(p)
    

class MotorsThread(Thread):
    def __init__(self, SYS):
        Thread.__init__(self)  
        try:
            self.delay = SYS["LOOP_PERIOD"].get()
        except KeyError:
            self.delay = 1
        
        # some db keys often red
        self.state = SYS['STATE']
        
        self._lock = False
        self._livesignal = True
                        
        self.SYS = SYS
        
        #####################################
        #                            
    
    def run(self):    
        
        SYS = self.SYS
        
        self._livesignal = True
        
        ## collect some static or dynamical info I will use often 
        # at run time 
        C = {}
        for mid, MOTOR in SYS.devices.items():
            C[mid] = {
                'CURRENT': MOTOR['CURRENT'],
                'BIT': MOTOR['BIT_ADDRESS'], 
                'SUBSTATE': MOTOR['SUBSTATE']
            }
                
        ct = self.SYS['CURRENT_TRESHOLD']
        
        while self._livesignal:            
            t_start = time.time()
            
            for mid, M in C.items():
                bit = M['BIT'].get()
                try:
                    current = mf.read_current(bit)
                except Exception as er:
                    print('ERROR: cannot read motor current %s : %s'%(mid, er))
                else:
                    M['CURRENT'].set(current)
                    if current>ct.get():                                                
                        M['SUBSTATE'].set('MOVING')
                    else:
                        M['SUBSTATE'].set('IDL')
                        
            t_stop = time.time()    
            time.sleep(max(self.delay - (t_stop-t_start) , 0) )
            
        
    
    

            
        
    
    