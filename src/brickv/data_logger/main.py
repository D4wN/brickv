#MAIN DATA_LOGGER PROGRAMM
from brickv.data_logger.loggable_devices import *

from brickv.data_logger.utils import ConfigurationReader, DataLoggerException, EventLogger, ConsoleLogger, FileLogger, GUILogger,ConfigurationValidator
from brickv.data_logger.data_logger import DataLogger

import argparse                             # command line argument parser
import sys

# HashMap keywords to store results of the command line arguments 
CONSOLE_CONFIG_FILE = "config_file"
GUI_CONFIG = "configuration"
CONSOLE_VALIDATE_ONLY ="validate"
CONSOLE_START = False

def __exit_condition(data_logger):
    '''
    Waits for an 'exit' or 'quit' to stop logging and close the program
    '''
    # TODO: Need another exit condition for the brickv GUI
    input_option = ""
    while True:
        input_option = raw_input("Type 'quit' or 'exit' to stop logging and close the program\n")  # Use input() in Python 3
        if input_option == "quit" or input_option == "exit":
            break
    data_logger.stop(0)
          
def main(arguments_map):
    '''
    This function initialize the data logger and starts the logging process
    '''
    #initiate the EventLogger
    EventLogger.add_logger(ConsoleLogger("ConsoleLogger", EventLogger.EVENT_LOG_LEVEL))
    #TODO: re-enable with gui
    #EventLogger.add_logger(GUILogger("GUILogger", EventLogger.EVENT_LOG_LEVEL))
    if EventLogger.EVENT_FILE_LOGGING:
        EventLogger.add_logger(FileLogger("FileLogger", EventLogger.EVENT_LOG_LEVEL, EventLogger.EVENT_FILE_LOGGING_PATH))
    
    
    configuration = None
    try:
        if arguments_map.has_key(CONSOLE_CONFIG_FILE) and arguments_map[CONSOLE_CONFIG_FILE] != None:
            # was started via console
            configuration = ConfigurationReader(arguments_map[CONSOLE_CONFIG_FILE])
            
        elif arguments_map.has_key(GUI_CONFIG) and arguments_map[GUI_CONFIG] != None:
            # was started via gui
            configuration = arguments_map[GUI_CONFIG]
            
            validator = ConfigurationValidator(configuration)
            validator.validate()
        else:
            # no configuration file was given
            # FIXME: better description for the error message
            EventLogger.critical("Can not run data logger without a configuration.")
            return
            
        if arguments_map[CONSOLE_VALIDATE_ONLY]:
            return
        
    except IOError as io_err:
        EventLogger.critical("The parsing of the configuration file failed :" + str(io_err) )
        sys.exit(DataLoggerException.DL_CRITICAL_ERROR)


    data_logger = DataLogger(configuration._configuration)
    if data_logger.ipcon != None:
            data_logger.run()   
            __exit_condition(data_logger)
    else:
        EventLogger.error("DataLogger did not start logging process! Please check for errors.")
   
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
