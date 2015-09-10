#
# Copyright (C) 2015-2016 Ettore Landini
#
# This code is translated from another project of mines written in C#
#
# This is a python library for the NewPort Agilis controlle agUC2 and agUC8
#
# You can find another approach to this problem here: http://nullege.com/codes/show/src@t@e@terapy-2.00b6
#
#
#

from time import time,sleep
from datetime import datetime
from libs.epz.epz import CMD
from libs.pyagilis.agPort import *
from configparser import ConfigParser

RATE = 750
LIMSPEED = 3
TIMEOUT = 2000 

class Axis(object):
    
    def __init__(self,name = '1',stepAmp = 50,rate = RATE,parent = None):
        
        if parent == None:
            raise(ValueError('You cannot initialize an Axis without a controller or a channel'))
        self.port = parent.port
        self.name = name
        self.rate = rate
        self.stepAmp = str(stepAmp) if 0<stepAmp<=50 else str(50)
        self.port.sendString(name+'SU+'+self.stepAmp+'\r\n')
        self.port.sendString(name+'SU-'+self.stepAmp+'\r\n')
        
        self.__lastOp__ = 'opened'
    
    
    def whatDidIdo(self):
        
        return self.__lastOp__
    
    
    def stop(self):
        self.port.sendString(self.name+'ST\n')
        self.__lastOp__ = 'stopped'
    
    
    def amIstill(self,rate):
        
        while True:
            if self.amIstillShot():
                return True
            sleep(0.001*rate)
            
            
    def amIstillShot(self):
        
        return self.port.sendString(self.name+'TS\n').find('0') != -1
    
            
    def amIatMyLimit(self):
        
        return self.port.sendString('PH\n').find(self.name) != -1 or self.controller.port.sendString('PH\n').find('3') != -1
        
    
    def queryCounter(self):
        
        return int(self.port.sendString(self.name+'TP\n')[3:])
    
    
    def resetCounter(self):
        
        self.port.sendString(self.name+'ZP\n')
        self.__lastOp__ = 'reset'
        
    
    def jog(self,steps = 0):
        
        if steps == 0:
            return False
        
        self.__lastOp__ = 'jogged: '+str(steps)
        self.port.sendString(self.name+'PR'+str(int(steps))+'\r\n')
    
    
    def goMax(self,speedTag = LIMSPEED):
        
        if self.__lastOp__ == 'goneMin':
            self.jog(500)
            self.amIstill(100)
        elif self.__lastOp__ == 'goneMax':
            return False 
            
        self.__lastOp__ = 'goneMax'
        self.port.sendString(self.name+'MV'+str(speedTag)+'\r\n')
    
    
    def goMin(self,speedTag = LIMSPEED):
        
        if self.__lastOp__ == 'goneMax':
            self.jog(-500)
            self.amIstill(100)
        elif self.__lastOp__ == 'goneMin':
            return False
            
        self.__lastOp__ = 'goneMin'
        self.port.sendString(self.name+'MV'+str(-1*speedTag)+'\r\n')
            
        
    def nowToMilliseconds(self):
        
        t = datetime.now()
        tMilli = t.microsecond/1000+t.second*1000+t.minute*60000+t.hour*3600000
        
        return tMilli
    
    
    def waitMe(self,interval):
        
        timePost = timePre = self.nowToMilliseconds()
        
        while timePost-timePre<interval:
            timePost = self.nowToMilliseconds()