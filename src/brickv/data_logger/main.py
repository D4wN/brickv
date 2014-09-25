#MAIN DATA_LOGGER PROGRAMM
from brickv.data_logger.bricklets import *

from brickv.data_logger.utils import ConfigurationReader, DataLoggerException
from brickv.data_logger.data_logger import DataLogger

import argparse                             # command line argument parser
import sys
#import logging                              #static logging system

""" 
- __main__
- brickv entry point
- switch-cases

"""
###switch###       
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
          
def main(ini_file_path):
    configuration = None
    try:
        configuration = ConfigurationReader(ini_file_path)
    except IOError as io_err:
        logging.critical("The parsing of the configuration file failed :" + str(io_err) )
        sys.exit(DataLoggerException.DL_CRITICAL_ERROR)

    data_logger = DataLogger(configuration._configuration)
    data_logger.run()
    
    __exit_condition(data_logger)
   
def command_line_start(argv,program_name):
    '''
    This function processes the command line arguments, if it was started via the console.
    '''
    cl_parser = argparse.ArgumentParser(description=' -c <config-file>')
    
    cl_parser.add_argument('-c', action="store", dest="config_file", default="None", help="Path to the configuration file")
    results = cl_parser.parse_args(argv)

    return results.config_file


from tinkerforge.ip_connection import IPConnection
###main###
if __name__ == '__main__':      
    ini_file_path = command_line_start(sys.argv[1:], sys.argv[0]) 
    main(ini_file_path)
