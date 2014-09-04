#MAIN DATA_LOGGER PROGRAMM
from brickv.data_logger.bricklets import *
from brickv.data_logger.utils import *

import brickv.data_logger.utils as dlu

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
    b = Barometer_Bricklet(tmp.get_uid())
    b.start_timer(tmp.get_variables())
        

def main(ini_file_path):
    print "data_logger.main ini_file_paht = " + ini_file_path
    
    """CREATE-CONNECTION-TO-BRICKD"""
    #open IPConnection    
    dlu.IPCON = IPConnection()
  
    dlu.IPCON.connect(dlu.HOST, dlu.PORT)  # Connect to brickd
    print "IPCON.CONNECT"
    # Don't use device before ipcon is connected
    
    """SWITCH-CASE"""
    #TODO: switch-case
    #DUMMYS
    bricklets = []
    b1 = BrickletInfo(BAROMETER, "fVP")
    b1.addKeyValuePair(BAROMETER_AIR_PRESSURE, 1000)
    b1.addKeyValuePair(BAROMETER_ALTITUDE, 5000)
#     b2 = Bricklet_Info("Amb", AMBIENT_LIGHT, {AMBIENT_LIGHT_ANALOG_VALUE:1250,AMBIENT_LIGHT_ILLUMINANCE:3000})
#     b3 = Bricklet_Info("Hum", HUMIDITY, {HUMIDITY_ANALOG_VALUE:1111,HUMIDITY_HUMIDITY:2750})
    bricklets.append(b1)
#     bricklets.append(b2)
#     bricklets.append(b3)
    
    main_switch(bricklets)
    
    """START-WRITE-THREAD
    + create the magic sleep time
    """   
    #TODO: magic sleep time    
    if dlu.CB_SUM > 0 and dlu.CB_COUNT > 0:
        dlu.THREAD_SLEEP = dlu.CB_SUM/1000.0/dlu.CB_COUNT/dlu.CB_COUNT     #TODO: magical thread sleep -> need optimazation!
        print "magic thread sleep time = " + str(dlu.THREAD_SLEEP)
        print "CB_SUM   = " + str(dlu.CB_SUM)
        print "CB_COUNT = " + str(dlu.CB_COUNT)
         
    else:
        #TODO: else do smth?
        print "magic thread sleep time not defined! -> exit!"
        dlu.IPCON.disconnect()
        sys.exit(3)    
        
    #create write thread
    t = threading.Thread(name="Writer_Thread", target=dlu.writer_thread)
    dlu.Threads.append(t)
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
    dlu.THREAD_EXIT_FLAG = 1
    #wait for writer thread
    for th in  dlu.Threads:
        th.join()
    print "ALL WRITER-THREADS STOPPED"
     
    
    dlu.IPCON.disconnect()
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
            dlu.HOST = arg
        
        elif opt in ("-p", "--port"):
            dlu.PORT = arg
    
    if cl_ini_file == "":
        print "No config file!"
        print help_response
        sys.exit(2)
            
    print "HOST        = " + dlu.HOST
    print "PORT        = " + str(dlu.PORT)
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
    
    
    
    
    

    
    
