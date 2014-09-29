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
        t = datetime.datetime.now()
        
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
            EventLogger.debug("File is not empty")
            return
    
        EventLogger.debug("CSVWriter._write_header() - done")
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
        self.filenName = name
        self._configuration = Configuration()
        
        self._read_json_config_file()   
           
        
    def _read_json_config_file(self):
        # TODO: is the UTF-8 encoding ok for json files
        with codecs.open(self.filenName, 'r', 'UTF-8') as content_file:       
            json_structure = json.load(content_file)
    
        # Load sections out of the json structure 
        self._configuration._general = json_structure[ConfigurationReader.GENERAL_SECTION]
        self._configuration._xively = json_structure[ConfigurationReader.XIVELY_SECTION]
         
        self._configuration._simple_devices = json_structure[bricklets.SIMPLE_DEVICE]
        self._configuration._complex_devices = json_structure[bricklets.COMPLEX_DEVICE]
        self._configuration._special_devices = json_structure[bricklets.SPECIAL_DEVICE]
                     
        validator = ConfigurationValidator(self._configuration)
        validator.validate()
                

""""
/*---------------------------------------------------------------------------
                                ConfigurationValidator
 ---------------------------------------------------------------------------*/
"""

class ConfigurationValidator(object):
    '''
    This class validates the (json) configuration file
    '''
    # TODO: Send error msg to user (replace the print)
    def __init__(self,config_file):
        self.json_config = config_file
    
    
    def validate(self):
        self.validate_general_section(self.json_config._general)
        self.validate_xively_section(self.json_config._xively)
        
        self.validate_simple_devices(self.json_config._simple_devices)
        self.validate_special_devices(self.json_config._special_devices)
        self.validate_complex_devices(self.json_config._complex_devices)
    
    def validate_general_section(self,global_section):
        pass
    
    def validate_xively_section(self,xively_section):
        pass
    
    def validate_simple_devices(self,devices):
        self.__replace_str_with_class(devices)
        
        for i in range(len(devices)):
            device = devices[i]
            self.__check_basic_data(device)
            
            values = device[bricklets.DEVICE_VALUES]
            for value in values:
                # arguments should be be either none or a list with len > 0
                if not self.__is_valid_arguments(values[value][bricklets.DEVICE_VALUES_ARGS]):                    
                    print self.__generate_error_message(device, [str(value),bricklets.DEVICE_VALUES_ARGS ], "arguments should be either 'None' or a list with length > 1 ")
                
                # interval should be an integer and >= 0
                if not self.__is_valid_interval(values[value][bricklets.DEVICE_VALUES_INTERVAL]):
                    print self.__generate_error_message(device,[str(value),bricklets.DEVICE_VALUES_INTERVAL],"interval should be an integer and >= 0")

                # function name should be a string and > 1
                if not self.__is_valid_string(values[value][bricklets.DEVICE_VALUES_NAME], 1):
                    print self.__generate_error_message(device,[str(value),bricklets.DEVICE_VALUES_NAME],"function name should be a string with a length > 1")

    def validate_special_devices(self,devices):
        self.__replace_str_with_class(devices)
        
        for i in range(len(devices)):
            device = devices[i]
            self.__check_basic_data(device)
            
            # the two lists (device values, device booleans) should have the same length
            if len(device[bricklets.SPECIAL_DEVICE_VALUE]) != len(device[bricklets.SPECIAL_DEVICE_VALUE]):
                print self.__generate_error_message(device,[bricklets.SPECIAL_DEVICE_VALUE,bricklets.SPECIAL_DEVICE_VALUE ],"should have the same length")

            # check types of the entities in the lists            
            for bool_value_key in device[bricklets.SPECIAL_DEVICE_BOOL]:
                if not isinstance(device[bricklets.SPECIAL_DEVICE_BOOL][bool_value_key], bool):
                    print self.__generate_error_message(device,[bricklets.SPECIAL_DEVICE_BOOL,bool_value_key], "is not a boolean" )
      
            for interval_value_key in device[bricklets.SPECIAL_DEVICE_VALUE]:
                if not self.__is_valid_interval(device[bricklets.SPECIAL_DEVICE_VALUE][interval_value_key]):
                    print self.__generate_error_message(device,[bricklets.SPECIAL_DEVICE_VALUE,interval_value_key],"is not a valid interval"  )
          
    def validate_complex_devices(self,devices):
        self.__replace_str_with_class(devices)
        
        for i in range(len(devices)):
            device = devices[i]
            self.__check_basic_data(device)
            
            values = device[bricklets.DEVICE_VALUES]
            for value in values:
                # arguments should be be either none or a list with len > 0
                if not self.__is_valid_arguments(values[value][bricklets.DEVICE_VALUES_ARGS]):
                    print self.__generate_error_message(device,[value,bricklets.DEVICE_VALUES_ARGS],"arguments should be be either 'None' or a list with len > 0"  )

                # interval should be an integer and >= 0
                if not self.__is_valid_interval(values[value][bricklets.DEVICE_VALUES_INTERVAL]):
                    print self.__generate_error_message(device,[value,bricklets.DEVICE_VALUES_INTERVAL],"interval should be an integer and >= 0"  )

                # function name should be a string and > 1   
                if not self.__is_valid_string(values[value][bricklets.DEVICE_VALUES_NAME], 1):
                    print self.__generate_error_message(device,[value,bricklets.DEVICE_VALUES_NAME],"function name should be a string and > 1"    )             
                
                # The two lists (var_bool, var_name) should have the same length   
                if len(values[value][bricklets.COMPLEX_DEVICE_VALUES_BOOL]) != len(values[value][bricklets.COMPLEX_DEVICE_VALUES_NAME]):
                    print self.__generate_error_message(device,[value,bricklets.COMPLEX_DEVICE_VALUES_BOOL,bricklets.COMPLEX_DEVICE_VALUES_NAME],"should have the same length")
               
     
                # check types of the entities in the lists  
                bool_values = values[value][bricklets.COMPLEX_DEVICE_VALUES_BOOL]
                for bool_value in bool_values:
                    if not isinstance(bool_value, bool):
                        print self.__generate_error_message(device,[value,bricklets.COMPLEX_DEVICE_VALUES_BOOL,str(bool_value)],"should be a boolean"   )

                string_values = values[value][bricklets.COMPLEX_DEVICE_VALUES_NAME]
                for string_value in string_values:
                    if not self.__is_valid_string(string_value, 1):
                        print self.__generate_error_message(device,[value,bricklets.COMPLEX_DEVICE_VALUES_NAME,str(bool_value)],"should be a string"   )  
    
    
    def __replace_str_with_class(self,devices):
        # FIXME: Should the exception be catched
        for i in range(len(devices)):
            class_str = devices[i][bricklets.DEVICE_CLASS]
            devices[i][bricklets.DEVICE_CLASS] = bricklets.string_to_class(class_str)  
    
    def __check_basic_data(self,device):                
        # should be a class not a string
        if isinstance(device[bricklets.DEVICE_CLASS],basestring):
            print self.__generate_error_message(device,[bricklets.DEVICE_CLASS],"should be a class but is a string"  )
            
        # should be a string with length > 0
        if not self.__is_valid_string(device[bricklets.DEVICE_NAME]):
            print self.__generate_error_message(device,[bricklets.DEVICE_NAME],"should be a string with length > 0"  )
            
        # should be a string with length >= 3
        if not self.__is_valid_string(device[bricklets.DEVICE_UID]):
            print self.__generate_error_message(device,[bricklets.DEVICE_UID],"should be a string with length > 0"  )

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
        elif isinstance(arg_value, list) and len(arg_value) >= 1:
            return True
        
        return False
    
    def __create_error_header(self,device):
        return "[UID=" + str(device[bricklets.DEVICE_UID]) + "]"
    
    def __generate_error_message(self,device,tier_array,msg):
        err_msg = "[UID=" + str(device[bricklets.DEVICE_UID]) + "]"
        for tier in tier_array:
            err_msg += "["+tier+"]"
        
        return err_msg + " - " + msg
        
          
""""
/*---------------------------------------------------------------------------
                                Configuration
 ---------------------------------------------------------------------------*/
"""
class Configuration():
    '''
    This class contains the information out of the json configuration file split by the 
    different categories/sections.
    '''
    def __init__(self):
        self._general = {}
        self._xively = {}
        
        self._simple_devices = []
        self._complex_devices = []
        self._special_devices = []
       
        
"""
/*---------------------------------------------------------------------------
                                Event Logger
 ---------------------------------------------------------------------------*/
"""    
class EventLogger():
    
    #Logger Options
    EVENT_FILE_LOGGING = False                              #for event logging in to a file
    EVENT_FILE_LOGGING_PATH = "data_logger.log"             #default file path for logging events TODO: enahcnment select file over commandline?
    EVENT_LOG_LEVEL = logging.DEBUG
    
    format = "%(asctime)s - %(levelname)8s - %(message)s"
    __loggers = {}
    
    def add_logger(logger):
        if logger.name == None or logger.name == "":
            raise Exception("Loggeer has no Attribute called 'name'!")

        EventLogger.__loggers[logger.name] = logger
    
    def remove_logger(logger_name):
        if EventLogger.__loggers.has_key(logger_name):
            EventLogger.__loggers.pop(logger_name)
            return True
        
        return False
    
    def debug(msg, logger_name=None):
        level = logging.DEBUG
        EventLogger._send_message(level, msg, logger_name)
        
    def info(msg, logger_name=None):
        level = logging.INFO
        EventLogger._send_message(level, msg, logger_name)
        
    def warn(msg, logger_name=None):
        level = logging.WARN
        EventLogger._send_message(level, msg, logger_name)
        
    def warning(msg, logger_name=None):
        level = logging.WARNING
        EventLogger._send_message(level, msg, logger_name)
        
    def error(msg, logger_name=None):
        level = logging.ERROR
        EventLogger._send_message(level, msg, logger_name)
        
    def critical(msg, logger_name=None):
        level = logging.CRITICAL
        EventLogger._send_message(level, msg, logger_name)
    
    def log(level, msg, logger_name=None):
        EventLogger._send_message(level, msg, logger_name)
    
    def _send_message(level, msg, logger_name):
        if logger_name != None:
            if EventLogger.__loggers.has_key(logger_name):
                EventLogger.__loggers[logger_name].log(level, msg)
        else:
            for logger in EventLogger.__loggers.values():
                logger.log(level, msg)
    
    
    #static methods
    add_logger = staticmethod(add_logger) 
    remove_logger = staticmethod(remove_logger)
    debug = staticmethod(debug) 
    info = staticmethod(info) 
    warn = staticmethod(warn) 
    warning = staticmethod(warning) 
    error = staticmethod(error) 
    critical = staticmethod(critical) 
    log = staticmethod(log) 
    _send_message = staticmethod(_send_message)
    
class ConsoleLogger(logging.Logger):
    
    def __init__(self, name, log_level):
        logging.Logger.__init__(self, name, log_level)
        
        #create console handler and set level
        ch = logging.StreamHandler()
        
        ch.setLevel(log_level)
        
        # create formatter
        formatter = logging.Formatter(EventLogger.format)
        
        # add formatter to ch
        ch.setFormatter(formatter)
        
        # add ch to logger
        self.addHandler(ch)

class FileLogger(logging.Logger):
    
    def __init__(self, name, log_level, filename):        
        logging.Logger.__init__(self, name, log_level)
        
        ch = logging.FileHandler(filename, mode="a")
        
        ch.setLevel(log_level)
        
        # create formatter
        formatter = logging.Formatter(EventLogger.format)
        
        # add formatter to ch
        ch.setFormatter(formatter)
        
        # add ch to logger
        self.addHandler(ch)

class GUILogger(logging.Logger):
    
    #for level as string
    _convert_level = {}
    _convert_level[logging.DEBUG] = "DEBUG"
    _convert_level[logging.INFO] = "INFO"
    _convert_level[logging.WARN] = "WARNING"
    _convert_level[logging.WARNING] = "WARNING"
    _convert_level[logging.CRITICAL] = "CRITIAL"
    _convert_level[logging.ERROR] = "ERROR"
    
    _output_format = "{asctime} - {levelname:8} - {message}s"
    
    def __init(self, name, log_level):        
        logging.Logger.__init__(self, name, log_level)
        
        
    def debug(self, msg):   
        self.log(logging.DEBUG, msg)
    
    def info(self, msg):              
        self.log(logging.INFO, msg)
        
    def warn(self, msg):              
        self.log(logging.WARN, msg)
        
    def warning(self, msg):              
        self.log(logging.WARNING, msg)
        
    def critical(self, msg):              
        self.log(logging.CRITICAL, msg)
    
    def error(self, msg):              
        self.log(logging.ERROR, msg)
            
    def log(self, level, msg):
        if level >= self.level:        
            asctime = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
            levelname = GUILogger._convert_level[level]
            #TODO: log to textfield
            print GUILogger._output_format.format(asctime=asctime, levelname=levelname, message=msg)      

"""
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
            EventLogger.debug("DataLogger.parse_to_int("+ string +") could not be parsed! Return 0 for the Timer.")
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
    EventLogger.debug(thread_name + " started.")
    csv_writer = CSVWriter(datalogger.default_file_path)
                           
    while (True):
        if not datalogger.data_queue.empty():
            csv_data = datalogger.data_queue.get()
            EventLogger.debug(thread_name + " -> " + str(csv_data.name)+"-"+ csv_data.var_name +":" +str(csv_data.raw_data))
            if not csv_writer.write_data_row(csv_data):
                EventLogger.warning(thread_name + " could not write csv row!")
                                      
        if not datalogger.thread_exit_flag and datalogger.data_queue.empty(): 
            #TODO: qucik testing fix EventLogger.debug(thread_name + " has no work to do. Sleeping for "+ str(DataLogger.THREAD_SLEEP) +" seconds.")
            time.sleep(datalogger.thread_sleep)
        
        if datalogger.thread_exit_flag and datalogger.data_queue.empty(): 
            exit_flag = csv_writer.close_file()
            if exit_flag:
                EventLogger.debug(thread_name + " closed his csv_writer.")
            else:
                EventLogger.debug(thread_name + " could NOT close his csv_writer! EXIT_FLAG=" + str(exit))
            EventLogger.debug(thread_name + " finished his work.")
            break
        
def xively_thread():
    # TODO: Xively writer implementation goes here
    pass
