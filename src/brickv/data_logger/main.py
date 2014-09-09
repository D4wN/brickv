#MAIN DATA_LOGGER PROGRAMM
from brickv.data_logger.bricklets import *
from brickv.data_logger.utils import *

import brickv.data_logger.utils as dlu

import argparse                             # command line argument parser
import sys

""" 
- __main__
- brickv entry point
- switch-cases

"""
###switch###
def general_switch(data):
    #TODO: write code to process data out of the xively
    pass

def xively_switch(data):
    #TODO: write code
    pass

def bricklet_switch(data):
    # TODO: Check if there are bricklets
    
    for current_bricklet in data:
        bricklet_name = current_bricklet.name
        bricklet_uid = current_bricklet.uid
        bricklet_variables = current_bricklet.variables
        
        # TODO: yes add all bricklets here
        if (bricklet_name == AMBIENT_LIGHT ):
            print bricklet_variables
            AmbientLightBricklet(bricklet_uid).start_timer(bricklet_variables)
        elif(bricklet_name == ANALOG_IN):
            AnalogInBricklet(bricklet_uid).start_timer(bricklet_variables)
        elif(bricklet_name == ANALOG_OUT):
            AnalogOutBricklet(bricklet_uid).start_timer(bricklet_variables)              
        elif(bricklet_name == BAROMETER):
            BarometerBricklet(bricklet_uid).start_timer(bricklet_variables)
        elif(bricklet_name == COLOR):
            ColorBricklet(bricklet_uid).start_timer(bricklet_variables)
        elif(bricklet_name == CURRENT_12):
            Current12Bricklet(bricklet_uid).start_timer(bricklet_variables)
        elif(bricklet_name == CURRENT_25):
            Current25Bricklet(bricklet_uid).start_timer(bricklet_variables)    
        elif(bricklet_name == DISTANCE_IR):
            DistanceIRBricklet(bricklet_uid).start_timer(bricklet_variables)
        elif(bricklet_name == DISTANCE_US):
            DistanceUSBricklet(bricklet_uid).start_timer(bricklet_variables)
        elif(bricklet_name == DUAL_BUTTON ):
            DualButtonBricklet(bricklet_uid).start_timer(bricklet_variables)
        elif(bricklet_name == DUAL_RELAY):
            DualRelayBricklet(bricklet_uid).start_timer(bricklet_variables)
        elif(bricklet_name == GPS_BRICKLET):
            GPSBricklet(bricklet_uid).start_timer(bricklet_variables)
        elif(bricklet_name == HALL_EFFECT):
            HallEffectBricklet(bricklet_uid).start_timer(bricklet_variables)
        elif(bricklet_name == HUMIDITY ):
            HumidityBricklet(bricklet_uid).start_timer(bricklet_variables)
        elif(bricklet_name == INDUSTRIAL_DIGITAL_IN_4 ):
            IndustrialDigitalIn4Bricklet(bricklet_uid).start_timer(bricklet_variables)      
        elif(bricklet_name == INDUSTRIAL_DIGITAL_OUT_4):
            IndustrialDigitalOut4Bricklet(bricklet_uid).start_timer(bricklet_variables)
        elif(bricklet_name == INDUSTRIAL_DUAL_0_20_MA):
            IndustrialDual020mABricklet(bricklet_uid).start_timer(bricklet_variables)
        elif(bricklet_name == INDUSTRIAL_QUAD_RELAY ):
            IndustrialQuadRelayBricklet(bricklet_uid).start_timer(bricklet_variables)
        elif(bricklet_name == IO_16):
            IO16Bricklet(bricklet_uid).start_timer(bricklet_variables) 
        elif(bricklet_name == IO_4):
            IO4Bricklet(bricklet_uid).start_timer(bricklet_variables) 
        elif(bricklet_name == JOYSTICK ):
            JoystickBricklet(bricklet_uid).start_timer(bricklet_variables) 
        elif(bricklet_name == LCD_16x2 ):
            LCD16x2Bricklet(bricklet_uid).start_timer(bricklet_variables) 
        elif(bricklet_name == LCD_20x4 ):
            LCD20x4Bricklet(bricklet_uid).start_timer(bricklet_variables) 
        elif(bricklet_name == LED_STRIP ):
            LEDStripBricklet(bricklet_uid).start_timer(bricklet_variables)
        elif(bricklet_name == LINE):
            LineBricklet(bricklet_uid).start_timer(bricklet_variables)
        elif(bricklet_name == LINEAR_POTI ):
            LinearPotiBricklet(bricklet_uid).start_timer(bricklet_variables)
        elif(bricklet_name == MOISTURE ):
            MoistureBricklet(bricklet_uid).start_timer(bricklet_variables)
        elif(bricklet_name == MOTION_DETECTOR ):
            MotionDetectorBricklet(bricklet_uid).start_timer(bricklet_variables)
        elif(bricklet_name == MULTI_TOUCH ):
            MultiTouchBricklet(bricklet_uid).start_timer(bricklet_variables)
        elif(bricklet_name == NFC_RFID):
            NFCRFIDBricklet(bricklet_uid).start_timer(bricklet_variables)
        elif(bricklet_name == PIEZO_BUZZER ):
            PiezoBuzzerBricklet(bricklet_uid).start_timer(bricklet_variables)
        elif(bricklet_name == PIEZO_SPEAKER ):
            PiezoSpeakerBricklet(bricklet_uid).start_timer(bricklet_variables)
        elif(bricklet_name == PTC_BRICKLET):
            PTCBricklet(bricklet_uid).start_timer(bricklet_variables)
        elif(bricklet_name == REMOTE_SWITCH ):
            RemoteSwitchBricklet(bricklet_uid).start_timer(bricklet_variables)
        elif(bricklet_name == ROTARY_ENCODER ):
            RotaryEncoderBricklet(bricklet_uid).start_timer(bricklet_variables)  
        elif(bricklet_name == ROTARY_POTI ):
            RotaryPotiBricklet(bricklet_uid).start_timer(bricklet_variables)
        elif(bricklet_name == SEGMENT_DISPLAY_4x7 ):
            SegmentDisplay4x7Bricklet(bricklet_uid).start_timer(bricklet_variables)  
        elif(bricklet_name == SOLID_STATE_RELAY ):
            SolidStateRelayBricklet(bricklet_uid).start_timer(bricklet_variables)
        elif(bricklet_name == SOUND_INTENSITY ):
            SoundIntensityBricklet(bricklet_uid).start_timer(bricklet_variables)
        elif(bricklet_name == TEMPERATURE ):
            TemperatureBricklet(bricklet_uid).start_timer(bricklet_variables)
        elif(bricklet_name == TEMPERATURE_IR ):
            TemperatureIRBricklet(bricklet_uid).start_timer(bricklet_variables)
        elif(bricklet_name == TILT ):
            TiltBricklet(bricklet_uid).start_timer(bricklet_variables)
        elif(bricklet_name == VOLTAGE ):
            VoltageBricklet(bricklet_uid).start_timer(bricklet_variables)
        elif(bricklet_name == VOLTAGE_CURRENT ):
            VoltageCurrentBricklet(bricklet_uid).start_timer(bricklet_variables)
        else:
            # TODO: Send err msg to user
            print "There is no bricklet with name: " + bricklet_name
                     
            
def main(ini_file_path):
    print "data_logger.main ini_file_paht = " + ini_file_path
    # exit if the path to the configuration file is invalid
    if (ini_file_path == "None"):
        sys.exit(-1) 
        
    '''Parse configuration file'''
    configFile = DataLoggerConfig(ini_file_path);
    configFile.read_config_file()
    
    """CREATE-CONNECTION-TO-BRICKD"""
    #open IPConnection    
    DataLogger.ipcon = IPConnection()
  
    DataLogger.ipcon.connect(DataLogger.host, DataLogger.port)  # Connect to brickd
    print "IPCON.CONNECT"
    # Don't use device before ipcon is connected
    
    general_switch(configFile.get_general_section())
    xively_switch(configFile.get_xively_section())
    bricklet_switch(configFile.get_bricklets())
    
    
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

def command_line_start(argv,program_name):
    cl_parser = argparse.ArgumentParser(description=' -c <config-file>')
    

    cl_parser.add_argument('-c', action="store", dest="config_file", default="None", help="Path to the configuration file")
    results = cl_parser.parse_args(argv)

    return results.config_file


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
    ini_file_path = command_line_start(sys.argv[1:], sys.argv[0]) 
    main(ini_file_path)
