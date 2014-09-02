#MAIN DATA_LOGGER PROGRAMM
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
    tmp.to_string()
    b = Barometer_Bricklet(tmp.uid)
    b.start_timer(tmp.variables)
        

###main###
if __name__ == '__main__':      
    
    """PARSE-INI""" 
    """START-WRITE-THREAD"""
    """CREATE-CONNECTION-TO-MASTERBRICK"""
    """SWITCH-CASE"""
    """INIT-CALLBACK"""
    """END_CONDITIONS"""
    """DEBUG-READ-CSV"""  
    
    ipcon = IPConnection()  # Create IP connection
  

    ipcon.connect(HOST, PORT)  # Connect to brickd
    # Don't use device before ipcon is connected
    #DUMMYS
    bricklets = []
    b1 = Bricklet_Info("fVP", BAROMETER, {BAROMETER_AIR_PRESSURE:0,BAROMETER_ALTITUDE:0})
    b2 = Bricklet_Info("Amb", AMBIENT_LIGHT, {AMBIENT_LIGHT_ANALOG_VALUE:1250,AMBIENT_LIGHT_ILLUMINANCE:3000})
    b3 = Bricklet_Info("Hum", HUMIDITY, {HUMIDITY_ANALOG_VALUE:1111,HUMIDITY_HUMIDITY:2750})
    bricklets.append(b1)
    bricklets.append(b2)
    bricklets.append(b3)
    
    main_switch(bricklets)
    
    raw_input('Press key to close\n')  # Use input() in Python 3
    
    #stop Timers
    for t in timers:
        t.cancel()
    #check if timer stopped
    for t in timers:
        t.join()
    
    ipcon.disconnect()
    
    
