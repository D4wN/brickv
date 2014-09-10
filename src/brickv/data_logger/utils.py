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

"""GLOBAL-VARIABLES"""

import Queue, threading, time, logging                               #Writer Thread

class DataLogger():
    
    #Logger
    FILE_EVENT_LOGGING = False                              #for event logging in to a file
    EVENT_LOGGING_FILE_PATH = "data_logger.log"             #default file path for logging events TODO: enahcnment select file over commandline?
    LOGGING_EVENT_LEVEL = logging.DEBUG
    
    #General
    DEFAULT_FILE_PATH = "logged_data.csv"
    ipcon = None
    host = "localhost"
    port = 4223  
    
    #Queues
    Q = Queue.Queue()                                       #gloabl queue for write jobs
    
    #Thread things
    Threads = []                                            #gloabl thread array for all running threads/jobs
    THREAD_EXIT_FLAG = False                                #flag for stopping the thread   
    THREAD_SLEEP = 5                                        #in seconds!; fail state = -1 TODO: Enahncement -> use condition objects
    
    
    #Functions
    def parse_to_int(string):
        try:
            ret = int(float(string))
            if ret < 0:
                ret = 0
            return ret
        except ValueError:
            logging.debug("DataLogger.parse_to_int("+ string +") could not be parsed! Return 0 for the Timer.")
            return 0
    
    parse_to_int = staticmethod(parse_to_int) 



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
        name     -- name of the bricklet
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
        ISO 8061 = YYYY-MM-DD hh:mm:ss.msmsms
        """
        self.timestamp = datetime.datetime.now()
    
    def __str__(self):
        """
        Simple Debug function for easier display of the object.
        """
        return "UID =" + self.uid + "\nNAME=" + self.name + "\nVAR =" + self.var_name + "\nRAW =" + str(self.raw_data) + "\nTIME=" + str(self.timestamp) + "\n"


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
            return
    
        logging.debug("CSVWriter._write_header() - done")
        self._csv_file.writerow(["UID"] + ["NAME"] + ["VAR"] + ["RAW"] + ["TIMESTAMP"])
        
    def write_data_row(self, csv_data):
        """
        Write a row into the csv file.
        Return:
            True  - Row was written into thee file
            False - Row was not written into the File
        """
        if self._raw_file == None or self._csv_file == None:
            return False
        
        self._csv_file.writerow([csv_data.uid] + [csv_data.name] + [csv_data.var_name] + [csv_data.raw_data] + [csv_data.timestamp])        
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
    
    Timers = [] # global array for all running timers
    EXIT_FLAG = False
    
    def __init__(self, interval, func):
        ''' 
        interval -- the repeat interval in ms
        func -- the function which will be called
        '''
        interval /= 1000 #for ms
        if interval < 0:
            interval = 0
        
        self._interval = interval
        self._func = func      
        self._t = Timer(self._interval, self._loop)
   
    
    def _loop(self):
        '''Runs the <self._func> function every <self._interval> seconds'''
        self._func()
        self.cancel()
        if LoggerTimer.EXIT_FLAG:
            self._t.cancel()
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
    
    def cancel(self):
        self._t.cancel()
        
    def join(self):
        if self._interval == 0: #quick fix for no timer.start()
            return
        self._t.join();


'''
/*---------------------------------------------------------------------------
                                DataLoggerConfig
 ---------------------------------------------------------------------------*/
 '''
import codecs # DataLoggerConfig to read the file in correct encoding
from ConfigParser import SafeConfigParser # DataLoggerConfig parser class

class DataLoggerConfig(object):
    '''
    This class provides the read-in functionality for the Data Logger configuration file
    '''
    __GENERAL_SECTION = "GENERAL"
    __XIVELY_SECTION = "XIVELY"
    
    __NAME_KEY = "name"
    __UID_KEY = "uid"

    def __init__(self,name):
        self._is_parsed = False
        self.filenName = name
        self._general = {}
        self._xively = {}
        self._bricklets = []
                
        
    def _get_section_as_hashmap(self,section_name ,parser ):
        '''
        saves variables out of an (configuration file) section to a hashmap.
        key -- variable name
        value -- variable value
        '''
        hashMap = {}
        for section_key in parser.options(section_name):
            hashMap[section_key] =  parser.get(section_name, section_key)
        return hashMap
    

    def __parse_first(self):
        '''
        Checks if the configuration file is already parsed. If not it'll
        call the <read_config_file()> function
        '''   
        if(not self._is_parsed):
            self.read_config_file()
            
    def read_config_file(self):
        '''
        reads the entries out of the configuration file and 
        saves them into a <BrickletInfo> structure.
        
        Call sys.exit() if there are no bricklets configured            
        '''
        parser = SafeConfigParser()
        # Open the file with the correct encoding
        with codecs.open(self.filenName, 'r', encoding='utf-8') as f:
            parser.readfp(f)
      
        for section_name in parser.sections():
            if (section_name == self.__GENERAL_SECTION):
                # Get GENERAL section
                self.general =self._get_section_as_hashmap(section_name,parser)

            elif (section_name == self.__XIVELY_SECTION):
                # Get XIVELY section
                self.xively = self._get_section_as_hashmap(section_name,parser)

            else:
                # Get all other variables  
                bricklet_name = parser.get(section_name, self.__NAME_KEY)
                bricklet_uid =  parser.get(section_name, self.__UID_KEY)
                
                tmp_bricklet = BrickletInfo(bricklet_name,bricklet_uid)
                for section_key in parser.options(section_name):
                    if (section_key != self.__NAME_KEY and section_key != self.__UID_KEY):
                        # All variables (key and value) are of type string                     
                        tmp_bricklet.add_key_value_pair(str(section_key).title(),str(parser.get(section_name, section_key)).title() )

                self._bricklets.append(tmp_bricklet)
                
        # configuration file is parsed an ready to use     
        self._is_parsed = True
        
        # TODO: define error number for this exception
        if(len(self._bricklets) == 0):
            logging.error("There are no bricklets configured in the configuration file!")
            sys.exit(-1)  
        
    def get_general_section(self):
        '''
        Returns the variables out of the "GENERAL" section in the configuration file if it
        was already parsed otherwise it call the <read_config_file()> function first
        '''
        self.__parse_first()
           
        return self._general

    def get_xively_section(self):
        '''
        Returns the variables out of the "XIVELY" section in the configuration file if it
        was already parsed otherwise it call the <read_config_file()> function first
        '''
        self.__parse_first()
           
        return self._xively
        
    def get_bricklets(self):
        '''
        Returns an array of bricklets out of the configuration file if it
        was already parsed. Otherwise it call the <read_config_file()> function first
        '''
        self.__parse_first()
           
        return self._bricklets


""""
/*---------------------------------------------------------------------------
                                BrickletInfo
 ---------------------------------------------------------------------------*/
"""
class BrickletInfo(object):
    '''
    This class holds the information about an entry out of the configuration file
    '''
    
    def __init__(self, name, uid):
        self.name = name
        self.uid = uid
        self.variables = { }
   
        
    def add_key_value_pair(self, key, value):
        '''
        adds a key-value pair to the bricklet dictionary
        '''
        self.variables[key] = value
    

""""
/*---------------------------------------------------------------------------
                                WriterThread
 ---------------------------------------------------------------------------*/
"""


def writer_thread():
    thread_name = "Work Thread(" + threading.current_thread().name + ")"
    logging.debug(thread_name + " started.")
    csv_writer = CSVWriter(DataLogger.DEFAULT_FILE_PATH)
    
    while (True):
        if not DataLogger.Q.empty():
            csv_data = DataLogger.Q.get()
            logging.debug(thread_name + " -> " + str(csv_data.raw_data))
            if not csv_writer.write_data_row(csv_data):
                print logging.warning(thread_name + " could not write csv row!")
                                      
        if not DataLogger.THREAD_EXIT_FLAG and DataLogger.Q.empty(): 
            logging.debug(thread_name + " has no work to do. Sleeping for "+ str(DataLogger.THREAD_SLEEP) +" seconds.")
            time.sleep(DataLogger.THREAD_SLEEP)
        
        if DataLogger.THREAD_EXIT_FLAG and DataLogger.Q.empty(): 
            
            exit_flag = csv_writer.close_file()
            if exit_flag:
                logging.debug(thread_name + " closed his csv_writer.")
            else:
                logging.debug(thread_name + " could NOT close his csv_writer! EXIT_FLAG=" + str(exit))
            logging.debug(thread_name + " finished his work.")
            break