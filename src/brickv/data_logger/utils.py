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
from brickv.data_logger.event_logger import EventLogger
import time  # Writer Thread


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

    def replace_right(source, target, replacement, replacements=None):
        return replacement.join(source.rsplit(target, replacements))
    
    replace_right = staticmethod(replace_right)

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
