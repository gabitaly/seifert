#!/usr/bin/env python

__author__="gabriele.giambartolomei@desy.de"
__date__ ="June, 2015, 10:56 AM"
__copyright__="Copyright (c) 2010-2015 European XFEL GmbH Hamburg. All rights reserved."

from scpi.scpi_device_2 import *

@KARABO_CLASSINFO("GeSeifertXray", "1.0 1.1 1.2 1.3")
class GeSeifertXray(ScpiDevice2, ScpiOnOffFsm):

    def __init__(self, configuration):
        # always call superclass constructor first!
        super(GeSeifertXray,self).__init__(configuration)
        
        self.commandTerminator = "\n" # The command terminator
        self.socketTimeout = 1.0 # Default timeout value for write/read, can be increased if necessary
    
    ### Register and Define additional slots ###
        
        def registerAdditionalSlots(self, sigslot):
            '''Register additional SLOTS'''
            sigslot.registerSlot(self.setVoltageCurrent)

            sigslot.registerSlot(self.setExposureTimerOn)
        
            sigslot.registerSlot(self.setExposureTimerOff)
                        
        def setVoltageCurrent(self):
            ''' Will set the voltage and current setpoints at once'''
            try:
                self.sendCommand("setVoltageCurrent")
            except:
                raise
            
        def setExposureTimerOn(self):
            ''' Will turn the specified Exposure Timer On'''
            try:
                self.sendCommand("setExposureTimerOn")
            except:
                raise  
            
        def setExposureTimerOff(self):
            ''' Will turn the specified Exposure Timer Off'''
            try:
                self.sendCommand("setExposureTimerOff")
            except:
                raise  
        
        ### Override base class post-processing method pollInstrumentSpecific ###
        def pollInstrumentSpecific(self): 
            '''Perform post-processing od data coming from queries'''
            try:
                '''Current setpoint is returned in uA, convert to mA'''
                currentInmA = self.get("current.setpoint") / 1000
                self.set("current.setpoint",currentInmA)
                currentInmA = self.get("current.actual") / 1000
                self.set("current.actual",currentInmA)
                
                '''Voltage setpoint returned in Volt, convert to kV'''
                voltageInKV = self.get("voltage.setpoint") / 1000
                self.set("voltage.setpoint",voltageInKV)
                voltageInKV = self.get("voltage.actual") / 1000
                self.set("voltage.actual",voltageInKV)     
                
                '''Exposure timer actual value returned in sec., convert to hh,mm,ss'''
                mm, ss = divmod(self.get("exposuretimer.actual"),60)
                hh, mm = divmod(mm, 60)
                self.set("exposuretimerActual.hours",hh)
                self.set("exposuretimerActual.minutes",mm)
                self.set("exposuretimerActual.seconds",ss)
                
                '''Process Status Words'''
                sw1 = self.get("statusWord1")
                sw1Bin = bin(sw1)
                self.set("statusWord1Bin",sw1Bin)
                
                sw2 = self.get("statusWord2")
                sw2Bin = bin(sw2)
                self.set("statusWord2Bin",sw2Bin)
                
                sw3 = self.get("statusWord3")
                sw3Bin = bin(sw3)
                self.set("statusWord3Bin",sw3Bin)
                
                sw4 = self.get("statusWord4")
                sw4Bin = bin(sw4)
                self.set("statusWord4Bin",sw4Bin)
                
                sw6 = self.get("statusWord6")
                sw6Bin = bin(sw6)
                self.set("statusWord6Bin",sw6Bin)
                
                
            except:
                raise
            
            
    
    @staticmethod
    def expectedParameters(expected):
        (
        
        ### Override scpi_device parameters ###
        
        
        # Define alias for the "on" slot
        SLOT_ELEMENT(expected).key("on")
                .tags("scpi")
                .alias("HV:1")
                .displayedName("High voltage ON")
                .description("Equipment start.")
                .allowedStates("Ok.Off")
                .commit(),
        

        # Define alias for the "off" slot
        SLOT_ELEMENT(expected).key("off")
                .tags("scpi")
                .alias("HV:0")
                .displayedName("High voltage OFF")
                .description("Equipment stop.")
                .allowedStates("Ok.On")
                .commit(),
           
                                
        ### Define specific parameters ###
        
        # Define node for Current Setpoint
        NODE_ELEMENT(expected).key("current")
                .displayedName("Current Setpoint")
                .commit(),
        
        INT32_ELEMENT(expected).key("current.setpoint")
                .tags("scpi poll")
                .alias("SC:{current.setpoint};;CN;*{current.setpoint:d};") 
                .displayedName("Current Setpoint [mA]")
                .description("The target value of the current. Command format is xx, adhere typing 05 not 5.")
                .assignmentOptional().defaultValue(0)
                .minInc(0).maxInc(80)
                .unit(Unit.AMPERE)
                .allowedStates("Ok.On")
                .reconfigurable()
                .commit(),
                
        INT32_ELEMENT(expected).key("current.actual")
                .tags("scpi poll")
                .alias(";;CA;*{current.actual:d};")
                .displayedName("Actual Current Setpoint [mA]")
                .description("The actual value of the Current Setpoint.")
                .unit(Unit.AMPERE)
                .readOnly()
                .commit(),            
                                
        # Define node for Voltage Setpoint
        NODE_ELEMENT(expected).key("voltage")
                .displayedName("Voltage Setpoint")
                .commit(),
       
         # NOTE: this value is returned in Volts and has to be converted to kV (Andrea)
        INT32_ELEMENT(expected).key("voltage.setpoint")
                .tags("scpi poll")
                .alias("SV:{voltage.setpoint};;VN;*{voltage.setpoint:d};")
                .displayedName("Voltage Setpoint [kV]")
                .description("The target value of the voltage.Command format is xx, adhere typing 05 not 5.")
                .assignmentOptional().defaultValue(0.0)
                .minInc(0).maxInc(60)
                .unit(Unit.VOLT)
                .allowedStates("Ok.On")
                .reconfigurable()
                .commit(),
                
        INT32_ELEMENT(expected).key("voltage.actual")
                .tags("scpi poll")
                .alias(";;VA;*{voltage.actual:d};")
                .displayedName("Actual Voltage Setpoint [kV]")
                .description("The actual value of the Voltage Setpoint.")
                .unit(Unit.VOLT)
                .readOnly()
                .commit(),                
  
        # Define current and voltage setpoints to be sent in one SLOT command 
        NODE_ELEMENT(expected).key("vc")
                .displayedName("Simultaneous Voltage and Current Setpoints")
                .commit(),
        
        INT32_ELEMENT(expected).key("vc.voltageset")
                .displayedName("Voltage Setpoint [kV]")
                .description("The target value of the Voltage.Command format is xx, adhere typing 05 not 5.")
                .assignmentOptional().defaultValue(0)
                .minInc(0).maxInc(60)
                .unit(Unit.VOLT)
                .allowedStates("Ok.On")
                .reconfigurable()
                .commit(),      
                
        INT32_ELEMENT(expected).key("vc.currentset")
                .displayedName("Current Setpoint [mA]")
                .description("The target value of the Current.Command format is xx, adhere typing 05 not 5.")
                .assignmentOptional().defaultValue(0)
                .minInc(0).maxInc(80)
                .unit(Unit.AMPERE)
                .allowedStates("Ok.On")
                .reconfigurable()
                .commit(),
                
        SLOT_ELEMENT(expected).key("setVoltageCurrent")
                .tags("scpi")
                .alias("SN:{vc.voltageset},{vc.currentset}")
                .displayedName("Set Voltage and Current Setpoints")
                .description("Set target value of Current and Voltage at the same time.")
                .allowedStates("Ok.On")
                .commit(),
        
    
        # Define and configure the Exposure Timers
        
        NODE_ELEMENT(expected).key("exposuretimer")
                .displayedName("Exposure Timer Setpoints")
                .commit(),
                
        INT32_ELEMENT(expected).key("exposuretimer.number")
                .displayedName("Exposure timer setpoint number")
                .description("Number of exposure timer: format integer x")
                .assignmentOptional().defaultValue(1)
                .options("1 2 3 4") 
                .reconfigurable()
                .commit(),
      
        INT32_ELEMENT(expected).key("exposuretimer.hours")
                .displayedName("Exposure timer setpoint hours(HH)")
                .description("Exposure timer setpoint value: hours")
                .unit(Unit.HOUR)
                .assignmentOptional().defaultValue(0)
                .minInc(0).maxInc(99)
                .reconfigurable()
                .commit(),
        
        INT32_ELEMENT(expected).key("exposuretimer.minutes")
                .displayedName("Exposure timer setpoint minutes(MM)")
                .description("Exposure timer setpoint value: minutes")
                .unit(Unit.MINUTE)
                .assignmentOptional().defaultValue(0)
                .minInc(0).maxInc(59)
                .reconfigurable()
                .commit(),     
                
        INT32_ELEMENT(expected).key("exposuretimer.seconds")
                .displayedName("Exposure timer setpoint seconds(SS)")
                .description("Exposure timer setpoint value: seconds")
                .unit(Unit.SECOND)
                .assignmentOptional().defaultValue(0)
                .minInc(0).maxInc(59)
                .reconfigurable()
                .commit(), 
        
        #Set Exposure Timer Setpoints. NOTE: this reply is in seconds, needs conversion to HH,MM,SS (Andrea) 
        INT32_ELEMENT(expected).key("exposuretimer.setpoint")
                .tags("scpi poll")
                .alias("TP:{exposuretimer.number},{exposuretimer.hours},{exposuretimer.minutes},{exposuretimer.seconds};;TN;*{exposuretimer.setpoint:d};") 
                .displayedName("Exposure timer setpoint values")
                .description("Exposure timer setpoint values: seconds")
                .unit(Unit.SECOND)
                .assignmentOptional().defaultValue(0.0)
                .allowedStates("Ok.On")
                .reconfigurable()
                .commit(),
                
        INT32_ELEMENT(expected).key("exposuretimer.actual")
                .tags("scpi poll")
                .alias(";;TA;*{exposuretimer.actual:d};") 
                .displayedName("Exposure Timer actual value")
                .description("Exposure Timer actual value: seconds")
                .unit(Unit.SECOND)
                .readOnly()
                .commit(),        
      
        # Displays the Exposure Timer Actual values        
        NODE_ELEMENT(expected).key("exposuretimerActual")
                .displayedName("Exposure Timer Actual Values")
                .commit(),                        
      
        INT32_ELEMENT(expected).key("exposuretimerActual.hours")
                .displayedName("Exposure timer actual value hours(HH)")
                .description("Exposure timer actual value: hours")
                .unit(Unit.HOUR)                
                .readOnly()
                .commit(),
        
        INT32_ELEMENT(expected).key("exposuretimerActual.minutes")
                .displayedName("Exposure timer actual value minutes(MM)")
                .description("Exposure timer actual value: minutes")
                .unit(Unit.MINUTE)
                .readOnly()                
                .commit(),     
                
        INT32_ELEMENT(expected).key("exposuretimerActual.seconds")
                .displayedName("Exposure timer actual value seconds(SS)")
                .description("Exposure timer actual value: seconds")
                .unit(Unit.SECOND)
                .readOnly()
                .commit(),         
                            
        # Set the specified Exposure Timer ON/OFF
        SLOT_ELEMENT(expected).key("setExposureTimerOn")
                .tags("scpi")
                .alias("TS:{exposuretimer.number}")
                .displayedName("Exposure timer ON")
                .description("Turn the Exposure timer specified in the Exposure timer number field ON")
                .allowedStates("Ok.On")
                .commit(),
                
        SLOT_ELEMENT(expected).key("setExposureTimerOff")
                .tags("scpi")
                .alias("TE:{exposuretimer.number}")
                .displayedName("Exposure timer OFF")
                .description("Turn the Exposure timer specified in the Exposure timer number field OFF")
                .allowedStates("Ok.On")
                .commit(),
                
        # Read and display Status Words
        INT32_ELEMENT(expected).key("statusWord1")
                .tags("scpi poll")
                .alias(";;SR:01;*{statusWord1:d};") 
                .displayedName("Status Word 1")
                .description("Status Word 1 decimal value.")                                
                .allowedStates("Ok.On")                
                .commit(),
        
        INT32_ELEMENT(expected).key("statusWord1Bin")
                .displayedName("Status Word 1 binary")
                .description("Status Word 1 binary value.")                                
                .readOnly()
                .commit(), 
        
        INT32_ELEMENT(expected).key("statusWord2")
                .tags("scpi poll")
                .alias(";;SR:02;*{statusWord2:d};") 
                .displayedName("Status Word 2")
                .description("Status Word 2 decimal value.")                                
                .allowedStates("Ok.On")                
                .commit(),
                
        INT32_ELEMENT(expected).key("statusWord2Bin")
                .displayedName("Status Word 2 binary")
                .description("Status Word 2 binary value.")                                
                .readOnly()
                .commit(),
        
        INT32_ELEMENT(expected).key("statusWord3")
                .tags("scpi poll")
                .alias(";;SR:03;*{statusWord3:d};") 
                .displayedName("Status Word 3")
                .description("Status Word 3 decimal value.")                                
                .allowedStates("Ok.On")                
                .commit(),
                
        INT32_ELEMENT(expected).key("statusWord3Bin")
                .displayedName("Status Word 3 binary")
                .description("Status Word 3 binary value.")                                
                .readOnly()
                .commit(),
        
        INT32_ELEMENT(expected).key("statusWord4")
                .tags("scpi poll")
                .alias(";;SR:04;*{statusWord4:d};") 
                .displayedName("Status Word 4")
                .description("Status Word 4 decimal value.")                                
                .allowedStates("Ok.On")                
                .commit(),
                
        INT32_ELEMENT(expected).key("statusWord4Bin")
                .displayedName("Status Word 4 binary")
                .description("Status Word 4 binary value.")                                
                .readOnly()
                .commit(),
        
        INT32_ELEMENT(expected).key("statusWord6")
                .tags("scpi poll")
                .alias(";;SR:06;*{statusWord6:d};") 
                .displayedName("Status Word 6")
                .description("Status Word 6 decimal value.")                                
                .allowedStates("Ok.On")                
                .commit(),
                
        INT32_ELEMENT(expected).key("statusWord6Bin")
                .displayedName("Status Word 6 binary")
                .description("Status Word 6 binary value.")                                
                .readOnly()
                .commit(),
        
     
                
                
        )
        
    def followHardwareState(self):
        
        hwState = self.get("onState")
        swState = self.get("state")
        
        if swState=='Ok.Off' and hwState==1:
            self.log.INFO('Follow hardware state -> ON')
            self.followOn()
        elif swState=='Ok.On' and hwState==0:
            self.log.INFO('Follow hardware state -> OFF')
            self.followOff()
        
       
    
# This entry used by device server
if __name__ == "__main__":
    launchPythonDevice()
