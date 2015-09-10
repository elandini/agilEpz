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

## @package agPort
# This module contains a class that implements custom versions of python built-in serial port class for the agilis controllers 
#

import serial as s
from datetime import datetime

## AGPort class documentation
#
# This class extend the python Serial class with some function that simplifies its use with the agilis controllers commands
class AGPort(s.Serial):
    
    ## Class constructor
    # @param portName The name of the virtual serial port of the chosen controller
    # Creates a Serial object with the values needed by the virtual serail port of the controller 
    def __init__(self,portName = None):
        
        if portName == None:
            ## @var AGPort.soul
            # if the port has not been opened, this value is None
            self.soul = None
            return None
        try:
            super(AGPort,self).__init__(portName,921600,s.EIGHTBITS,s.PARITY_NONE,s.STOPBITS_ONE)
            self.soul = 'p'
        except Exception as e:
            print(e.message)
            self.soul = None
            return None
    
    ## amInull
    # Return False if @var soul is None
    def amInull(self):
        return self.soul is None
    
    ## isAquery
    def isAquery(self,command):
        
        if self.amInull():
            return False
        
        queryOnly=["?","PH","TE","TP","TS","VE"]
        command = command.upper()
        for q in queryOnly:
            if command.find(q) != -1:
                return True
        return False
    
    
    def sendString(self,command):
        
        response = ''
        self.write(command)
        if self.isAquery(command):
            response = self.readline()
        return  response
    
    
 