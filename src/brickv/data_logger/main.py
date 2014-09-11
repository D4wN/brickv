#MAIN DATA_LOGGER PROGRAMM
from brickv.data_logger.bricklets import *
from brickv.data_logger.utils import *

import argparse                             # command line argument parser
#import sys
#import logging                              #static logging system

""" 
- __main__
- brickv entry point
- switch-cases

"""
###switch###
def general_switch(data):           
    DataLogger.LOG_TO_FILE = DataLogger.parse_to_bool(data.get(GENERAL_LOG_TO_FILE))
    DataLogger.DEFAULT_FILE_PATH = data.get(GENERAL_PATH_TO_FILE)

def xively_switch(data):
    #TODO: write code for xively handling
    
    # = data.get(XIVELY_ACTIVE)
    # = data.get(XIVELY_AGENT_DESCRIPTION)
    # = data.get(XIVELY_FEED)
    # = data.get(XIVELY_API_KEY)
    # = DataLogger.parse_to_int(data.get(XIVELY_UPDATE_RATE))
    pass

def bricklet_switch(data):

    for current_bricklet in data:
        bricklet_name = current_bricklet.name
        bricklet_uid = current_bricklet.uid
        bricklet_variables = current_bricklet.variables
        
        if (bricklet_name == AMBIENT_LIGHT ):
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
            logging.warning("The bricklet [" +bricklet_name+ "] is not yet supported")                     

def __exit_condition():
    '''
    Waits for an 'exit' or 'quit' to stop logging and close the program
    '''
    # TODO: Need another exit condition for the brickv GUI
    input_option = ""
    while (True):
        input_option = raw_input("Type 'quit' or 'exit' to stop logging and close the program\n")  # Use input() in Python 3
        if((input_option == "quit") or (input_option == "exit") ):
            break
              
def main(ini_file_path):
    if DataLogger.FILE_EVENT_LOGGING:
        logging.basicConfig(filename=DataLogger.EVENT_LOGGING_FILE_PATH,format='%(asctime)s - %(levelname)8s - %(message)s',level=DataLogger.LOGGING_EVENT_LEVEL)  
    else:
        logging.basicConfig(format="%(asctime)s - %(levelname)8s - %(message)s",level=DataLogger.LOGGING_EVENT_LEVEL)  
    
    logging.debug("data_logger.main main->ini_file_path: "+ ini_file_path)
    # exit if the path to the configuration file is invalid
    if (ini_file_path == "None"):
        logging.critical("No config.ini file found!")
        sys.exit(-1) 
        
    '''Parse configuration file'''
    configFile = DataLoggerConfig(ini_file_path);
    configFile.read_config_file()
    
    """CREATE-CONNECTION-TO-BRICKD"""
    #open IPConnection    
    DataLogger.ipcon = IPConnection()
  
    DataLogger.ipcon.connect(DataLogger.host, DataLogger.port)  # Connect to brickd
    logging.info("Connection to " + DataLogger.host + ":" + str(DataLogger.port) + " established.")
    # Don't use device before ipcon is connected
    
    general_switch(configFile.get_general_section())
    xively_switch(configFile.get_xively_section())      
    bricklet_switch(configFile.get_bricklets())    
    
    """START-WRITE-THREAD"""       
    #create write thread
    DataLogger.Threads.append(threading.Thread(name="CSV Writer Thread", target=writer_thread))
    for t in DataLogger.Threads:
        t.start()
    logging.debug("Work Threads started.")    
    
    """START-TIMERS"""
    for t in LoggerTimer.Timers:
        t.start()
    logging.debug("Get-Timers started.")  
      
    """END_CONDITIONS"""
    __exit_condition()
    
    """CLEANUP_AFTER_STOP """
    #set EXIT_FLAG for Get-Timers
    LoggerTimer.EXIT_FLAG = True
    #check if all timers stopped
    for t in LoggerTimer.Timers:
        t.join()    
    logging.debug("Get-Timers stopped.")
    
    #set THREAD_EXIT_FLAG for all work threads
    DataLogger.THREAD_EXIT_FLAG = True
    #wait for all threads to stop
    for th in  DataLogger.Threads:
        th.join()    
    logging.debug("Work Threads stopped.")
    
    DataLogger.ipcon.disconnect()
    logging.info("Connection closed successfully.")
    
    #TODO: delet this!
#     logging.debug("Level 10")          #Detailed information, typically of interest only when diagnosing problems.
#     logging.info("Level 20"            #Confirmation that things are working as expected.
#     logging.warn("Level 30")           #An indication that something unexpected happened, or indicative of some problem in the near future (e.g. disk space low). The software is still working as expected.     
#     logging.warning("Level 30")        #Use warning instead of warn
#     logging.error("Level 40")          #Due to a more serious problem, the software has not been able to perform some function.
#     logging.exception("Level 40")      #DO NOT USE! OR ONLY FOR EXCEPTIONS!
#     logging.critical("Level 50")       #A serious error, indicating that the program itself may be unable to continue running.

def command_line_start(argv,program_name):
    cl_parser = argparse.ArgumentParser(description=' -c <config-file>')
    
    cl_parser.add_argument('-c', action="store", dest="config_file", default="None", help="Path to the configuration file")
    results = cl_parser.parse_args(argv)

    return results.config_file


from tinkerforge.ip_connection import IPConnection
###main###
if __name__ == '__main__':      
    ini_file_path = command_line_start(sys.argv[1:], sys.argv[0]) 
    main(ini_file_path)
