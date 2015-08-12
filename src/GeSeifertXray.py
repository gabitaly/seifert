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

        sigslot.registerSlot(self.setExposureTimerValues)

        sigslot.registerSlot(self.acknowledgeError)

        sigslot.registerSlot(self.setWarmupProgram)
        
        sigslot.registerSlot(self.openShutter)
        
        sigslot.registerSlot(self.closeShutter)
                                                       

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

    def setExposureTimerValues(self):
        ''' Set the Exposure Timer3 setpoint values'''
        try:
            self.sendCommand("setExposureTimerValues")
        except:
            raise     

    def acknowledgeError(self):
        ''' Error message cancellation '''
        try:
            self.sendCommand("acknowledgeError")
        except:
            raise    

    def setWarmupProgram(self):
        ''' Set warm-up program '''
        try:
            self.sendCommand("setWarmupProgram")
        except:
            raise
    
    def openShutter(self):
        ''' Open Beam Shutter 3 '''
        try:
            self.sendCommand("openShutter")
        except:
            raise    
 
    def closeShutter(self):
        ''' Close Beam Shutter 3 '''
        try:
            self.sendCommand("closeShutter")
        except:
            raise    
    
    @staticmethod
    def expectedParameters(expected):
        (
        
        ### Override scpi_device parameters ###
        
        
        # Define alias for the "on" slot
        SLOT_ELEMENT(expected).key("on")
                .tags("scpi")
                .alias("HV:1;;;;")
                .displayedName("START")
                .description("Turn hi voltage on")
                .expertAccess()
                .allowedStates("Ok.Off")
                .commit(),
        

        # Define alias for the "off" slot
        SLOT_ELEMENT(expected).key("off")
                .tags("scpi")
                .alias("HV:0;;;;")
                .displayedName("STOP")
                .description("Turn hi voltage off.")
                .expertAccess()
                .allowedStates("Ok.On")
                .commit(),
    
                        
        ### Define specific parameters ###
    
        # Define node for Current Setpoint
        NODE_ELEMENT(expected).key("current")
                .displayedName("Current Setpoint")
                .commit(),
        
        INT32_ELEMENT(expected).key("current.setpoint")
                .tags("scpi")
                .alias("SC:{current.setpoint};;;;") 
                .displayedName("Set target Current Setpoint")
                .description("The target value of the Current. "
                "Command format is xx, adhere typing 05 not 5.")
                .assignmentOptional().defaultValue(0)
                .minInc(0).maxInc(80)
                .unit(Unit.AMPERE).metricPrefix(MetricPrefix.MILLI)
                .allowedStates("Ok.On Ok.Off")
                .reconfigurable()
                .commit(),
        
        INT32_ELEMENT(expected).key("current.target")
                .tags("scpi poll")
                .alias(";;CN;*{current.target:d};")
                .displayedName("Target Current Setpoint")
                .description("The target value of the Current Setpoint.")
                .unit(Unit.AMPERE).metricPrefix(MetricPrefix.MILLI)
                .readOnly()
                .commit(),  
                
        INT32_ELEMENT(expected).key("current.actual")
                .tags("scpi poll")
                .alias(";;CA;*{current.actual:d};")
                .displayedName("Actual Current Setpoint")
                .description("The actual value of the Current Setpoint.")
                .unit(Unit.AMPERE).metricPrefix(MetricPrefix.MILLI)
                .readOnly()
                .commit(),        
                            
        # Define node for Voltage Setpoint
        NODE_ELEMENT(expected).key("voltage")
                .displayedName("Voltage Setpoint")
                .commit(), 
       
         # NOTE: this value is returned in Volts and has to be converted to kV
        INT32_ELEMENT(expected).key("voltage.setpoint")
                .tags("scpi")
                .alias("SV:{voltage.setpoint};;;;")
                .displayedName("Set target Voltage Setpoint")
                .description("The target value of the Voltage. "
                "Command format is xx, adhere typing 05 not 5. ")
                .assignmentOptional().defaultValue(0)
                .minInc(0).maxInc(60)
                .unit(Unit.VOLT).metricPrefix(MetricPrefix.KILO)
                .allowedStates("Ok.On Ok.Off")
                .reconfigurable()
                .commit(),
        
        INT32_ELEMENT(expected).key("voltage.target")
                .tags("scpi poll")
                .alias(";;VN;*{voltage.target:d};")
                .displayedName("Target Voltage Setpoint")
                .description("The target value of the Voltage Setpoint.")
                .unit(Unit.VOLT).metricPrefix(MetricPrefix.KILO)
                .readOnly()
                .commit(), 
                
        INT32_ELEMENT(expected).key("voltage.actual")
                .tags("scpi poll")
                .alias(";;VA;*{voltage.actual:d};")
                .displayedName("Actual Voltage Setpoint")
                .description("The actual value of the Voltage Setpoint.")
                .unit(Unit.VOLT).metricPrefix(MetricPrefix.KILO)
                .readOnly()
                .commit(),                        
    
        # Define and configure the Exposure Timers
        
        NODE_ELEMENT(expected).key("exposuretimer")
                .displayedName("Exposure Timer 3 Setpoints")
                .commit(),
             
        INT32_ELEMENT(expected).key("exposuretimer.hours")
                .displayedName("Exposure timer setpoint hours")
                .description("Exposure timer setpoint value [hrs]")
                .unit(Unit.HOUR)
                .assignmentOptional().defaultValue(0)
                .allowedStates("Ok.On Ok.Off")
                .minInc(0).maxInc(99)
                .reconfigurable()
                .commit(),
        
        INT32_ELEMENT(expected).key("exposuretimer.minutes")
                .displayedName("Exposure timer setpoint minutes")
                .description("Exposure timer setpoint value [min]")
                .unit(Unit.MINUTE)
                .assignmentOptional().defaultValue(0)
                .allowedStates("Ok.On Ok.Off")
                .minInc(0).maxInc(59)
                .reconfigurable()
                .commit(),     
                
        INT32_ELEMENT(expected).key("exposuretimer.seconds")
                .displayedName("Exposure timer setpoint seconds")
                .description("Exposure timer setpoint value [sec}")
                .unit(Unit.SECOND)
                .assignmentOptional().defaultValue(0)
                .allowedStates("Ok.On Ok.Off")
                .minInc(0).maxInc(59)
                .reconfigurable()
                .commit(), 
        
        INT32_ELEMENT(expected).key("exposuretimer.target")
                .tags("scpi poll")
                .alias(";;TN:3;*{exposuretimer.target:d};") 
                .displayedName("Exposure Timer 3 target value [sec]")
                .description("Exposure Timer 3 target value [sec]")                
                .unit(Unit.SECOND)
                .readOnly()
                .commit(), 
                
        #Set Exposure Timer Setpoints. NOTE: reply is in seconds, needs conversion to HH,MM,SS 
        
        SLOT_ELEMENT(expected).key("setExposureTimerValues")
                .tags("scpi")
                .alias("TP:3,{exposuretimer.hours},{exposuretimer.minutes},{exposuretimer.seconds};;;;") 
                .displayedName("Set target Exposure timer 3 setpoints")
                .description("Set the targets for the specified Exposure Timer setpoints.")                                
                .allowedStates("Ok.On Ok.Off")                
                .commit(),                                               
        
        # Set the specified Exposure Timer ON/OFF
        
        SLOT_ELEMENT(expected).key("setExposureTimerOn")
                .tags("scpi")
                .alias("TS:3;;;;")
                .displayedName("Turn Exposure timer 3 ON")
                .description("Turn the specified Exposure timer ON")
                .allowedStates("Ok.On Ok.Off")
                .commit(),
                
        SLOT_ELEMENT(expected).key("setExposureTimerOff")
                .tags("scpi")
                .alias("TE:3;;;;")
                .displayedName("Turn Exposure timer 3 OFF")
                .description("Turn the specified Exposure timer OFF")
                .allowedStates("Ok.On Ok.Off")
                .commit(),
                
        # Displays the Exposure Timer Actual values      
        
        NODE_ELEMENT(expected).key("exposuretimerActual")
                .displayedName("Exposure Timer 3 Actual Values")
                .commit(),                        
      
        INT32_ELEMENT(expected).key("exposuretimerActual.hours")
                .displayedName("Exposure timer actual value hours")
                .description("Exposure timer actual value: hours")
                .unit(Unit.HOUR)                
                .readOnly() 
                .commit(),
        
        INT32_ELEMENT(expected).key("exposuretimerActual.minutes")
                .displayedName("Exposure timer actual value minutes")
                .description("Exposure timer actual value: minutes")
                .unit(Unit.MINUTE)
                .readOnly()                
                .commit(),     
                
        INT32_ELEMENT(expected).key("exposuretimerActual.seconds")
                .displayedName("Exposure timer actual value seconds")
                .description("Exposure timer actual value: seconds")
                .unit(Unit.SECOND)
                .readOnly()
                .commit(),    
                        
        INT32_ELEMENT(expected).key("exposuretimerActual.totalSec")
                .tags("scpi poll")
                .alias(";;TA:3;*{exposuretimerActual.totalSec:d};") 
                .displayedName("Exposure Timer actual value [sec]")
                .description("Exposure Timer actual value [sec]")                
                .unit(Unit.SECOND)
                .readOnly()
                .commit(),
        
        
        # Read and clear status message
        
        NODE_ELEMENT(expected).key("statusMassage")
                .displayedName("Status Message")
                .commit(),   
                
        INT32_ELEMENT(expected).key("statusMassage.statusWord12")
                .tags("scpi poll")
                .alias(";;SR:12;*{statusMassage.statusWord12:d};") 
                .displayedName("Status Word 12 Code")
                .description("Status Word 12 Code.")        
                .readOnly()                 
                .commit(),
               
        STRING_ELEMENT(expected).key("statusMassage.statusWord12Str")
                .displayedName("Status Word 12 Message")
                .description("Status Word 12 Message")             
                .readOnly()
                .commit(), 
        
        SLOT_ELEMENT(expected).key("acknowledgeError")
                .tags("scpi")
                .alias("CL;;;;")
                .displayedName("Acknowledge Error")
                .description("Cancellation of message.")
                .commit(),
              
        # Read and display Status Words
        
        NODE_ELEMENT(expected).key("sw")
                .displayedName("Status Words")
                .commit(),  
             
        INT32_ELEMENT(expected).key("sw.statusWord1")
                .tags("scpi poll")
                .alias(";;SR:01;*{sw.statusWord1:d};") 
                .displayedName("Status Word 1")
                .description("Status Word 1 decimal value.")                 
                .readOnly()                               
                .commit(),
        
        INT32_ELEMENT(expected).key("sw.statusWord1Bin")
                .displayedName("Status Word 1 binary")
                .description("Status Word 1: "
                "Ext.Computer Control|High Voltage|Cooling Circuit|Buffer Battery|mA Nom=Actual|kV Nom=Actual|Shutter Status|Not used ")
                .readOnly()
                .commit(), 
        
        INT32_ELEMENT(expected).key("sw.statusWord2")
                .tags("scpi poll")
                .alias(";;SR:02;*{sw.statusWord2:d};") 
                .displayedName("Status Word 2")
                .description("Status Word 2 decimal value.")                
                .readOnly()                 
                .commit(),
                
        INT32_ELEMENT(expected).key("sw.statusWord2Bin")
                .displayedName("Status Word 2 binary")
                .description("Status Word 2: "
                "Timer1|Timer2|Timer3|Timer4|ShutterControl1|ShutterControl2|ShutterControl3|ShutterControl4 ")  
                .readOnly()
                .commit(),
        
        INT32_ELEMENT(expected).key("sw.statusWord3")
                .tags("scpi poll")
                .alias(";;SR:03;*{sw.statusWord3:d};") 
                .displayedName("Status Word 3")
                .description("Status Word 3 decimal value.")                
                .readOnly()                 
                .commit(),
                
        INT32_ELEMENT(expected).key("sw.statusWord3Bin")
                .displayedName("Status Word 3 binary")
                .description("Status Word 3: "
                "Shutter1Command|Shutter1Status|Shutter1 Non-Syst.Closed|Shutter1Connected|Shutter2Command|Shutter2Status|Shutter2 Non-syst.Closed|Shutter2Connected ")   
                .readOnly()
                .commit(),
        
        INT32_ELEMENT(expected).key("sw.statusWord4")
                .tags("scpi poll")
                .alias(";;SR:04;*{sw.statusWord4:d};") 
                .displayedName("Status Word 4")
                .description("Status Word 4 decimal value.")                
                .readOnly()                
                .commit(),
                
        INT32_ELEMENT(expected).key("sw.statusWord4Bin")
                .displayedName("Status Word 4 binary")
                .description("Status Word 4: "
                "Shutter3Command|Shutter3Status|Shutter3 Non-Syst.Closed|Shutter3Connected|Shutter4Command|Shutter4Status|Shutter4 Non-syst.Closed|Shutter4Connected ")  
                .readOnly()
                .commit(),
        
        INT32_ELEMENT(expected).key("sw.statusWord6")
                .tags("scpi poll")
                .alias(";;SR:06;*{sw.statusWord6:d};") 
                .displayedName("Status Word 6")
                .description("Status Word 6 decimal value.")        
                .readOnly()                 
                .commit(),
                
        INT32_ELEMENT(expected).key("sw.statusWord6Bin")
                .displayedName("Status Word 6 binary")
                .description("Status Word 6: "
                "Not Used|Not Used|Not Used|Not Used|Warm-up Progr.|Warm-up Aborted|Warm-up via Ext.Computer|Warm-up via Keeyboard ")             
                .readOnly()
                .commit(),      
        
        # Set and read the Water Flow Rate
        INT32_ELEMENT(expected).key("sw.statusWord14")
                .tags("scpi")
                .alias("SW:14:{sw.statusWord14};;;;")
                .displayedName("Set target Minimum Water Flow Rate")
                .description("Target Minimum Water Flow Rate. Min 181Hz, Max 250Hz")
                .assignmentOptional().defaultValue(181)
                .minInc(181).maxInc(250)
                .unit(Unit.HERTZ)
                .allowedStates("Ok.On Ok.Off")
                .reconfigurable()
                .commit(),
        
        INT32_ELEMENT(expected).key("sw.statusWord14Actual")
                .tags("scpi poll")
                .alias(";;SR:14;*{sw.statusWord14Actual:d};") 
                .displayedName("Minimum Water Flow Rate actual value")
                .description("Minimum Water Flow Rate actual value. Min 181Hz, Max 250Hz")        
                .readOnly()                 
                .commit(), 
        
        INT32_ELEMENT(expected).key("sw.statusWord15")
                .tags("scpi poll")
                .alias(";;SR:15;*{sw.statusWord15:d};") 
                .displayedName("Water Flow Rate actual")
                .description("Water Flow Rate actual value. Max 250Hz")  
                .unit(Unit.HERTZ)
                .readOnly()                 
                .commit(),         
                
        # Warm-up program
        NODE_ELEMENT(expected).key("warmup")
                .displayedName("Warm-up Program")
                .commit(),   
        
        INT32_ELEMENT(expected).key("warmup.time")
                .displayedName("Non-operative interval time")
                .description("Non-operative interval. "
                "0 = no warm-up, 1 = one day, 2 = 2 days, 3 = 1 week, 4 = via RTC ")
                .assignmentOptional().defaultValue(0)
                .allowedStates("Ok.On Ok.Off")
                .options("0 1 2 3 4") 
                .reconfigurable()
                .commit(), 
                
        INT32_ELEMENT(expected).key("warmup.voltage")
                .displayedName("Test voltage")
                .description("Test voltage")                
                .assignmentOptional().defaultValue(0)
                .allowedStates("Ok.On Ok.Off")
                .unit(Unit.VOLT).metricPrefix(MetricPrefix.KILO)
                .minInc(0).maxInc(60) 
                .reconfigurable()
                .commit(),         
        
        SLOT_ELEMENT(expected).key("setWarmupProgram")
                .tags("scpi")
                .alias("WU:{warmup.time},{warmup.voltage};;;;")
                .displayedName("Set Warm-up program")
                .description("Set Warm-up program (time and voltage)")
                .commit(),
                
        INT32_ELEMENT(expected).key("warmup.timeleft")
                .tags("scpi poll")
                .alias(";;WT;*{warmup.timeleft:d};") 
                .displayedName("Warm-up time left")
                .description("Warm-up time left")  
                .unit(Unit.SECOND)
                .readOnly()                 
                .commit(), 
                
        NODE_ELEMENT(expected).key("keypadOnOff")
                .displayedName("Enable/Disable Keypad")
                .commit(),
            
        INT32_ELEMENT(expected).key("keypadOnOff.OnOff")
                .tags("scpi")
                .alias("KB:{keypadOnOff.OnOff};;;;") 
                .displayedName("Enable/Disable Keypad")
                .description("Enable/Disable Keypad. 0 = blocked except for key STOP, 1 = enabled ")
                .assignmentOptional().defaultValue(1)
                .allowedStates("Ok.On Ok.Off")
                .options("0 1")
                .reconfigurable()
                .commit(),
        
        NODE_ELEMENT(expected).key("focus")
                .displayedName("Focus")
                .commit(),        
                
        STRING_ELEMENT(expected).key("focus.string")
                .tags("scpi poll")
                .alias(";;FR;{focus.string};") 
                .displayedName("Focus settings")
                .description("Focus settings string.")                  
                .readOnly()                 
                .commit(),
                
        NODE_ELEMENT(expected).key("anode")
                .displayedName("Anode material")
                .commit(),        
                
        STRING_ELEMENT(expected).key("anode.material")
                .tags("scpi poll")
                .alias(";;MR;{anode.material};") 
                .displayedName("Anode material type")
                .description("Anode material string.")                  
                .readOnly()                 
                .commit(), 
        
        NODE_ELEMENT(expected).key("beamshutter")
                .displayedName("Beam Shutter 3 Control")
                .commit(),   
                
        STRING_ELEMENT(expected).key("beamshutter.control")
                .tags("scpi")
                .alias("CC:{beamshutter.control};;;;") 
                .displayedName("Control via keypad/computer")
                .description("Beam shutter 3 control: 0000 = via keypad, 0010 = via computer.")  
                .assignmentOptional().defaultValue("0010")
                .options("0000 0010")
                .reconfigurable()
                .commit(),
        
        SLOT_ELEMENT(expected).key("openShutter")
                .tags("scpi")
                .alias("OS:3;;;;") 
                .displayedName("Open Beam Shutter 3")
                .description("Open beam shutter 3.")                
                .commit(),
                
        SLOT_ELEMENT(expected).key("closeShutter")
                .tags("scpi")
                .alias("CS:3;;;;") 
                .displayedName("Close Beam Shutter 3")
                .description("Close beam shutter 3.")                                              
                .commit(),
                
        STRING_ELEMENT(expected).key("beamshutter.status")                                
                .displayedName("Status: ")
                .description("Status of the bean shutter: open/closed")  
                .readOnly()                                 
                .commit(),        
        
        )
    """   
    def followHardwareState(self):
        
        hwState = self.get("onState")
        swState = self.get("state")
        
        if swState=='Ok.Off' and hwState==1:
            self.log.INFO('Follow hardware state -> ON')
            self.followOn()
        elif swState=='Ok.On' and hwState==0:
            self.log.INFO('Follow hardware state -> OFF')
            self.followOff()
    """
    ### Override base class post-processing method pollInstrumentSpecific ###
    def pollInstrumentSpecific(self): 


       '''Status Word 12 messages'''
       statusWord12Msg = {
       0:'No messages',
       33:'Cooling system failed',
       37:'Absolute undervoltage monitoring',
       38:'Absolute overvoltage monitoring',
       39:'Absolute undercurrent monitoring',
       43:'Extern stop',
       46:'EMERGENCY-STOP',
       49:'Preselection exceeded rated power',
       50:'Tube overpower',
       51:'Preselection out of range',
       52:'Presel.exceeding rated generator current',
       53:'High voltage lamp defective',
       55:'Relative overcurrent monitoring',
       56:'Relative undervoltage monitoring',
       60:'Relative undercurrent monitoring',
       63:'Door contact 1 and 2 open',
       64:'Door contact 1 open',
       65:'Door contact 2 open',
       67:'Temp. supervision cooling system',
       70:'Tube to be warmed up?',
       72:'Preselection out of range',
       76:'----Stand-by----',
       80:'Temperature supervision power module',
       86:'HV contact faulty',
       90:'Fault in filament circuit',
       91:'Buffer battery empty',
       96:'Shutter non-systematically closed',
       97:'Shutter not connected',
       98:'Shutter not opened',
       99:'Shutter not closed',
       104:'External warning lamp failed',
       105:'Temperature supervision generator',
       106:'Warm-up necessary',
       108:'Power fail (low voltage)',
       109:'Warm-up! 0=No',
       112:'Shutter safety circuit open',
       113:'Absolute overcurrent monitoring',
       114:'Relative overvoltage monitoring',
       116:'Warm-up terminated after 3 attempts',
       117:'Warm-up aborted. Try again',
       118:'Push START button'}


       '''Current setpoint is returned in uA, convert to mA'''
       targetInmA = self.get("current.target") // 1000
       self.set("current.target",targetInmA)
       actualInmA = self.get("current.actual") // 1000
       self.set("current.actual",actualInmA)

       '''Voltage setpoint returned in Volt, convert to kV'''
       targetInKV = self.get("voltage.target") // 1000
       self.set("voltage.target",targetInKV)
       actualInKV = self.get("voltage.actual") // 1000
       self.set("voltage.actual",actualInKV)     
       
       '''Exposure timer actual value returned in sec., convert to hh,mm,ss'''
       mm, ss = divmod(self.get("exposuretimerActual.totalSec"),60)
       hh, mm = divmod(mm, 60)
       self.set("exposuretimerActual.hours",hh)
       self.set("exposuretimerActual.minutes",mm)
       self.set("exposuretimerActual.seconds",ss)

       
       '''Process Status Words'''
       sw1 = self.get("sw.statusWord1")
       sw1Bin = "{0:8b}".format(sw1)
       self.set("sw.statusWord1Bin",sw1Bin)

       sw2 = self.get("sw.statusWord2")
       sw2Bin = "{0:8b}".format(sw2)
       self.set("sw.statusWord2Bin",sw2Bin)

       sw3 = self.get("sw.statusWord3")
       sw3Bin = "{0:8b}".format(sw3)
       self.set("sw.statusWord3Bin",sw3Bin)

       sw4 = self.get("sw.statusWord4")
       sw4Bin = "{0:8b}".format(sw4)
       self.set("sw.statusWord4Bin",sw4Bin)
       
       BeamShutterStatus = sw4 & 0b01000000 # Check Bit6 "Shutter 3 Status" and set the string
       if BeamShutterStatus > 0:
           text = "Open"
           self.set("beamshutter.status",text)
       else:
           text = "Closed"
           self.set("beamshutter.status",text)                      
       
       sw6 = self.get("sw.statusWord6")
       sw6Bin = "{0:8b}".format(sw6)
       self.set("sw.statusWord6Bin",sw6Bin)
       
       ### Display Status Word 12 message ###
       msgIdx = self.get("statusMassage.statusWord12")
       msgTxt = statusWord12Msg[msgIdx]
       self.set("statusMassage.statusWord12Str",msgTxt)
                     
       
    
# This entry used by device server
if __name__ == "__main__":
    launchPythonDevice()
