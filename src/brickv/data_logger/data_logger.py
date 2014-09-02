#MAIN DATA_LOGGER PROGRAMM
from data_logger_bricklets import *
from data_logger_utils import *
import data_logger_bricklets as dlb         #TODO: get referenced object







""" 
- __main__
- brickv entry point
- switch-cases

"""
###switch###
def main_switch(data):  
    general_switch(data)
    xively_switch(data)
    bricklet_switch(data)

def general_switch(data):
    pass

def xively_switch(data):
    pass

def bricklet_switch(data):
    tmp = data[0]
    b = Barometer_Bricklet(tmp.get_uid())
    b.start_timer(tmp)
        

def main():

    #DUMMYS
    bricklets = []
    b1 = Bricklet_Info(BAROMETER, "fVP")
    b1.addKeyValuePair(BAROMETER_AIR_PRESSURE, 1000)
    b1.addKeyValuePair(BAROMETER_ALTITUDE, 0)
#     b2 = Bricklet_Info("Amb", AMBIENT_LIGHT, {AMBIENT_LIGHT_ANALOG_VALUE:1250,AMBIENT_LIGHT_ILLUMINANCE:3000})
#     b3 = Bricklet_Info("Hum", HUMIDITY, {HUMIDITY_ANALOG_VALUE:1111,HUMIDITY_HUMIDITY:2750})
    bricklets.append(b1)
#     bricklets.append(b2)
#     bricklets.append(b3)
    
    main_switch(bricklets)
    
    
    
    raw_input('Press key to close\n')  # Use input() in Python 3
    
    #stop Timers
    for t in LoggerTimer.Timers:
        t.cancel()
    #check if timer stopped
    for t in LoggerTimer.Timers:
        t.join()
    

from tinkerforge.ip_connection import IPConnection
###main###
if __name__ == '__main__':      
     
    """PARSE-INI""" 
    """START-WRITE-THREAD"""
    """CREATE-CONNECTION-TO-MASTERBRICK"""
    """SWITCH-CASE"""
    """INIT-CALLBACK"""
    """END_CONDITIONS"""
    """DEBUG-READ-CSV""" 
    
    #open OPConnection    
    dlb.IPCON = IPConnection()
 
    #both from ini-parser TODO:
    HOST = "localhost"    
    PORT = 4223
 
    dlb.IPCON.connect(HOST, PORT)  # Connect to brickd
    # Don't use device before ipcon is connected
     
    main()
    
    dlb.IPCON.disconnect()
    print "IPCON.DISCONNECT()"
    
    
