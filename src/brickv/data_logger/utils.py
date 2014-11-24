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
from array import array
import threading, time, logging  # Writer Thread


'''
/*---------------------------------------------------------------------------
                                DataLoggerException
 ---------------------------------------------------------------------------*/
 '''     
class DataLoggerException(Exception):
    
    # Error Codes
    DL_MISSING_ARGUMENT = -1  # Missing Arguments in Config File
    DL_CRITICAL_ERROR = -42  # For all other critical errors
    # TODO: More specific error codes from our DataLogger
    
    def __init__(self, err_code, desc):
        self.value = err_code
        self.description = desc
    
    
    def __str__(self):
        return repr("ERROR[DL" + str(self.value) + "]: " + str(self.description))

'''
/*---------------------------------------------------------------------------
                                CSVData
 ---------------------------------------------------------------------------*/
 '''
import datetime  # CSV_Data

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
        ISO 8061 =  YYYY-MM-DDThh:mm:ss+tz:tz
                    2014-09-10T14:12:05+02:00
        """
        t = datetime.datetime.now()
        utc = self._time_utc_offset()
        utc_string = ""
        if utc < 0:
            utc *= -1
            utc_string = "-%02d:00" % (utc,)
        else:
            utc_string = "+%02d:00" % (utc,)
            
        self.timestamp = '{:%Y-%m-%dT%H:%M:%S}'.format(t)
        self.timestamp += utc_string
        
    
    def _time_utc_offset(self):
        if time.localtime(time.time()).tm_isdst and time.daylight:
            return -time.altzone / (60 * 60)
   
        return -time.timezone / (60 * 60)
    
    def __str__(self):
        """
        Simple Debug function for easier display of the object.
        """
        return "[UID=" + str(self.uid) + ";NAME=" + str(self.name) + ";VAR=" + str(self.var_name) + ";RAW=" + str(self.raw_data) + ";TIME=" + str(self.timestamp) + "]"


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
        interval /= 1000  # for ms
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
        if self._interval == 0:  # quick fix for no timer.start()
            return
        self._t.join();


'''
/*---------------------------------------------------------------------------
                                ConfigurationReader
 ---------------------------------------------------------------------------*/
 '''
import codecs  # ConfigurationReader to read the file in correct encoding
from ConfigParser import SafeConfigParser  # ConfigurationReader parser class
import json
import loggable_devices

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

    def __init__(self, name):
        self.filenName = name
        self._configuration = Configuration()
        
        self._read_json_config_file()   
           
        
    def _read_json_config_file(self):
        with codecs.open(self.filenName, 'r', 'UTF-8') as content_file:       
            json_structure = json.load(content_file)
    
        # Load sections out of the json structure 
        try:
            self._configuration._general = json_structure[ConfigurationReader.GENERAL_SECTION]
        except KeyError:
            EventLogger.warning("json configuration file has no [" + ConfigurationReader.GENERAL_SECTION + "] section")
            # TODO: Should end the program due to missing the general section
            
        
        def prevent_key_error(key):
            '''
            This function returns an empty array if there is no such  
            section in the configuration file
            key -- section key
            '''
            result = [] 
            try:
                result = json_structure[key]
            except KeyError:
                EventLogger.warning("json configuration file has no [" + key + "] section")
            return result
        
        self._configuration._xively = prevent_key_error(ConfigurationReader.XIVELY_SECTION)
        self._configuration._simple_devices = prevent_key_error(loggable_devices.Identifier.SIMPLE_DEVICE)
        self._configuration._complex_devices = prevent_key_error(loggable_devices.Identifier.COMPLEX_DEVICE)
        self._configuration._special_devices = prevent_key_error(loggable_devices.Identifier.SPECIAL_DEVICE)
                            
        validator = ConfigurationValidator(self._configuration)
        validator.validate()
                

""""
/*---------------------------------------------------------------------------
                                ConfigurationValidator
 ---------------------------------------------------------------------------*/
"""
import re

class ConfigurationValidator(object):
    '''
    This class validates the (json) configuration file
    '''
    def __init__(self, config_file):
        self.json_config = config_file
        self._error_count = 0
    
    
    def validate(self):
        '''
        This function performs the validation of the various sections of the json
        configuration file
        '''
        EventLogger.info("Started configuration file validation")
        
        self.validate_general_section(self.json_config._general)
        self.validate_xively_section(self.json_config._xively)
        
        self.validate_simple_devices(self.json_config._simple_devices)
        self.validate_special_devices(self.json_config._special_devices)
        self.validate_complex_devices(self.json_config._complex_devices)
        
        EventLogger.info("Validation ends with [" + str(self._error_count) + "] errors")
        
        if self._error_count != 0:
            # TODO: shutdown logger due to errors in the configuration file
            pass
    
    def validate_general_section(self, global_section):
        
        def is_valid_ip_format(ip_str):
            '''
            This function validates the format of an ip-address and returns true 
            on an valid and false on an invalid format.
            
            This function does not check if the ip-address makes any sense
            e.g '0.0.0.0' is a valid ip-address format
            '''
            # FIXME: Add IP6 pattern
            pattern = r"\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"
            if re.match(pattern, ip_str):
                return True
            else:
                return False
        
        # ConfigurationReader.GENERAL_HOST ip address
        host = global_section[ConfigurationReader.GENERAL_HOST] 
        if not host.lower() == 'localhost' and not is_valid_ip_format(host):
            EventLogger.critical(self._generate_error_message(tier_array=[ConfigurationReader.GENERAL_SECTION, ConfigurationReader.GENERAL_HOST], \
                                                msg="host should be 'localhost' or an valid ip-address"))
        
        # ConfigurationReader.GENERAL_PORT port number
        port = global_section[ConfigurationReader.GENERAL_PORT]
        if not self._is_valid_string(port, 1) and  not(port > 0 and port <= 65535):
            EventLogger.critical(self._generate_error_message(tier_array=[ConfigurationReader.GENERAL_SECTION, ConfigurationReader.GENERAL_PORT], \
                                                msg="port should be an integer 0-65535"))
        
        # ConfigurationReader.GENERAL_LOG_TO_FILE 
        if not type(global_section[ConfigurationReader.GENERAL_LOG_TO_FILE]) == bool:
            EventLogger.critical(self._generate_error_message(tier_array=[ConfigurationReader.GENERAL_SECTION, ConfigurationReader.GENERAL_LOG_TO_FILE], \
                                                msg="should be a boolean"))
        
        # ConfigurationReader.GENERAL_PATH_TO_FILE 
        if not self._is_valid_string(global_section[ConfigurationReader.GENERAL_PATH_TO_FILE], 1):
            EventLogger.critical(self._generate_error_message(tier_array=[ConfigurationReader.GENERAL_SECTION, ConfigurationReader.GENERAL_PATH_TO_FILE], \
                                                msg="should be a path to the file where the data will be saved"))
  
    def validate_xively_section(self, xively_section):
        # TODO: implement xively section validation
        EventLogger.info("Xively validation is not yet supported")
        pass
    
    def validate_simple_devices(self, devices):
        '''
        This function validates all devices from the configuration file which are of type 'SimpleDevice'
        '''
        self._replace_str_with_class(devices)
        
        for i in range(len(devices)):
            device = devices[i]
            self._check_basic_data(device)
            
            try:
                values = device[loggable_devices.Identifier.DEVICE_VALUES]
                for value in values:
                    self._check_basic_variables(device, values, value)
                        
            except KeyError as k:
                EventLogger.critical(self._generate_error_message(device=device, \
                                                                  tier_array=["values", value], \
                                                                  msg="device has no key " + str(k)))
                
    def validate_special_devices(self, devices):
        '''
        This function validates all devices from the configuration file which are of type 'SpecialDevices'.
        Every special device has its own implementation without an super class.
        '''
        self._replace_str_with_class(devices)
        
        for i in range(len(devices)):
            device = devices[i]
            self._check_basic_data(device)
            
            try:
                # the two lists (device values, device booleans) should have the same length
                if len(device[loggable_devices.Identifier.SPECIAL_DEVICE_VALUE]) != len(device[loggable_devices.Identifier.SPECIAL_DEVICE_VALUE]):
                    EventLogger.critical(self._generate_error_message(device=device, \
                                                        tier_array=[loggable_devices.Identifier.SPECIAL_DEVICE_VALUE, loggable_devices.Identifier.SPECIAL_DEVICE_VALUE ], \
                                                        msg="should have the same length"))
    
                # check types of the entities in the lists            
                for bool_value_key in device[loggable_devices.Identifier.SPECIAL_DEVICE_BOOL]:
                    if not isinstance(device[loggable_devices.Identifier.SPECIAL_DEVICE_BOOL][bool_value_key], bool):
                        EventLogger.critical(self._generate_error_message(device=device, \
                                                            tier_array=[loggable_devices.Identifier.SPECIAL_DEVICE_BOOL, bool_value_key], \
                                                            msg="is not a boolean"))
          
                for interval_value_key in device[loggable_devices.Identifier.SPECIAL_DEVICE_VALUE]:
                    if not self._is_valid_interval(device[loggable_devices.Identifier.SPECIAL_DEVICE_VALUE][interval_value_key]):
                        EventLogger.critical(self._generate_error_message(device=device, \
                                                            tier_array=[loggable_devices.Identifier.SPECIAL_DEVICE_VALUE, interval_value_key], \
                                                            msg="is not a valid interval"))
            except KeyError as k:
                EventLogger.critical(self._generate_error_message(device=device, \
                                                                  tier_array=[""], \
                                                                  msg="device has no key " + str(k)))
          
    def validate_complex_devices(self, devices):
        '''
        This function validates all devices from the configuration file which are of type 'ComplexDevice'.
        '''
        self._replace_str_with_class(devices)
        
        for i in range(len(devices)):
            device = devices[i]
            self._check_basic_data(device)
            
            try:
                values = device[loggable_devices.Identifier.DEVICE_VALUES]
                for value in values:
                    self._check_basic_variables(device, values, value)           
                    
                    if len(values[value][loggable_devices.Identifier.COMPLEX_DEVICE_VALUES_BOOL]) != \
                    len(values[value][loggable_devices.Identifier.COMPLEX_DEVICE_VALUES_NAME]):
                        EventLogger.critical(self._generate_error_message(device=device, \
                                                            tier_array=["values", value, loggable_devices.Identifier.COMPLEX_DEVICE_VALUES_BOOL, loggable_devices.Identifier.COMPLEX_DEVICE_VALUES_NAME], \
                                                            msg="should have the same length"))
                   
                    # loggable_devices.Identifier.COMPLEX_DEVICE_VALUES_BOOL
                    bool_values = values[value][loggable_devices.Identifier.COMPLEX_DEVICE_VALUES_BOOL]
                    for bool_value in bool_values:
                        if not isinstance(bool_value, bool):
                            EventLogger.critical(self._generate_error_message(device=device, \
                                                                tier_array=["values", value, loggable_devices.Identifier.COMPLEX_DEVICE_VALUES_BOOL, str(bool_value)], \
                                                                msg="should be a boolean"))
    
                    # loggable_devices.Identifier.COMPLEX_DEVICE_VALUES_NAME
                    string_values = values[value][loggable_devices.Identifier.COMPLEX_DEVICE_VALUES_NAME]
                    for string_value in string_values:
                        if not self._is_valid_string(string_value, 1):
                            EventLogger.critical(self._generate_error_message(device=device, \
                                                                tier_array=["values", value, loggable_devices.Identifier.COMPLEX_DEVICE_VALUES_NAME, str(bool_value)], \
                                                                msg="should be a string"))
            except KeyError as k:
                EventLogger.critical(self._generate_error_message(device=device, \
                                                                  tier_array=["values", value], \
                                                                  msg="device has no key " + str(k)))
    
    
    def _replace_str_with_class(self, devices):
        '''
        This function replaces the entry 'loggable_devices.Identifier.DEVICE_CLASS' which contains 
        the class name as a string with the actual class object
        '''
        class_str = ""
        for i in range(len(devices)):
            try:
                class_str = devices[i][loggable_devices.Identifier.DEVICE_CLASS]
                devices[i][loggable_devices.Identifier.DEVICE_CLASS] = loggable_devices.string_to_class(class_str) 
                 
            except (KeyError, AttributeError):
                self._error_count += 1
                EventLogger.critical("Can not parse [" + class_str + "] to an actual class")

    def _check_basic_data(self, device):
        '''
        This function validates entries which are present in every device type
        '''           
        try:    
            # should be a class not a string
            if isinstance(device[loggable_devices.Identifier.DEVICE_CLASS], basestring):
                EventLogger.critical(self._generate_error_message(device=device, \
                                                    tier_array=[loggable_devices.Identifier.DEVICE_CLASS], \
                                                    msg="should be a class but is a string"))
                
            # should be a string with length > 0
            if not self._is_valid_string(device[loggable_devices.Identifier.DEVICE_NAME]):
                EventLogger.critical(self._generate_error_message(device=device, \
                                                    tier_array=[loggable_devices.Identifier.DEVICE_NAME], \
                                                    msg="should be a string with length > 0"))
                
            # should be a string with length >= 3
            if not self._is_valid_string(device[loggable_devices.Identifier.DEVICE_UID]):
                EventLogger.critical(self._generate_error_message(device=device, \
                                                    tier_array=[loggable_devices.Identifier.DEVICE_UID], \
                                                    msg="should be a string with length > 0"))
                
        except KeyError as k:
            EventLogger.critical(self._generate_error_message(device=device, \
                                                              tier_array=[""], \
                                                              msg="device has no key " + str(k)))
       
    def _check_basic_variables(self, device, values, value):
        '''
        This function checks entries which are present in the simple- and complex devices
        '''
        # loggable_devices.Identifier.DEVICE_VALUES_ARGS
        if not self._is_valid_arguments(values[value][loggable_devices.Identifier.DEVICE_VALUES_ARGS]):  
                        EventLogger.critical(self._generate_error_message(device=device, \
                                                            tier_array=[str(value), loggable_devices.Identifier.DEVICE_VALUES_ARGS ], \
                                                            msg="arguments should be either 'None' or a list with length >= 1 "))
        # loggable_devices.Identifier.DEVICE_VALUES_INTERVAL
        if not self._is_valid_interval(values[value][loggable_devices.Identifier.DEVICE_VALUES_INTERVAL]):
                        EventLogger.critical(self._generate_error_message(device=device, \
                                                            tier_array=[str(value), loggable_devices.Identifier.DEVICE_VALUES_INTERVAL], \
                                                            msg="interval should be an integer and >= 0"))
        # loggable_devices.Identifier.DEVICE_VALUES_NAME                        
        func_name = values[value][loggable_devices.Identifier.DEVICE_VALUES_NAME]
        class_object = device[loggable_devices.Identifier.DEVICE_CLASS]
        if not self._is_valid_function(class_object, func_name):
                        EventLogger.critical(self._generate_error_message(device=device, \
                                                                          tier_array=[str(value), loggable_devices.Identifier.DEVICE_VALUES_NAME], \
                                                                          msg="[" + class_object.__name__ + "] has no function \"" + func_name + "\""))
                        
    def _is_valid_string(self, string_value, min_length=0):
        '''
        Returns True if 'string_value' is of type basestring and has at least a size of
        'min_length'
        '''
        if not isinstance(string_value, basestring) or len(string_value) < min_length :
            return False
        return True
    
    def _is_valid_interval(self, integer_value):
        '''
        Returns True if the 'integer_value' is of type integer and is not negative
        '''
        if not isinstance(integer_value, int) or integer_value < 0:
            return False
        return True
    
    def _is_valid_arguments(self, arg_value):
        '''
        Returns True if the 'arg_value' is 'None' or a list with at least one element
        '''
        if arg_value == None:
            return True
        elif isinstance(arg_value, list) and len(arg_value) >= 1:
            return True
        
        return False
     
    def _is_valid_function(self, class_obj, func_name):
        '''
        Returns True if the class 'class_obj' has an function wit the name 'func_name'
        '''
        return hasattr(class_obj, func_name)  
 
    def _generate_error_message(self, tier_array, msg, device=None):
        '''
        This function generates an error message which includes a error trace,
        so that the error can be quickly found in the actual configuration file
        '''
        err_msg = ""
        if device != None:
            err_msg = "[UID=" + str(device[loggable_devices.Identifier.DEVICE_UID]) + "]"
            
        for tier in tier_array:
            err_msg += "[" + tier + "]"
        
        self._error_count += 1
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
    
    # Logger Options
    EVENT_FILE_LOGGING = True  # for event logging in to a file
    EVENT_FILE_LOGGING_PATH = "data_logger.log"  # default file path for logging events TODO: enahcnment select file over commandline?
    EVENT_LOG_LEVEL = logging.DEBUG
    
    format = "%(asctime)s - %(levelname)8s - %(message)s"
    __loggers = {}
    
    def add_logger(logger):
        if logger.name == None or logger.name == "":
            raise Exception("Logger has no Attribute called 'name'!")

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
    
    
    # static methods
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
    '''
    This class outputs the logged events to the console
    '''
    
    def __init__(self, name, log_level):
        logging.Logger.__init__(self, name, log_level)
        
        # create console handler and set level
        ch = logging.StreamHandler()
        
        ch.setLevel(log_level)
        
        # create formatter
        formatter = logging.Formatter(EventLogger.format)
        
        # add formatter to ch
        ch.setFormatter(formatter)
        
        # add ch to logger
        self.addHandler(ch)

class FileLogger(logging.Logger):
    '''
    This class writes the logged events to an LOG file (EventLogger.EVENT_FILE_LOGGING_PATH)
    '''
    
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
        
        self.info("###### NEW LOGGING SESSION STARTED ######")

class GUILogger(logging.Logger):
    '''
    This class outputs the logged data to the brickv gui
    '''
    
    # for level as string
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
            # TODO: log to textfield
            print GUILogger._output_format.format(asctime=asctime, levelname=levelname, message=msg)      

"""
/*---------------------------------------------------------------------------
                                Utilities
 ---------------------------------------------------------------------------*/
"""
class Utilities(object):
    '''
    This class provides some utility functions for the data logger project
    '''
    
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
            EventLogger.debug("DataLogger.parse_to_int(" + string + ") could not be parsed! Return 0 for the Timer.")
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


'''
/*---------------------------------------------------------------------------
                                CSVWriter
 ---------------------------------------------------------------------------*/
 '''
import os  # CSV_Writer
import sys  # CSV_Writer
import csv  # CSV_Writer

class CSVWriter(object):
    '''
    This class provides the actual open/write functions, which are used by the CSVWriterJob class to write logged data into 
    a CSV formatted file.
    '''    
    
    def __init__(self, file_path):
        '''
        file_path = Path to the csv file
        ''' 
        self._file_path = file_path
        self._raw_file = None
        self._csv_file = None
        
        self._open_file_A()    
    
    def _open_file_A(self):
        """Opens a file in append mode."""

        # newline problem solved + import sys
        if sys.version_info >= (3, 0, 0):
            self._raw_file = open(self._file_path, 'a', newline='')
        else:
            self._raw_file = open(self._file_path, 'ab')
        
        self._csv_file = csv.writer(self._raw_file, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        # if the file is empty, create a csv header
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


""""
/*---------------------------------------------------------------------------
                                Jobs
 ---------------------------------------------------------------------------*/
"""
import Queue

class AbstractJob(threading.Thread):
    
    def __init__(self, datalogger=None, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target, name=name, args=args, kwargs=kwargs, verbose=verbose)
        self._exit_flag = False
        self._datalogger = datalogger
        self._job_name = "[Job:" + self.name + "]"
        
        if self._datalogger != None:
            self._datalogger.data_queue[self.name] = Queue.Queue()
    
    def stop(self):
        self._exit_flag = True
        try:
            self._datalogger.data_queue.pop(self.name)
        except KeyError as key_err:
            # TODO: key_err usen?
            pass
    
    def _job(self):
        # check for datalogger object
        if self._datalogger == None:
            EventLogger.warning(self.name + " started but did not get a DataLogger Object! No work could be done.")
            return True
        return False

    def _get_data_from_queue(self):
        if self._datalogger != None:
            return self._datalogger.data_queue[self.name].get()
        return None

class CSVWriterJob(AbstractJob):
    '''
    This class enables the data logger to write logged data to an CSV formatted file 
    '''    
    def __init__(self, datalogger=None, group=None, name="CSVWriterJob", args=(), kwargs=None, verbose=None):        
        target = self._job        
        AbstractJob.__init__(self, datalogger=datalogger, group=group, target=target, name=name, args=args, kwargs=kwargs, verbose=verbose)
        
    def _job(self):
        try:
            # check for datalogger object
            if AbstractJob._job(self):
                return
    
            EventLogger.debug(self._job_name + " Started")
            csv_writer = CSVWriter(self._datalogger.default_file_path)
                                   
            while (True):
                if not self._datalogger.data_queue[self.name].empty():
                    csv_data = self._get_data_from_queue()
                    EventLogger.debug(self._job_name + " -> " + str(csv_data))
                    if not csv_writer.write_data_row(csv_data):
                        EventLogger.warning(self._job_name + " Could not write csv row!")
                                              
                if not self._exit_flag and self._datalogger.data_queue[self.name].empty(): 
                    time.sleep(self._datalogger.job_sleep)
                
                if self._exit_flag and self._datalogger.data_queue[self.name].empty(): 
                    exit_return_Value = csv_writer.close_file()
                    if exit_return_Value:
                        EventLogger.debug(self._job_name + " Closed his csv_writer")
                    else:
                        EventLogger.debug(self._job_name + " Could NOT close his csv_writer! EXIT_RETURN_VALUE=" + str(exit))
                    EventLogger.debug(self._job_name + " Finished")
                    break
        except Exception as e:
            EventLogger.critical(self._job_name + " " + str(e))
            self.stop()
                      
class XivelyJob(AbstractJob):
    '''
    This class enables the data logger to upload logged data to the Xively platform
    '''
    
    def __init__(self, datalogger=None, group=None, name="XivelyJob", args=(), kwargs=None, verbose=None):        
        target = self._job        
        AbstractJob.__init__(self, datalogger=datalogger, group=group, target=target, name=name, args=args, kwargs=kwargs, verbose=verbose)
        # TODO: implement xively logger
        EventLogger.warning(self._job_name + " Is not supported!")
        
    def _job(self):
        # TODO: implement xively logger
        EventLogger.warning(self._job_name + " Is not supported!")
        try:
            # check for datalogger object
            if AbstractJob._job(self):
                return
    
            EventLogger.debug(self._job_name + " Started")
                                   
            while (True):
                if not self._datalogger.data_queue[self.name].empty():
                    # write
                    csv_data = self._get_data_from_queue()
                    EventLogger.debug(self._job_name + " -> " + str(csv_data))
                                              
                if not self._exit_flag and self._datalogger.data_queue[self.name].empty(): 
                    time.sleep(self._datalogger.job_sleep)
                
                if self._exit_flag and self._datalogger.data_queue[self.name].empty(): 
                    # close job
                    EventLogger.debug(self._job_name + " Finished")
                    break
        except Exception as e:
            EventLogger.critical(self._job_name + " " + str(e))
            self.stop()
            
