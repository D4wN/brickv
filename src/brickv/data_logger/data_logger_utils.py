# -*- coding: utf-8 -*-  
"""
brickv (Brick Viewer) 
Copyright (C) 2012, 2014 Roland Dudko  <roland.dudko@gmail.com>
Copyright (C) 2012, 2014 Marvin Lutz <>

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

""""CSV_Data"""
import datetime #CSV_Data

'''
/*---------------------------------------------------------------------------
                                CSVData
 ---------------------------------------------------------------------------*/
 '''
class CSVData(object):
    '''
    This class is used as a temporary save spot for all csv relevant data.
    '''    
    
    def __init__(self, uid, name, var_name, raw_data):
        '''
        uid      = uid of the bricklet
        name     = name of the bricklet
        var_name = variable name of the logged value
        raw_data = the logged value
        
        The timestamp is added automaticaly.
        '''        
        self.uid = uid
        self.name = name;
        self.var_name = var_name
        self.raw_data = raw_data
        self.timestamp = None
        self.__set_timestamp()
        
        
    def __set_timestamp(self):
        """
        Adds a timestamp in ISO 8601 standard, with ms
        ISO 8061 = YYYY-MM-DD hh:mm:ss.msmsms
        """
        self.timestamp = datetime.datetime.now()
    
    def to_string(self):
        """
        Simple Debug function for easier display of the object.
        """
        return "UID =" + self.uid + "\nNAME=" + self.name + "\nVAR =" + self.var_name + "\nRAW =" + str(self.raw_data) + "\nTIME=" + str(self.timestamp) + "\n"
    
""""CSV_Writer"""
import os #CSV_Writer
import sys #CSV_Writer
import csv #CSV_Writer

'''
/*---------------------------------------------------------------------------
                                CSVWriter
 ---------------------------------------------------------------------------*/
 '''
class CSVWriter(object):
    '''
    This class is used for writing a csv file.
    '''    
    
    def __init__(self, file_path):
        '''
        file_path = Path to the csv file
        ''' 
        self.__file_path = file_path
        self.__raw_file = None
        self.__csv_file = None
        
        self.__open_file_A()
        """
        1. Open File
        2. Check if File is empty
            2.a) If Empty, write the Header
        3. File is ready to be used
        4. Write Data Rows in File
        5. Close File
        """
    
    
    def __open_file_A(self):
        """Opens a file in append mode."""

        #newline problem solved + import sys
        if sys.version_info >= (3, 0, 0):
            self.__raw_file = open(self.__file_path, 'a', newline='')
        else:
            self.__raw_file = open(self.__file_path, 'ab')
        
        self.__csv_file = csv.writer(self.__raw_file, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        #if the file is empty, create a csv header
        if self.__file_is_empty():
            self.__write_header()

    def __file_is_empty(self):
        """
        Simple check if the file is empty.
        Return:
            True  - File is empty or missing
            False - File is not empty
        """
        try:
            if os.stat(self.__file_path).st_size > 0:
                return False
            else:
                return True
        except OSError:
            return True

    def __write_header(self):
        """Writes a csv header into the file"""
        if(not self.__file_is_empty()):
            return
    
        self.__csv_file.writerow(["UID"] + ["NAME"] + ["VAR"] + ["RAW"] + ["TIMESTAMP"])
        
    def write_data_row(self, csv_data):
        """
        Write a row into the csv file.
        Return:
            True  - Row was written into thee file
            False - Row was not written into the File
        """
        if self.__raw_file == None or self.__csv_file == None:
            return False
        
        self.__csv_file.writerow([csv_data.uid] + [csv_data.name] + [csv_data.var_name] + [csv_data.raw_data] + [csv_data.timestamp])        
        return True
    
    def set_file_path(self, new_file_path):
        """
        Sets a new file path.
        Return:
            True  - File path was updated and successfully opened
            False - File path could not be updated or opened
        """
        if self.__file_path == new_file_path:
            return True
        
        if not self.close_file():
            #print "CSV_Writer.set_file_path(" + new_file_path + ") failed!"
            return False
        
        self.__file_path = new_file_path
        self.__open_file_A()
        return True
                          
    def reopen_file(self):
        """
        Tries to reopen a file, if the file was manually closed.
        Return:
            True  - File could be reopened
            False - File could not be reopened
        """
        if self.__raw_file != None and self.__csv_file != None:
            return False
        
        self.__open_file_A()        
        return True
    
    def close_file(self):
        """
        Tries to close the current file.
        Return:
            True  - File was close
            False - File could not be closed
        """
        if self.__raw_file == None or self.__csv_file == None:
            return False
        try:
            self.__raw_file.close()
            self.__csv_file = None
            self.__raw_file = None
            return True
        
        except ValueError:
            return False

""""TODO: LoggerTimer"""
from threading import Timer

'''
/*---------------------------------------------------------------------------
                                LoggerTimer
 ---------------------------------------------------------------------------*/
 '''
class LoggerTimer(object):
    '''
    TODO: comment goes here
    '''
	Timers = [] # global array for all running timers
    
    def __init__(self, interval, func):
        ''' 
        interval -- the repeat interval in ms
        func -- the function which will be called
        '''
        interval /= 1000 #for ms
        if interval < 0:
            interval = 0
        
        self.__interval = interval
        self.__func = func      
        self.__t = Timer(self.__interval, self.__loop)
   
    
    def __loop(self):
        '''Runs the <self.__func> function every <self.__interval> seconds'''
        self.__func()
        self.cancel()
        self.__t = Timer(self.__interval, self.__loop)
        self.start()
           
    def start(self):
        '''Starts the timer if <self.__interval> is not 0 otherwise the 
           timer will be canceled 
        '''
        if self.__interval == 0:
            self.cancel()
            return     
 
        self.__t.start()
    
    def cancel(self):
        self.__t.cancel()
        
    def join(self):
        if self.__interval == 0: #quick fix for no timer.start()
            return
        self.__t.join();

""""TODO: INI-PARSER"""
import codecs # DataLoggerConfig to read the file in correct encoding
from ConfigParser import SafeConfigParser # DataLoggerConfig parser class

'''
/*---------------------------------------------------------------------------
                                DataLoggerConfig
 ---------------------------------------------------------------------------*/
 '''
class DataLoggerConfig(object):
    '''
    This class provides the read-in functionality for the Data Logger configuration file
    '''
    __GENERAL_SECTION = "GENERAL"
    __XIVELY_SECTION = "XIVELY"
    
    __NAME_KEY = "name"
    __UID_KEY = "uid"

    def __init__(self,name):
        self.__isParsed = False
        self.filenName = name
        self.__general = {}
        self.__xively = {}
        self.__bricklets = []
        
        
    def __get_section_as_hashmap(self,section_name ,parser ):
        '''
        saves variables out of an section to a hashmap.
        key -- variable name
        value -- variable value
        '''
        hashMap = {}
        for section_key in parser.options(section_name):
            hashMap[section_key] =  parser.get(section_name, section_key)
        return hashMap     
    
    def read_config_file(self):
        '''
        reads the entries out of the configuration file and 
        saves them into a <BrickletInfo> structure            
        '''
        parser = SafeConfigParser()
        # Open the file with the correct encoding
        with codecs.open(self.filenName, 'r', encoding='utf-8') as f:
            parser.readfp(f)
      
        for section_name in parser.sections():
            if (section_name == self.__GENERAL_SECTION):
                # Get GENERAL section
                self.__general =self.__get_section_as_hashmap(section_name,parser)

            elif (section_name == self.__XIVELY_SECTION):
                # Get XIVELY section
                self.__xively = self.__get_section_as_hashmap(section_name,parser)

            else:
                # Get all other variables  
                bricklet_name = parser.get(section_name, self.__NAME_KEY)
                bricklet_uid =  parser.get(section_name, self.__UID_KEY)
                
                tmp_bricklet = BrickletInfo(bricklet_name,bricklet_uid)
                for section_key in parser.options(section_name):
                    if (section_key != self.__NAME_KEY and section_key != self.__UID_KEY):
                        tmp_bricklet.addKeyValuePair(section_key, parser.get(section_name, section_key))

                self.__bricklets.append(tmp_bricklet)
                
        # configuration file is parsed an ready to use     
        self.__isParsed = True
        
    def get_general_section(self):
        '''
        Returns the variables out of the "GENERAL" section in the configuration file if it
        was already parsed otherwise it call the <read_config_file()> function first
        '''
        if(not self.__isParsed):
            self.read_config_file()
            
        return self.__general

    def get_xively_section(self):
        '''
        Returns the variables out of the "XIVELY" section in the configuration file if it
        was already parsed otherwise it call the <read_config_file()> function first
        '''
        if(not self.__isParsed):
            self.read_config_file()
            
        return self.__xively
        
    def get_bricklets(self):
        '''
        Returns an array of bricklets out of the configuration file if it
        was already parsed. Otherwise it call the <read_config_file()> function first
        '''
        if(not self.__isParsed):
            self.read_config_file()
        
        return self.__bricklets

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
        self.__name = name
        self.__uid = uid
        self.__variables = { }
   
        
    def addKeyValuePair(self, key, value):
        '''
        adds a key-value pair to the bricklet dictionary
        '''
        self.__variables[key] = value
 
    def get_variables(self):
        '''
        Returns the dictionary which provides the variable name and its value 
        '''
        return self.__variables  
    
    def get_name(self):
        '''
        Returns the bricklet name
        '''
        return self.__name
    
    def get_uid(self):
        '''
        Returns the bricklet uid
        '''
        return self.__uid

""""
/*---------------------------------------------------------------------------
                                WriterThread
 ---------------------------------------------------------------------------*/
"""
import Queue, threading, time

Q = Queue.Queue()       #gloabl queue for write jobs
Threads = []            #gloabl thread array for all running threads/jobs

THREAD_EXIT_FLAG = 0    #flag for stopping the thread   
#CB_SUM / CB_COUNT = CB_MED per sec
#CB_MED / CB_COUNT = Thread time for each write
CB_SUM = 0
CB_COUNT = 0
THREAD_SLEEP = 0
if CB_SUM > 0 and CB_COUNT > 0:
    THREAD_SLEEP = CB_SUM/1000/CB_COUNT/CB_COUNT     #TODO: magical thread sleep 


def writer_thread():
    csv_writer = CSVWriter(DEFAULT_FILE_PATH)
    
    while (True):
        if not q.empty():
            csv_data = q.get()
            #print "WR--THREAD      : %s" % (str(data.raw_data))
            if not csv_writer.write_data_row(csv_data):
                print "csv_writer.write_data_row failed!"
        #TODO: sleep time?
        time.sleep(THREAD_SLEEP)
        
        if(EXIT_FLAG and q.empty()): 
            
            exit = csv_writer.close_file()
            if exit:
                print "csv_writer closed!"
            else:
                print "csv_writer not closed! -> " + str(exit)
            break