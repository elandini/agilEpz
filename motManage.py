from libs.epz.epz import CMD,CMDREC,Environment
from configparser import ConfigParser as cp
from libs.pyagilis.controller import AGUC8

class MOT(CMDREC):
    
    def __init__(self,cfgName,environment):
        
        super(MOT,self).__init__(environment)
        
        cfg = cp()
        cfg.read(cfgName)
        
        self.notifier = CMD(environment)
        self.notifier.command = 'NTF'
        
        self.controller = AGUC8(cfg.get('PORT','com'),[cfg.get('CONTROLLER','channel')],
                                cfg.get('CONTROLLER','x'),cfg.get('CONTROLLER','y'),cfg.get('CONTROLLER','ampx'),cfg.get('CONTROLLER','ampy'))
        
        self.respDict = {'M':self.controller.move,
                         'S':self.controller.stop,
                         'SZ':self.controller.setZero,
                         'GZ':self.controller.goToZero,
                         'UU':self.controller.moveUpUp,
                         'UD':self.controller.moveUpDown,
                         'DU':self.controller.moveDownUp,
                         'DD':self.controller.moveDownDown,}
        
        
    def react(self,resp):
        
        # Command synthax 'whatToDo:value1:value2'
        
        pieces = resp.split(':')
        args = resp[1:]
        self.respDict[pieces[0]](*args)
        
        self.notifier.send('OK')
        

ENV = Environment('libs\epz\epz.conf')
MOTCONF = 'libs\pyagilis\config.mot'


if __name__ == '__main__':
    
    mot = MOT(MOTCONF,ENV)
    mot.tag = 'MOT'
    mot.daemon = False
    
    mot.start()
    
        