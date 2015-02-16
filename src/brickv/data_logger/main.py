#MAIN DATA_LOGGER PROGRAMM
from brickv.data_logger.loggable_devices import *

from brickv.data_logger.utils import DataLoggerException
from brickv.data_logger.configuration_validator import ConfigurationReader, ConfigurationValidator
from brickv.data_logger.event_logger import  EventLogger, ConsoleLogger, FileLogger, GUILogger
from brickv.data_logger.data_logger import DataLogger

import argparse                             # command line argument parser
import sys
import signal
import threading

# HashMap keywords to store results of the command line arguments 
CONSOLE_CONFIG_FILE = "config_file"
GUI_CONFIG = "configuration"
CONSOLE_VALIDATE_ONLY ="validate"
CONSOLE_START = False
CLOSE = False

def __exit_condition(data_logger):
    '''
    Waits for an 'exit' or 'quit' to stop logging and close the program
    '''
    try:
        while True:
            raw_input("") # FIXME: is raw_input the right approach 
            if CLOSE:
                raise KeyboardInterrupt()
            
    except (KeyboardInterrupt,EOFError):
        sys.stdin.close();
        data_logger.stop()
     
def signal_handler(signum, frame):
    '''
    This function handles the ctrl + c exit condition
    if it's raised through the console
    '''
    main.CLOSE = True

signal.signal(signal.SIGINT, signal_handler)
      
def main(arguments_map):
    '''
    This function initialize the data logger and starts the logging process
    '''
    #initiate the EventLogger
    EventLogger.add_logger(ConsoleLogger("ConsoleLogger", EventLogger.EVENT_LOG_LEVEL))
    
    if EventLogger.EVENT_FILE_LOGGING:
        EventLogger.add_logger(FileLogger("FileLogger", EventLogger.EVENT_LOG_LEVEL, EventLogger.EVENT_FILE_LOGGING_PATH))
    
    
    configuration = None
    guiStart = False
    try:
        if arguments_map.has_key(CONSOLE_CONFIG_FILE) and arguments_map[CONSOLE_CONFIG_FILE] != None:
            # was started via console
            configuration = ConfigurationReader(name=arguments_map[CONSOLE_CONFIG_FILE])
            
        elif arguments_map.has_key(GUI_CONFIG) and arguments_map[GUI_CONFIG] != None:
            # was started via gui
            configuration = ConfigurationReader(configuration=arguments_map[GUI_CONFIG])
            guiStart = True
            
            validator = ConfigurationValidator(configuration._configuration)
            validator.validate()
        else:
            # no configuration file was given
            EventLogger.critical("Can not run data logger without a configuration.")
            return
            
        if arguments_map.has_key(CONSOLE_VALIDATE_ONLY) and arguments_map[CONSOLE_VALIDATE_ONLY]:
            return
        
    except IOError as io_err:
        EventLogger.critical("The parsing of the configuration file failed :" + str(io_err) )
        sys.exit(DataLoggerException.DL_CRITICAL_ERROR)

    data_logger = DataLogger(configuration._configuration)       
    try:
        if data_logger.ipcon != None:
            data_logger.run()
            if not guiStart:
                __exit_condition(data_logger)
        else:
            EventLogger.error("DataLogger did not start logging process! Please check for errors.")
    except Exception:
        pass
    
    return data_logger
    
def command_line_start(argv,program_name):
    '''
    This function processes the command line arguments, if it was started via the console.
    '''
    main.CONSOLE_START = True
    cl_parser = argparse.ArgumentParser(description='Tinkerforge Data Logger')
    
    cl_parser.add_argument('config_file', help="Path to the configuration file")
    cl_parser.add_argument('-v', action="store_true", dest="validate", help="Just process the validation of the configuration file")
    
    results = cl_parser.parse_args(argv)
    
    arguments_map = {}
    arguments_map[CONSOLE_CONFIG_FILE] = results.config_file
    arguments_map[CONSOLE_VALIDATE_ONLY] = results.validate
    
    return arguments_map


from tinkerforge.ip_connection import IPConnection
###main###
if __name__ == '__main__':      
    arguments_map = command_line_start(sys.argv[1:], sys.argv[0]) 
    main(arguments_map)