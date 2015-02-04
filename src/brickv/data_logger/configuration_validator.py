
'''
/*---------------------------------------------------------------------------
                                ConfigurationReader
 ---------------------------------------------------------------------------*/
 '''
import codecs  # ConfigurationReader to read the file in correct encoding
import json
import loggable_devices
import os

from ConfigParser import SafeConfigParser  # ConfigurationReader parser class
from brickv.data_logger.event_logger import EventLogger
from lib2to3.fixer_util import String

class ConfigurationReader(object):
    '''
    This class provides the read-in functionality for the Data Logger configuration file
    '''   
    GENERAL_SECTION = "GENERAL"
    GENERAL_LOG_TO_FILE = "log_to_file"
    GENERAL_PATH_TO_FILE = "path_to_file"
    GENERAL_LOG_COUNT = "log_count"
    GENERAL_LOG_FILE_SIZE = "max_logged_file_size"
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
              
        # validates the configuration              
        validator = ConfigurationValidator(self._configuration)
        validator.validate()
                

""""
/*---------------------------------------------------------------------------
                                ConfigurationValidator
 ---------------------------------------------------------------------------*/
"""
import re
from  brickv.data_logger.utils import Utilities

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
       
        
