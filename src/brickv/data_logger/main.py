# MAIN DATA_LOGGER PROGRAMM
import argparse  # command line argument parser
import os
import signal
import sys
import traceback

from brickv.data_logger.configuration_validator import ConfigurationReader
from brickv.data_logger.data_logger import DataLogger
from brickv.data_logger.event_logger import ConsoleLogger, FileLogger, EventLogger
from brickv.data_logger.utils import DataLoggerException


if hasattr(sys, "frozen"):
    program_path = os.path.dirname(os.path.realpath(unicode(sys.executable, sys.getfilesystemencoding())))

    if sys.platform == "darwin":
        resources_path = os.path.join(os.path.split(program_path)[0], 'Resources')
    else:
        resources_path = program_path
else:
    program_path = os.path.dirname(os.path.realpath(unicode(__file__, sys.getfilesystemencoding())))
    resources_path = program_path

# add program_path so OpenGL is properly imported
sys.path.insert(0, program_path)

# Allow brickv to be directly started by calling "main.py"
# without "brickv" being in the path already
if not 'brickv' in sys.modules:
    head, tail = os.path.split(program_path)

    if not head in sys.path:
        sys.path.insert(0, head)

    if not hasattr(sys, "frozen"):
        # load and inject in modules list, this allows to have the source in a
        # directory named differently than 'brickv'
        sys.modules['brickv'] = __import__(tail, globals(), locals(), [], -1)



# HashMap keywords to store results of the command line arguments
CONSOLE_CONFIG_FILE = "config_file"
GUI_CONFIG = "configuration"
CONSOLE_VALIDATE_ONLY = "validate"
CONSOLE_START = False
CLOSE = False

def __exit_condition(data_logger):
    '''
    Waits for an 'exit' or 'quit' to stop logging and close the program
    '''
    try:
        while True:
            raw_input("")  # FIXME: is raw_input the right approach
            if CLOSE:
                raise KeyboardInterrupt()
            
    except (KeyboardInterrupt, EOFError):
        sys.stdin.close()
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
    # output to console and file only if logger was not started via gui
    if not GUI_CONFIG in arguments_map:        
        # initiate the EventLogger
        EventLogger.add_logger(ConsoleLogger("ConsoleLogger", EventLogger.EVENT_LOG_LEVEL))
    
        if EventLogger.EVENT_FILE_LOGGING:
            EventLogger.add_logger(FileLogger("FileLogger", EventLogger.EVENT_LOG_LEVEL, EventLogger.EVENT_FILE_LOGGING_PATH))
     
    configuration = None
    guiStart = False
    try:
        # was started via console
        if CONSOLE_CONFIG_FILE in arguments_map and arguments_map[CONSOLE_CONFIG_FILE] is not None:
            configuration = ConfigurationReader(pathToConfig=arguments_map[CONSOLE_CONFIG_FILE])
         
        # was started via gui
        elif GUI_CONFIG in arguments_map and arguments_map[GUI_CONFIG] is not None:
            guiStart = True
            configuration = ConfigurationReader(configuration=arguments_map[GUI_CONFIG])

        # no configuration file was given
        else:
            raise DataLoggerException("Can not run data logger without a configuration.")
           
        if CONSOLE_VALIDATE_ONLY in arguments_map and arguments_map[CONSOLE_VALIDATE_ONLY]:
            return
        
    except Exception as exc:
        EventLogger.critical(str(exc))
        if guiStart:
            return None
        else:
            sys.exit(DataLoggerException.DL_CRITICAL_ERROR)
        
    if configuration._configuration.isEmpty():
        EventLogger.error("Configuration is empty")
        return None
        
    data_logger = None
    try:
        data_logger = DataLogger(configuration._configuration)
        if data_logger.ipcon is not None:
            data_logger.run()
            if not guiStart:
                __exit_condition(data_logger)
        else:
            raise DataLoggerException(DataLoggerException.DL_CRITICAL_ERROR, "DataLogger did not start logging process! Please check for errors.")
        
    except Exception as exc:
        EventLogger.critical(str(exc))
        traceback.print_exc(file=sys.stdout)
        if guiStart:
            return None
        else:
            sys.exit(DataLoggerException.DL_CRITICAL_ERROR)
    
    return data_logger
    
def command_line_start(argv, program_name):
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

###main###
if __name__ == '__main__':
    arguments_map = command_line_start(sys.argv[1:], sys.argv[0])
    main(arguments_map)
