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

from tinkerforge.ip_connection import IPConnection
import Queue, logging, threading, sys
import bricklets
import utils
from brickv.data_logger.utils import ConfigurationReader
from brickv.data_logger.utils import EventLogger
from brickv.data_logger.utils import CSVWriterJob, XivelyJob

class DataLogger():
    '''
    This class represents the data logger and an object of this class is
    the actual instance of a logging process
    '''   
       
    # constructor and other functions
    def __init__(self,config):
        
        # Thread configuration
        self.jobs = []              # thread hashmap for all running threads/jobs
        self.job_exit_flag = False   # flag for stopping the thread
        self.job_sleep = 1           # FIXME: quick testing fix (Enahncement -> use condition objects) 
        self.timers = []

        self.data_queue = {} #universal data_queue hash map
          
        # IPConenction configuration
        self.host = config._general[ConfigurationReader.GENERAL_HOST]
        self.port = utils.Utilities.parse_to_int(config._general[ConfigurationReader.GENERAL_PORT]) 
            
        self.ipcon = IPConnection()  
        #open IPConnection    
        self.ipcon.connect(self.host, self.port)  # Connect to brickd
        # Don't use device before ipcon is connected
        EventLogger.info("Connection to " + self.host + ":" + str(self.port) + " established.")
        self.ipcon.set_timeout(1) #TODO: Timeout number 
        EventLogger.debug("Set ipcon.time_out to 1.")
        
        # Configuration file processing   
        self._configuration = config
        
        self.default_file_path = "logged_data.csv"
        self.log_to_file = True
        self.log_to_xively = False
   
    
    def process_general_section(self,data):
        '''
        Information out of the general section will be consumed here
        '''         
        self.log_to_file = data[utils.ConfigurationReader.GENERAL_LOG_TO_FILE]
        self.default_file_path = data[utils.ConfigurationReader.GENERAL_PATH_TO_FILE]
        
        EventLogger.debug("Logging output to file: " + str(self.log_to_file)) 
        EventLogger.debug("Output file path: " + str(self.default_file_path)) 
          
    def process_xively_section(self,data):
        '''
        Information out of the xively section will be consumed here
        '''
        #TODO: write code for xively handling
        if len(data) == 0:
            return
    
        self.LOG_TO_XIVELY =  data.get(utils.ConfigurationReader.XIVELY_ACTIVE)
        logging.debug("Logging output to Xively: " +  str(self.LOG_TO_XIVELY))
        # = data.get(XIVELY_AGENT_DESCRIPTION)
        # = data.get(XIVELY_FEED)
        # = data.get(XIVELY_API_KEY)
        #  = DataLogger.parse_to_int(data.get(XIVELY_UPDATE_RATE))

    def initialize_bricklets(self,data):
        '''
        This function creates actual objects for each device out of the configuration
        '''
        simple_devices = self._configuration._simple_devices
        complex_devices = self._configuration._complex_devices
        special_devices = self._configuration._special_devices
        
        #start the timers
        try:
            for i in range(0, len(simple_devices)):
                bricklets.SimpleDevice(simple_devices[i], self).start_timer()            
             
            for i in range(0, len(complex_devices)):
                bricklets.ComplexDevice(complex_devices[i], self).start_timer()
         
            for i in range(0, len(special_devices)):
                (special_devices[i][bricklets.Identifier.DEVICE_CLASS](special_devices[i], self)).start_timer()

        except Exception as exc: # FIXME: Catch-All just for debugging purpose 
            msg = "A critical error occur: " + str(exc)
            EventLogger.critical( msg)
            self.stop(utils.DataLoggerException.DL_CRITICAL_ERROR)
                
    def run(self):
        '''
        This function starts the logging process
        '''    
        self.process_general_section(self._configuration._general)
        self.process_xively_section(self._configuration._xively)

        self.initialize_bricklets(self._configuration)
        
        """START-WRITE-THREAD"""       
        #create jobs
        #look which thread should be working
        if self.log_to_file:
            self.jobs.append(CSVWriterJob(name="CSV-Writer", datalogger=self))
        if self.log_to_xively:
            self.jobs.append(XivelyJob(name="Xively-Writer", datalogger=self))
        
        for t in self.jobs:
            t.start()
        EventLogger.debug("Jobs started.")    
    
        """START-TIMERS"""
        for t in self.timers:
            t.start()
        EventLogger.debug("Get-Timers started.")  
      
        """END_CONDITIONS"""
        EventLogger.info("DataLogger is runninng...")
        # TODO Exit condition ?
    
    def stop(self,error_code):
        '''
        This function ends the logging process
        '''
        EventLogger.info("Closing Timers and Threads...")    

        """CLEANUP_AFTER_STOP """
        #check if all timers stopped
        for t in self.timers:
            t.stop()        
        for t in self.timers:
            t.join()    
        EventLogger.debug("Get-Timers stopped.")
    
        #set THREAD_EXIT_FLAG for all work threads
        for job in self.jobs:
            job.stop()
        #wait for all threads to stop
        for job in  self.jobs:
            job.join()    
        EventLogger.debug("Jobs stopped.")
    
        if self.ipcon != None and self.ipcon.get_connection_state() == IPConnection.CONNECTION_STATE_CONNECTED:
            self.ipcon.disconnect()
        EventLogger.info("Connection closed successfully.")
       
    def add_to_queue(self,csv):
        '''
        '''
        for q in self.data_queue.values():
            q.put(csv)
            