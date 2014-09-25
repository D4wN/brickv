# -*- coding: utf-8 -*-  
"""
brickv (Brick Viewer) 
Copyright (C) 2012, 2014 Roland Dudko  <roland.dudko@gmail.com>
Copyright (C) 2012, 2014 Marvin Lutz <marvin.lutz.mail@gmail.com>

data_logger_util.py: Util classes for the data logger

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License 
as published by the Free Software Foundation; either version 2 
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public
License along with this program; if not, write to the
Free Software Foundation, Inc., 59 Temple Place - Suite 330,
Boston, MA 02111-1307, USA.
"""
from lib2to3.fixer_util import String
from array import array
"""GLOBAL-VARIABLES"""

import threading, time, logging                               #Writer Thread


'''
/*---------------------------------------------------------------------------
                                DataLoggerException
 ---------------------------------------------------------------------------*/
 ''' 
    
class DataLoggerException(Exception):
    
    #Error Codes
    DL_MISSING_ARGUMENT = -1           #Missing Arguments in Config File
    DL_CRITICAL_ERROR = -42            # For all other critical errors
    #TODO: More specific error codes from our DataLogger
    
    def __init__(self, err_code, desc):
        self.value = err_code
        self.description = desc
    
    
    def __str__(self):
        return repr("ERROR[DL"+str(self.value)+"]: "+str(self.description))

'''
/*---------------------------------------------------------------------------
                                CSVData
 ---------------------------------------------------------------------------*/
 '''
import datetime #CSV_Data

class CSVData(object):
    '''
    This class is used as a temporary save spot for all csv relevant data.
    '''    
    
    def __init__(self, uid, name, var_name, raw_data):
        '''
        uid      -- uid of the bricklet
        name     -- DEVICE_IDENTIFIER of the bricklet
        var_name -- variable name of the logged value
        raw_data -- the logged value
        
        The timestamp is added automatically.
        '''        
        self.uid = uid
        self.name = name;
        self.var_name = var_name
        self.raw_data = raw_data
        self.timestamp = None
        self._set_timestamp()
        
        
    def _set_timestamp(self):
        """
        Adds a timestamp in ISO 8601 standard, with ms
        ISO 8061 =  YYYY-MM-DDThh:mm:ss
                    2014-09-10T14:12:05
        Python doees not support Timezones without extra libraries!
        """
        t = datetime.datetime.now();
        
        self.timestamp = '{:%Y-%m-%dT%H:%M:%S}'.format(t)
    
    def __str__(self):
        """
        Simple Debug function for easier display of the object.
        """
        return "UID =" + str(self.uid) + "\nNAME=" + str(self.name) + "\nVAR =" + str(self.var_name) + "\nRAW =" + str(self.raw_data) + "\nTIME=" + str(self.timestamp) + "\n"


'''
/*---------------------------------------------------------------------------
                                CSVWriter
 ---------------------------------------------------------------------------*/
 '''
import os #CSV_Writer
import sys #CSV_Writer
import csv #CSV_Writer

class CSVWriter(object):
    '''
    This class is used for writing a csv file.
    '''    
    
    def __init__(self, file_path):
        '''
        file_path = Path to the csv file
        ''' 
        self._file_path = file_path
        self._raw_file = None
        self._csv_file = None
        
        self._open_file_A()
        """
        1. Open File
        2. Check if File is empty
            2.a) If Empty, write the Header
        3. File is ready to be used
        4. Write Data Rows in File
        5. Close File
        """
    
    
    def _open_file_A(self):
        """Opens a file in append mode."""

        #newline problem solved + import sys
        if sys.version_info >= (3, 0, 0):
            self._raw_file = open(self._file_path, 'a', newline='')
        else:
            self._raw_file = open(self._file_path, 'ab')
        
        self._csv_file = csv.writer(self._raw_file, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        #if the file is empty, create a csv header
        if self._file_is_empty():
            self._write_header()

    def _file_is_empty(self):
        """
        Simple check if the file is empty.
        Return:
            True  - File is empty or missing
            False - File is not empty
        """
        try:
            if os.stat(self._file_path).st_size > 0:
                return False
            else:
                return True
        except OSError:
            return True

    def _write_header(self):
        """Writes a csv header into the file"""
        if(not self._file_is_empty()):
            logging.debug("File is not empty")
            return
    
        logging.debug("CSVWriter._write_header() - done")
        self._csv_file.writerow(["UID"] + ["DEVICE_IDENTIFIER"] + ["VAR"] + ["RAW"] + ["TIMESTAMP"])
        
    def write_data_row(self, csv_data):
        """
        Write a row into the csv file.
        Return:
            True  - Row was written into thee file
            False - Row was not written into the File
        """
        if self._raw_file == None or self._csv_file == None:
            return False
        
        self._csv_file.writerow([csv_data.uid] + [csv_data.name] + [csv_data.var_name] + [str(csv_data.raw_data)] + [csv_data.timestamp])        
        return True
    
    def set_file_path(self, new_file_path):
        """
        Sets a new file path.
        Return:
            True  - File path was updated and successfully opened
            False - File path could not be updated or opened
        """
        if self._file_path == new_file_path:
            return True
        
        if not self.close_file():
            return False
        
        self._file_path = new_file_path
        self._open_file_A()
        return True
                          
    def reopen_file(self):
        """
        Tries to reopen a file, if the file was manually closed.
        Return:
            True  - File could be reopened
            False - File could not be reopened
        """
        if self._raw_file != None and self._csv_file != None:
            return False
        
        self._open_file_A()        
        return True
    
    def close_file(self):
        """
        Tries to close the current file.
        Return:
            True  - File was close
            False - File could not be closed
        """
        if self._raw_file == None or self._csv_file == None:
            return False
        try:
            self._raw_file.close()
            self._csv_file = None
            self._raw_file = None
            return True
        
        except ValueError:
            return False


'''
/*---------------------------------------------------------------------------
                                LoggerTimer
 ---------------------------------------------------------------------------*/
 '''
from threading import Timer

class LoggerTimer(object):
    '''This class provides a timer with a repeat functionality based on a interval'''
        
    def __init__(self, interval, func_name, var_name, device):
        ''' 
        interval -- the repeat interval in ms
        func -- the function which will be called
        '''
        self.exit_flag = False
        interval /= 1000 #for ms
        if interval < 0:
            interval = 0
        
        self._interval = interval
        self._func_name = func_name     
        self._var_name = var_name 
        self._device = device
        self._t = Timer(self._interval, self._loop)
   
    
    def _loop(self):
        '''Runs the <self._func_name> function every <self._interval> seconds'''
        getattr(self._device, self._func_name)(self._var_name)
        self.cancel()
        if self.exit_flag:
            return
        self._t = Timer(self._interval, self._loop)
        self.start()
           
    def start(self):
        '''Starts the timer if <self._interval> is not 0 otherwise the 
           timer will be canceled 
        '''
        if self._interval == 0:
            self.cancel()
            return     
 
        self._t.start()
    
    def stop(self):
        self.exit_flag = True
    
    def cancel(self):
        self._t.cancel()
        
    def join(self):
        if self._interval == 0: #quick fix for no timer.start()
            return
        self._t.join();


'''
/*---------------------------------------------------------------------------
                                ConfigurationReader
 ---------------------------------------------------------------------------*/
 '''
import codecs # ConfigurationReader to read the file in correct encoding
from ConfigParser import SafeConfigParser # ConfigurationReader parser class
import json
import bricklets

class ConfigurationReader(object):
    '''
    This class provides the read-in functionality for the Data Logger configuration file
    '''   
    GENERAL_SECTION = "GENERAL"
    GENERAL_LOG_TO_FILE = "log_to_file"
    GENERAL_PATH_TO_FILE = "path_to_file"
    GENERAL_HOST = "host"
    GENERAL_PORT = "port"

    XIVELY_SECTION = "XIVELY"
    XIVELY_ACTIVE = "active"
    XIVELY_AGENT_DESCRIPTION = "agent_description"
    XIVELY_FEED = "feed"
    XIVELY_API_KEY = "api_key"
    XIVELY_UPLOAD_RATE = "upload_rate"
    
    __NAME_KEY = "name"
    __UID_KEY = "uid"

    def __init__(self,name):
        # TODO: Check the configuration file name
        self.filenName = name
        self._configuration = Configuration()
        
        self._read_json_config_file()   
           
        
    def _read_json_config_file(self):
        with open(self.filenName, 'r') as content_file:       
            json_structure = json.load(content_file)
    
        # Load sections out of the json structure 
        self._configuration._general = json_structure[ConfigurationReader.GENERAL_SECTION]
        self._configuration._xively = json_structure[ConfigurationReader.XIVELY_SECTION]
         
        self._configuration._simple_devices = json_structure[bricklets.SIMPLE_DEVICE]
        self._configuration._special_devices = json_structure[bricklets.SPECIAL_DEVICE]
        self._configuration._complex_devices = json_structure[bricklets.COMPLEX_DEVICE]
                
        validator = ConfigurationValidator(self._configuration)
        validator.validate()
                

""""
/*---------------------------------------------------------------------------
                                ConfigurationValidator
 ---------------------------------------------------------------------------*/
"""
class ConfigurationValidator(object):
    '''
    '''
    
    def __init__(self,config_file):
        self.json_config = config_file
    
    
    def validate(self):
        # TODO: validation general and xively
        self.validate_simple_devices(self.json_config._simple_devices)
        self.validate_special_devices(self.json_config._special_devices)
        self.validate_complex_devices(self.json_config._complex_devices)
    
    def validate_simple_devices(self,devices):
        self.__replace_str_with_class(devices)
        
        for i in range(len(devices)):
            device = devices[i]
            self.__check_basic_data(device)
            
            values = device[bricklets.DEVICE_VALUES]
            for value in values:
                # arguments should be be either none or a list with len > 0
                if not self.__is_valid_arguments(values[value][bricklets.DEVICE_VALUES_ARGS]):
                    print "arguments should be be either none or a list with len > 0 " \
                    + str(values[value][bricklets.DEVICE_VALUES_ARGS]) + " " + str(type(values[value][bricklets.DEVICE_VALUES_ARGS]))
                # interval should be an integer and >= 0
                if not self.__is_valid_interval(values[value][bricklets.DEVICE_VALUES_INTERVAL]):
                    print "function name should be a string and > 1"
                # function name should be a string and > 1
                if not self.__is_valid_string(values[value][bricklets.DEVICE_VALUES_NAME], 1):
                    print "function name should be a string and > 1"

    def validate_special_devices(self,devices):
        self.__replace_str_with_class(devices)
        
        for i in range(len(devices)):
            device = devices[i]
            self.__check_basic_data(device)
            
    
    def validate_complex_devices(self,devices):
        self.__replace_str_with_class(devices)
        
        for i in range(len(devices)):
            device = devices[i]
            self.__check_basic_data(device)
    
    
    def __replace_str_with_class(self,devices):
        for i in range(len(devices)):
            class_str = devices[i][bricklets.DEVICE_CLASS]
            devices[i][bricklets.DEVICE_CLASS] = bricklets.string_to_class(class_str)  
    
    def __check_basic_data(self,device):
        # TODO: Send error msg to user
        
        # should be a class not a string
        if isinstance(device[bricklets.DEVICE_CLASS],basestring):
            print "Error \"class\" is a string"
        # should be a string with length > 0
        if not self.__is_valid_string(device[bricklets.DEVICE_NAME]):
            print "Error \"name\" is not a string or too short"
        # should be a string with length >= 3
        if not self.__is_valid_string(device[bricklets.DEVICE_UID]):
            print "Error \"uid\" is not a string or too short"
        
    def __is_valid_string(self,string_value,min_length=0):
        if not isinstance(string_value, basestring) or len(string_value) < min_length :
            return False
        return True
    
    def __is_valid_interval(self,integer_value):
        if not isinstance(integer_value, int) or integer_value < 0:
            return False
        return True
    
    def __is_valid_arguments(self,arg_value):
        if arg_value == None:
            return True
        elif isinstance(arg_value, list) and len(arg_value) > 0:
            return True
        
        return False
    
""""
/*---------------------------------------------------------------------------
                                Configuration
 ---------------------------------------------------------------------------*/
"""
class Configuration():
    '''
    '''
    def __init__(self):
        self._general = {}
        self._xively = {}
        
        self._simple_devices = []
        self._complex_devices = []
        self._special_devices = []
        
     
""""
/*---------------------------------------------------------------------------
                                Utilities
 ---------------------------------------------------------------------------*/
"""
class Utilities(object):
    
    def parse_to_int(string):
        '''
        Returns an integer out of a string.
        0(Zero) -- if string is negative or an exception raised during the converting process.
        '''
        try:
            ret = int(float(string))
            if ret < 0:
                ret = 0
            return ret
        except ValueError:
            logging.debug("DataLogger.parse_to_int("+ string +") could not be parsed! Return 0 for the Timer.")
            return 0
    
    parse_to_int = staticmethod(parse_to_int) 

    def parse_to_bool(bool_string):
        '''
        Returns a 'True', if the string is equals to 'true' or 'True'.
        Otherwise it'll return a False
        '''
        if bool_string == "true" or bool_string == "True" or bool_string == "TRUE":
            return True
        else:
            return False
            
    parse_to_bool = staticmethod(parse_to_bool)       


""""
/*---------------------------------------------------------------------------
                                WriterThread
 ---------------------------------------------------------------------------*/
"""
import data_logger
def writer_thread(datalogger):
    thread_name = "Work Thread(" + threading.current_thread().name + ")"
    logging.debug(thread_name + " started.")
    csv_writer = CSVWriter(datalogger.default_file_path)
                           
    while (True):
        if not datalogger.data_queue.empty():
            csv_data = datalogger.data_queue.get()
            logging.debug(thread_name + " -> " + str(csv_data.name)+"-"+ csv_data.var_name +":" +str(csv_data.raw_data))
            if not csv_writer.write_data_row(csv_data):
                logging.warning(thread_name + " could not write csv row!")
                                      
        if not datalogger.thread_exit_flag and datalogger.data_queue.empty(): 
            #TODO: qucik testing fix logging.debug(thread_name + " has no work to do. Sleeping for "+ str(DataLogger.THREAD_SLEEP) +" seconds.")
            time.sleep(datalogger.thread_sleep)
        
        if datalogger.thread_exit_flag and datalogger.data_queue.empty(): 
            exit_flag = csv_writer.close_file()
            if exit_flag:
                logging.debug(thread_name + " closed his csv_writer.")
            else:
                logging.debug(thread_name + " could NOT close his csv_writer! EXIT_FLAG=" + str(exit))
            logging.debug(thread_name + " finished his work.")
            break
        
def xively_thread():
    pass
