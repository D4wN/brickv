#MAIN DATA_LOGGER PROGRAMM
from brickv.data_logger.bricklets import *
from brickv.data_logger.utils import *

import getopt                               #command_line()

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
    #TODO: write code
    pass

def xively_switch(data):
    #TODO: write code
    pass

def bricklet_switch(data):
    #TODO: write code
    tmp = data[0]
    b = BarometerBricklet(tmp.uid)
#     b.start_timer(tmp.variables)
     
    tmp = data[1]
    a = AmbientLightBricklet("amb")
    a.start_timer(tmp.variables)
     
    tmp = data[2]
    h = HumidityBricklet(tmp.uid)
#     h.start_timer(tmp.variables)        

def main(ini_file_path):
    print "data_logger.main ini_file_paht = " + ini_file_path
    
    """CREATE-CONNECTION-TO-BRICKD"""
    #open IPConnection    
    DataLogger.ipcon = IPConnection()
  
    DataLogger.ipcon.connect(DataLogger.host, DataLogger.port)  # Connect to brickd
    print "IPCON.CONNECT"
    # Don't use device before ipcon is connected
    
    """SWITCH-CASE"""
    #TODO: switch-case
    #DUMMYS
    bricklets = []
    b1 = BrickletInfo(BAROMETER, "fVP")
    b1.add_key_value_pair(BAROMETER_AIR_PRESSURE, 1000)
    b1.add_key_value_pair(BAROMETER_ALTITUDE, 5000)
    
    b2 = BrickletInfo(AMBIENT_LIGHT, "hZD")
    b2.add_key_value_pair(AMBIENT_LIGHT_ANALOG_VALUE, 2000)
    b2.add_key_value_pair(AMBIENT_LIGHT_ILLUMINANCE, 1500)
    
    b3 = BrickletInfo(HUMIDITY, "hTH")
    b3.add_key_value_pair(HUMIDITY_ANALOG_VALUE, 4000)
    b3.add_key_value_pair(HUMIDITY_HUMIDITY, 6000)
    
    bricklets.append(b1)
    bricklets.append(b2)
    bricklets.append(b3)
    
    main_switch(bricklets)
    
    """START-WRITE-THREAD
    + create the magic sleep time
    """   
    #TODO: magic sleep time    
    if DataLogger.CB_SUM > 0 and DataLogger.CB_COUNT > 0:
        DataLogger.THREAD_SLEEP = DataLogger.CB_SUM/1000.0/DataLogger.CB_COUNT/DataLogger.CB_COUNT     #TODO: magical thread sleep -> need optimazation!
        print "magic thread sleep time = " + str(DataLogger.THREAD_SLEEP)
        print "CB_SUM   = " + str(DataLogger.CB_SUM)
        print "CB_COUNT = " + str(DataLogger.CB_COUNT)
         
    else:
        #TODO: else do smth?
        print "magic thread sleep time not defined! -> exit!"
        DataLogger.ipcon.disconnect()
        sys.exit(3)    
        
    #create write thread
    t = threading.Thread(name="Writer_Thread", target=writer_thread)
    DataLogger.Threads.append(t)
    t.start()
    
    
    """START-TIMERS"""
    for t in LoggerTimer.Timers:
        t.start()
        
    """END_CONDITIONS"""
    raw_input('Press key to close\n')  # Use input() in Python 3
    
    #stop Timers--------------------
    for t in LoggerTimer.Timers:
        t.cancel()
    #check if timer stopped
    for t in LoggerTimer.Timers:
        t.join()
    print "ALL TIMERS STOPPED"
    
    #stop writer thread-------------
    #set stop flag for writer thread
    DataLogger.THREAD_EXIT_FLAG = 1
    #wait for writer thread
    for th in  DataLogger.Threads:
        th.join()
    print "ALL WRITER-THREADS STOPPED"
     
    
    DataLogger.ipcon.disconnect()
    print "IPCON.DISCONNECT()"

def command_line(argv, program_name):
    #http://www.diveintopython.net/scripts_and_streams/command_line_arguments.html
    help_response = program_name + " -c <config-file> [-m <host-address> -p <host-port>]"
    cl_ini_file = ""
        
    try:
        opts, args = getopt.getopt(argv,"hc:m:p:",["help", "config=", "host=", "port="])
        
    except getopt.GetoptError:
        print help_response
        sys.exit(2)
        
    for opt, arg in opts:
        if opt == '-h' or opt == "--help":
            print help_response
            sys.exit()
        
        elif opt in ("-c", "--config"):
            cl_ini_file = arg
        
        elif opt in ("-m", "--host"):
            DataLogger.host = arg
        
        elif opt in ("-p", "--port"):
            DataLogger.port = arg
    
    if cl_ini_file == "":
        print "No config file!"
        print help_response
        sys.exit(2)
            
    print "HOST        = " + DataLogger.host
    print "PORT        = " + str(DataLogger.port)
    print "Config-File = " + cl_ini_file     
    
    return cl_ini_file

from tinkerforge.ip_connection import IPConnection
###main###
if __name__ == '__main__':      
    """PARSE-INI
    command-line-start:
        - check arguments
            - must have: config-file-path
        - get HOST and PORT from command-line arguments / ini file
            - create DEFAULT values for both ("localhost", 4223)
        
        
    gui-start:
        
    both:
        - set DEFAULT_FILE_PATH
    """ 
    ini_file_path = command_line(sys.argv[1:], sys.argv[0])
    
    main(ini_file_path)
    
    
    
    
    

    
    
