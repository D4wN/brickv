
'''
/*---------------------------------------------------------------------------
                                ConfigurationReader
 ---------------------------------------------------------------------------*/
 '''
import codecs  # ConfigurationReader to read the file in correct encoding
import json
import re

from brickv.data_logger.event_logger import EventLogger
from brickv.data_logger.utils import DataLoggerException
import loggable_devices


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

    def __init__(self, pathToConfig=None, configuration=None):
        '''
        pathToConfig -- path to the json configuration file
        OR
        configuration -- the configuration itself
        '''
        self._configuration = Configuration()
        self._readConfigErr = 0  # Errors which occure during readin
        
        if pathToConfig is None and configuration is None:
            EventLogger.critical("ConfigurationReader needs a path to the configuration file or an actual configuration")
            return
        
        if pathToConfig is not None:
            self.filenName = pathToConfig
            self._read_json_config_file()
            
        if configuration is not None:
            if isinstance(configuration, Configuration):
                self._configuration = configuration
            else:
                self.map_dict_to_config(configuration)
                        
        validator = ConfigurationValidator(self._configuration)
        validator._error_count += self._readConfigErr
        validator.validate()
        
        
    def _read_json_config_file(self):
        with codecs.open(self.filenName, 'r', 'UTF-8') as content_file:
            try:
                json_structure = json.load(content_file)
            except ValueError as e:
                EventLogger.critical("Cant parse the configuration file: " + str(e))
                return
        
        # Load sections out of the json structure
        try:
            self._configuration._general = json_structure[ConfigurationReader.GENERAL_SECTION]
        except KeyError:
            EventLogger.critical("json configuration file has no [" + ConfigurationReader.GENERAL_SECTION + "] section")
            self._readConfigErr += 1
            
        self._configuration._xively = prevent_key_error(json_structure, ConfigurationReader.XIVELY_SECTION)
        self._configuration._simple_devices = prevent_key_error(json_structure, loggable_devices.Identifier.SIMPLE_DEVICE)
        self._configuration._complex_devices = prevent_key_error(json_structure, loggable_devices.Identifier.COMPLEX_DEVICE)
        self._configuration._special_devices = prevent_key_error(json_structure, loggable_devices.Identifier.SPECIAL_DEVICE)
    
    def map_dict_to_config(self, json_dict):
        self._configuration._general = prevent_key_error(json_dict, ConfigurationReader.GENERAL_SECTION)
        self._configuration._xively = prevent_key_error(json_dict, ConfigurationReader.XIVELY_SECTION)
                
        self._configuration._simple_devices = prevent_key_error(json_dict, loggable_devices.Identifier.SIMPLE_DEVICE)
        self._configuration._special_devices = prevent_key_error(json_dict, loggable_devices.Identifier.SPECIAL_DEVICE)
        self._configuration._complex_devices = prevent_key_error(json_dict, loggable_devices.Identifier.COMPLEX_DEVICE)

""""
/*---------------------------------------------------------------------------
                                ConfigurationValidator
 ---------------------------------------------------------------------------*/
"""

class ConfigurationValidator(object):
    '''
    This class validates the (json) configuration file
    '''
    MIN_INTERVAL = 1000
    
    def __init__(self, config_file):
        self.CR = ConfigurationReader  # alias for the ConfigurationReader
        self.ldi = loggable_devices.Identifier  # alias for the loggable_devices.Identifier
        
        self.json_config = config_file
   
        self._error_count = 0
        file_count = self.json_config._general[self.CR.GENERAL_LOG_COUNT]
        file_size = self.json_config._general[self.CR.GENERAL_LOG_FILE_SIZE]
         
        self._log_space_counter = LogSpaceCounter(file_count, file_size)
                
        
    def validate(self):
        '''
        This function performs the validation of the various sections of the json
        configuration file
        '''
        EventLogger.info("Started configuration file validation")
        
        self.validate_general_section()
        self.validate_xively_section()
        
        self.validate_simple_devices()
        self.validate_special_devices()
        self.validate_complex_devices()
        
        EventLogger.info("Validation ends with [" + str(self._error_count) + "] errors")

        logging_time = self._log_space_counter.calculate_time()
        EventLogger.info("Logging time until old data will be overwritten.")
        EventLogger.info("Days: " + str(logging_time[0]) + 
                        " Hours: " + str(logging_time[1]) + 
                        " Minutes: " + str(logging_time[2]) + 
                        " Seconds: " + str(logging_time[3]))
        EventLogger.info("About " + str(int(self._log_space_counter.lines_per_second + 0.5)) + " lines per second.")

        if self._error_count != 0:
            raise DataLoggerException(DataLoggerException.DL_FAILED_VALIDATION, "Validation process found some errors")
        
    def validate_general_section(self):
        '''
        This function validates the general section out of the configuration
        '''
        global_section = self.json_config._general
        
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
        host = global_section[self.CR.GENERAL_HOST]
        if not host.lower() == 'localhost' and not is_valid_ip_format(host):
            EventLogger.critical(self._generate_error_message(tier_array=[self.CR.GENERAL_SECTION, self.CR.GENERAL_HOST],
                                                msg="host should be 'localhost' or an valid ip-address"))
        
        # ConfigurationReader.GENERAL_PORT port number
        port = global_section[self.CR.GENERAL_PORT]
        if not self._is_valid_string(port, 1) and not(port > 0 and port <= 65535):
            EventLogger.critical(self._generate_error_message(tier_array=[self.CR.GENERAL_SECTION, self.CR.GENERAL_PORT], msg="port should be an integer 0-65535"))
        
        # ConfigurationReader.GENERAL_LOG_TO_FILE
        if not type(global_section[self.CR.GENERAL_LOG_TO_FILE]) == bool:
            EventLogger.critical(self._generate_error_message(tier_array=[self.CR.GENERAL_SECTION, self.CR.GENERAL_LOG_TO_FILE], msg="should be a boolean"))

        # ConfigurationReader.GENERAL_PATH_TO_FILE
        if not self._is_valid_string(global_section[self.CR.GENERAL_PATH_TO_FILE], 1):
            EventLogger.critical(self._generate_error_message(tier_array=[self.CR.GENERAL_SECTION, self.CR.GENERAL_PATH_TO_FILE], msg="should be a path to the file where the data will be saved"))
         
        # ConfigurationReader.GENERAL_LOG_COUNT and GENERAL_LOG_FILE_SIZE
        count = global_section[self.CR.GENERAL_LOG_COUNT]
        if not isinstance(count, int) and (not isinstance(count, float)):
            EventLogger.critical(self._generate_error_message(tier_array=[self.CR.GENERAL_SECTION, self.CR.GENERAL_LOG_COUNT], msg="should be a int or float"))
        size = global_section[self.CR.GENERAL_LOG_FILE_SIZE]
        if not isinstance(size, int) and (not isinstance(size, float)):
            EventLogger.critical(self._generate_error_message(tier_array=[self.CR.GENERAL_SECTION, self.CR.GENERAL_LOG_FILE_SIZE], msg="should be a int or float"))
         
        # TODO: Check free disk space of the destination
        
    def validate_xively_section(self):
        '''
        This function validates the xively section out of the configuration
        '''
        # TODO: implement xively section validation
        # xively_section = self.json_config._xively
        EventLogger.info("Xively validation is not yet supported")
        pass
    
    def validate_simple_devices(self):
        '''
        This function validates all devices from the configuration file which are of type 'SimpleDevice'
        '''
        devices = self.json_config._simple_devices
        self._replace_str_with_class(devices)
        
        for i in range(len(devices)):
            device = devices[i]
            self._check_basic_data(device)
            
            try:
                values = device[self.ldi.DEVICE_VALUES]
                for value in values:
                    self._check_basic_variables(device, values, value)
                    # log space calculation
                    self._log_space_counter.simple_devices(values[value][self.ldi.DEVICE_VALUES_INTERVAL])
                           
            except KeyError as k:
                EventLogger.critical(self._generate_error_message(device=device,
                                                                  tier_array=["values", value],
                                                                  msg="device has no key " + str(k)))
                
    def validate_special_devices(self):
        '''
        This function validates all devices from the configuration file which are of type 'SpecialDevices'.
        Every special device has its own implementation without an super class.
        '''
        devices = self.json_config._special_devices
        self._replace_str_with_class(devices)
        
        for i in range(len(devices)):
            device = devices[i]
            self._check_basic_data(device)
            
            try:
                # the two lists (device values, device booleans) should have the same length
                if len(device[self.ldi.SPECIAL_DEVICE_VALUE]) != len(device[self.ldi.SPECIAL_DEVICE_VALUE]):
                    EventLogger.critical(self._generate_error_message(device=device,
                                                                      tier_array=[self.ldi.SPECIAL_DEVICE_VALUE, self.ldi.SPECIAL_DEVICE_VALUE],
                                                                      msg="should have the same length"))
    
                # check types of the entities in the lists
                variables = device[self.ldi.SPECIAL_DEVICE_BOOL]
                variables_count = 0
                for bool_value_key in variables:
                    value = device[self.ldi.SPECIAL_DEVICE_BOOL][bool_value_key]
                    if not isinstance(value, bool):
                        EventLogger.critical(self._generate_error_message(device=device,
                                                                          tier_array=[self.ldi.SPECIAL_DEVICE_BOOL, bool_value_key],
                                                                          msg="is not a boolean"))
                    else:
                        if value is True:
                            variables_count += 1
          
                interval = device[self.ldi.SPECIAL_DEVICE_VALUE]
                interval_summ = 0
                for interval_value_key in interval:
                    interval_length = device[self.ldi.SPECIAL_DEVICE_VALUE][interval_value_key]
                    if not self._is_valid_interval(interval_length, min_value=ConfigurationValidator.MIN_INTERVAL):
                        EventLogger.critical(self._generate_error_message(device=device,
                                                                          tier_array=[self.ldi.SPECIAL_DEVICE_VALUE, interval_value_key],
                                                                          msg="interval (in milliseconds) should be an integer and at least " + str(ConfigurationValidator.MIN_INTERVAL)))
                    else:
                        interval_summ += interval_length
                        
                # log space calculation
                interval_summ /= len(interval)
                self._log_space_counter.special_devices(variables_count, interval_summ)
                
            except KeyError as k:
                EventLogger.critical(self._generate_error_message(device=device,
                                                                  tier_array=[""],
                                                                  msg="device has no key " + str(k)))
          
    def validate_complex_devices(self):
        '''
        This function validates all devices from the configuration file which are of type 'ComplexDevice'.
        '''
        devices = self.json_config._complex_devices
        self._replace_str_with_class(devices)
        
        for i in range(len(devices)):
            device = devices[i]
            self._check_basic_data(device)
            
            try:
                values = device[self.ldi.DEVICE_VALUES]
                for value in values:
                    self._check_basic_variables(device, values, value)
                    
                    if len(values[value][self.ldi.COMPLEX_DEVICE_VALUES_BOOL]) != len(values[value][self.ldi.COMPLEX_DEVICE_VALUES_NAME]):
                        EventLogger.critical(self._generate_error_message(device=device,
                                                                          tier_array=["values", value, self.ldi.COMPLEX_DEVICE_VALUES_BOOL, self.ldi.COMPLEX_DEVICE_VALUES_NAME],
                                                                          msg="should have the same length"))
                   
                    # loggable_devices.Identifier.COMPLEX_DEVICE_VALUES_BOOL
                    bool_values = values[value][self.ldi.COMPLEX_DEVICE_VALUES_BOOL]
                    for bool_value in bool_values:
                        if not isinstance(bool_value, bool):
                            EventLogger.critical(self._generate_error_message(device=device,
                                                                              tier_array=["values", value, self.ldi.COMPLEX_DEVICE_VALUES_BOOL, str(bool_value)],
                                                                              msg="should be a boolean"))
    
                    # loggable_devices.Identifier.COMPLEX_DEVICE_VALUES_NAME
                    string_values = values[value][self.ldi.COMPLEX_DEVICE_VALUES_NAME]
                    for string_value in string_values:
                        if not self._is_valid_string(string_value, 1):
                            EventLogger.critical(self._generate_error_message(device=device,
                                                                              tier_array=["values", value, self.ldi.COMPLEX_DEVICE_VALUES_NAME, str(bool_value)],
                                                                              msg="should be a string"))
                            
                    # log space calculation
                    interval = values[value][self.ldi.DEVICE_VALUES_INTERVAL]
                    self._log_space_counter.complex_devices(interval, bool_values)
                    
            except KeyError as k:
                EventLogger.critical(self._generate_error_message(device=device,
                                                                  tier_array=["values", value],
                                                                  msg="device has no key " + str(k)))
        
    def _replace_str_with_class(self, devices):
        '''
        This function replaces the entry 'loggable_devices.Identifier.DEVICE_CLASS' which contains
        the class name as a string with the actual class object
        '''
        class_str = ""
        for i in range(len(devices)):
            try:
                class_str = devices[i][self.ldi.DEVICE_CLASS]
                devices[i][self.ldi.DEVICE_CLASS] = loggable_devices.string_to_class(class_str)
                 
            except (KeyError, AttributeError):
                self._error_count += 1
                EventLogger.critical("Can not parse [" + class_str + "] to an actual class")

    def _check_basic_data(self, device):
        '''
        This function validates entries which are present in every device type
        '''
        try:
            # should be a class not a string
            if isinstance(device[self.ldi.DEVICE_CLASS], basestring):
                EventLogger.critical(self._generate_error_message(device=device,
                                                                  tier_array=[self.ldi.DEVICE_CLASS],
                                                                  msg="should be a class but is a string"))
                
            # should be a string with length > 0
            if not self._is_valid_string(device[self.ldi.DEVICE_NAME], min_length=1):
                EventLogger.critical(self._generate_error_message(device=device,
                                                                  tier_array=[self.ldi.DEVICE_NAME],
                                                                  msg="should be a string with length > 0"))
                
            # should be a string with length >= 3
            if not self._is_valid_string(device[self.ldi.DEVICE_UID], min_length=3):
                EventLogger.critical(self._generate_error_message(device=device,
                                                                  tier_array=[self.ldi.DEVICE_UID],
                                                                  msg="the UID should be a string with length >= 3"))
                
        except KeyError as k:
            EventLogger.critical(self._generate_error_message(device=device,
                                                              tier_array=[""],
                                                              msg="device has no key " + str(k)))
       
    def _check_basic_variables(self, device, values, value):
        '''
        This function checks entries which are present in the simple- and complex devices
        '''
        # loggable_devices.Identifier.DEVICE_VALUES_ARGS
        if not self._is_valid_arguments(values[value][self.ldi.DEVICE_VALUES_ARGS]):
                        EventLogger.critical(self._generate_error_message(device=device,
                                                                          tier_array=[str(value), self.ldi.DEVICE_VALUES_ARGS],
                                                                          msg="arguments should be either 'None' or a list with length >= 1 "))
        # loggable_devices.Identifier.DEVICE_VALUES_INTERVAL
        interval = values[value][self.ldi.DEVICE_VALUES_INTERVAL]
        if not self._is_valid_interval(interval, min_value=ConfigurationValidator.MIN_INTERVAL):
                        EventLogger.critical(self._generate_error_message(device=device,
                                                                          tier_array=[str(value), self.ldi.DEVICE_VALUES_INTERVAL],
                                                                          msg="interval (in milliseconds) should be an integer and at least " + str(ConfigurationValidator.MIN_INTERVAL)))
        
        # loggable_devices.Identifier.DEVICE_VALUES_NAME
        func_name = values[value][self.ldi.DEVICE_VALUES_NAME]
        class_object = device[self.ldi.DEVICE_CLASS]
        if not self._is_valid_function(class_object, func_name):
            tmp_msg = ""
            if isinstance(class_object, basestring):
                tmp_msg = "[" + str(class_object) + "] has no function \"" + func_name + "\""
            else:
                tmp_msg = "[" + class_object.__name__ + "] has no function \"" + func_name + "\""
                
            EventLogger.critical(self._generate_error_message(device=device,
                                                              tier_array=[str(value), self.ldi.DEVICE_VALUES_NAME],
                                                              msg=tmp_msg))
                        
    def _is_valid_string(self, string_value, min_length=0):
        '''
        Returns True if 'string_value' is of type basestring and has at least a size of
        'min_length'
        '''
        if not isinstance(string_value, basestring) or len(string_value) < min_length:
            return False
        return True
    
    def _is_valid_interval(self, integer_value, min_value=0):
        '''
        Returns True if the 'integer_value' is of type integer and is not negative
        '''
        if not isinstance(integer_value, int) or integer_value < min_value:
            return False
        return True
    
    def _is_valid_arguments(self, arg_value):
        '''
        Returns True if the 'arg_value' is 'None' or a list with at least one element
        '''
        if arg_value is None:
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
        if device is not None:
            err_msg = "[UID=" + str(device[self.ldi.DEVICE_UID]) + "]"
            
        for tier in tier_array:
            err_msg += "[" + tier + "]"
        
        self._error_count += 1
        return err_msg + " - " + msg
   
    
""""
/*---------------------------------------------------------------------------
                                LogSpaceCounter
 ---------------------------------------------------------------------------*/
"""
class LogSpaceCounter(object):
    '''
    This class provides functions to count the average lines per second
    in the log file
    '''
    def __init__(self, file_count, file_size):
        '''
        file_count -- the amount of logfiles
        file_size -- the size of each file
        '''
        self.file_count = file_count
        self.file_size = file_size
        
        self.lines_per_second = 0.0

    
    def simple_devices(self, interval):
        '''
        This function calculates the lines per second for simple devices and
        have to be called for every variable
        
        interval -- logging interval for a variable
        '''
        if interval == 0:
            return
        
        self.lines_per_second += 1000.0 / interval
    
    def special_devices(self, variables, interval):
        '''
        This function calculates the lines per second for special devices
        
        variables -- Amount of variables
        interval -- Sum of all interval
        '''
        if interval == 0:
            return
        
        self.lines_per_second += ((variables * 1000.0) / interval)
    
    def complex_devices(self, interval, bool_values):
        '''
            This function calculates the lines per second for complex devices
            countOfTrue / interval
            
            interval -- logging interval
            bool_values -- list with True/False values (Amount of True's equals to amount of loggable variables)
            
        '''
        if interval == 0:
            return
        
        variables = 0
        for entry in bool_values:
            if isinstance(entry, bool) and entry is True:
                variables += 1
        
        self.lines_per_second += ((variables * 1000.0) / interval)
                
    def calculate_time(self):
        '''
        This function calculates the time where the logger can
        save data without overwriting old ones.
        
        18k lines -> 1MB
        '''
        if self.lines_per_second <= 0:
            return 0, 0, 0, 0
        
        max_available_space = (self.file_count + 1) * ((self.file_size / 1024.0) / 1024.0)
        secondsForOneMB = 18000.0 / self.lines_per_second
        
        sec = secondsForOneMB * max_available_space * 1.0

        days = int(sec / 86400.0)
        sec -= 86400.0 * days

        hrs = int(sec / 3600.0)
        sec -= 3600.0 * hrs

        mins = int(sec / 60.0)
        sec -= 60.0 * mins
        
        return days, hrs, mins, int(sec)
        
                
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
      
    def isEmpty(self):
        return True if len(self._general) == 0 else False
 
def prevent_key_error(dict_src, key):
    '''
    This function returns an empty array if there is no such
    section in the configuration file
    key -- section key
    '''
    result = []
    try:
        result = dict_src[key]
    except KeyError:
        EventLogger.warning("json configuration file has no [" + key + "] section")
    return result
