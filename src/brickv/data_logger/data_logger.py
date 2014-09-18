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


class DataLogger():
    '''
    DataLogger class
    '''
        
    #Logger
    FILE_EVENT_LOGGING = False                              #for event logging in to a file
    EVENT_LOGGING_FILE_PATH = "data_logger.log"             #default file path for logging events TODO: enahcnment select file over commandline?
    LOGGING_EVENT_LEVEL = logging.DEBUG
    
    #General
    DEFAULT_FILE_PATH = "logged_data.csv"
    LOG_TO_FILE = True
    LOG_TO_XIVELY = False
    
    ipcon = IPConnection()
    host = "localhost"
    port = 4223  
    
    #Xivley Var
    xively = None                                           #xively object; xively queue
    
    #Queues
    Q = Queue.Queue()                                       #gloabl queue for write jobs
    
    #Thread things
    Threads = []                                            #gloabl thread array for all running threads/jobs
    THREAD_EXIT_FLAG = False                                #flag for stopping the thread   
    THREAD_SLEEP = 1#TODO: qucik testing fix                #in seconds!; fail state = -1 TODO: Enahncement -> use condition objects
    
    # constructor and other functions
    def __init__(self,config):
        if DataLogger.FILE_EVENT_LOGGING:
            logging.basicConfig(filename=DataLogger.EVENT_LOGGING_FILE_PATH,format='%(asctime)s - %(levelname)8s - %(message)s',level=DataLogger.LOGGING_EVENT_LEVEL)  
        else:
            logging.basicConfig(format="%(asctime)s - %(levelname)8s - %(message)s",level=DataLogger.LOGGING_EVENT_LEVEL) 
            
        #open IPConnection    
        DataLogger.ipcon.connect(DataLogger.host, DataLogger.port)  # Connect to brickd
        # Don't use device before ipcon is connected
        logging.info("Connection to " + DataLogger.host + ":" + str(DataLogger.port) + " established.")
        DataLogger.ipcon.set_timeout(1) #TODO: Timeout number 
        logging.debug("Set ipcon.time_out to 1.")
            
        self._configuration = config
    
    def general_switch(self,data):           
        self.LOG_TO_FILE = utils.Utilities.parse_to_bool(data.get(utils.DataLoggerConfig.GENERAL_LOG_TO_FILE))
        self.DEFAULT_FILE_PATH = data.get(utils.DataLoggerConfig.GENERAL_PATH_TO_FILE)
        
    def xively_switch(self,data):
        #TODO: write code for xively handling
    
        self.LOG_TO_XIVELY =  utils.Utilities.parse_to_bool(data.get(utils.DataLoggerConfig.XIVELY_ACTIVE))

        # = data.get(XIVELY_AGENT_DESCRIPTION)
        # = data.get(XIVELY_FEED)
        # = data.get(XIVELY_API_KEY)
        #  = DataLogger.parse_to_int(data.get(XIVELY_UPDATE_RATE))
        pass

    def bricklet_switch(self,data):
        for current_bricklet in data:
            try:
                bricklet_name = current_bricklet.name
                bricklet_uid = current_bricklet.uid
                bricklet_variables = current_bricklet.variables
        
                if bricklet_name == bricklets.AMBIENT_LIGHT:
                    bricklets.AmbientLightBricklet(bricklet_uid,bricklet_variables).start_timer()
                elif bricklet_name == bricklets.ANALOG_IN:
                    bricklets.AnalogInBricklet(bricklet_uid,bricklet_variables).start_timer()
                elif bricklet_name == bricklets.ANALOG_OUT:
                    bricklets.AnalogOutBricklet(bricklet_uid,bricklet_variables).start_timer()              
                elif bricklet_name == bricklets.BAROMETER:
                    bricklets.BarometerBricklet(bricklet_uid,bricklet_variables).start_timer()
                elif bricklet_name == bricklets.COLOR:
                    bricklets.ColorBricklet(bricklet_uid,bricklet_variables).start_timer()
                elif bricklet_name == bricklets.CURRENT_12:
                    bricklets.Current12Bricklet(bricklet_uid,bricklet_variables).start_timer()
                elif bricklet_name == bricklets.CURRENT_25:
                    bricklets.Current25Bricklet(bricklet_uid,bricklet_variables).start_timer()    
                elif bricklet_name == bricklets.DISTANCE_IR:
                    bricklets.DistanceIRBricklet(bricklet_uid,bricklet_variables).start_timer()
                elif bricklet_name == bricklets.DISTANCE_US:
                    bricklets.DistanceUSBricklet(bricklet_uid,bricklet_variables).start_timer()
                elif bricklet_name == bricklets.DUAL_BUTTON:
                    bricklets.DualButtonBricklet(bricklet_uid,bricklet_variables).start_timer()
                elif bricklet_name == bricklets.DUAL_RELAY:
                    bricklets.DualRelayBricklet(bricklet_uid,bricklet_variables).start_timer()
                elif bricklet_name == bricklets.GPS_BRICKLET:
                    bricklets.GPSBricklet(bricklet_uid,bricklet_variables).start_timer()
                elif bricklet_name == bricklets.HALL_EFFECT:
                    bricklets.HallEffectBricklet(bricklet_uid,bricklet_variables).start_timer()
                elif bricklet_name == bricklets.HUMIDITY:
                    bricklets.HumidityBricklet(bricklet_uid,bricklet_variables).start_timer()
                elif bricklet_name == bricklets.INDUSTRIAL_DIGITAL_IN_4:
                    bricklets.IndustrialDigitalIn4Bricklet(bricklet_uid,bricklet_variables).start_timer()      
                elif bricklet_name == bricklets.INDUSTRIAL_DIGITAL_OUT_4:
                    bricklets.IndustrialDigitalOut4Bricklet(bricklet_uid,bricklet_variables).start_timer()
                elif bricklet_name == bricklets.INDUSTRIAL_DUAL_0_20_MA:
                    bricklets.IndustrialDual020mABricklet(bricklet_uid,bricklet_variables).start_timer()
                elif bricklet_name == bricklets.INDUSTRIAL_QUAD_RELAY:
                    bricklets.IndustrialQuadRelayBricklet(bricklet_uid,bricklet_variables).start_timer()
                elif bricklet_name == bricklets.IO_16:
                    bricklets.IO16Bricklet(bricklet_uid,bricklet_variables).start_timer() 
                elif bricklet_name == bricklets.IO_4:
                    bricklets.IO4Bricklet(bricklet_uid,bricklet_variables).start_timer() 
                elif bricklet_name == bricklets.JOYSTICK:
                    bricklets.JoystickBricklet(bricklet_uid,bricklet_variables).start_timer() 
                elif bricklet_name == bricklets.LCD_16x2:
                    bricklets.LCD16x2Bricklet(bricklet_uid,bricklet_variables).start_timer() 
                elif bricklet_name == bricklets.LCD_20x4:
                    bricklets.LCD20x4Bricklet(bricklet_uid,bricklet_variables).start_timer() 
                elif bricklet_name == bricklets.LED_STRIP:
                    bricklets.LEDStripBricklet(bricklet_uid,bricklet_variables).start_timer()
                elif bricklet_name == bricklets.LINE:
                    bricklets.LineBricklet(bricklet_uid,bricklet_variables).start_timer()
                elif bricklet_name == bricklets.LINEAR_POTI:
                    bricklets.LinearPotiBricklet(bricklet_uid,bricklet_variables).start_timer()
                elif bricklet_name == bricklets.MOISTURE:
                    bricklets.MoistureBricklet(bricklet_uid,bricklet_variables).start_timer()
                elif bricklet_name == bricklets.MOTION_DETECTOR:
                    bricklets.MotionDetectorBricklet(bricklet_uid,bricklet_variables).start_timer()
                elif bricklet_name == bricklets.MULTI_TOUCH:
                   bricklets.MultiTouchBricklet(bricklet_uid,bricklet_variables).start_timer()
                elif bricklet_name == bricklets.NFC_RFID:
                    bricklets.NFCRFIDBricklet(bricklet_uid,bricklet_variables).start_timer()
                elif bricklet_name == bricklets.PIEZO_BUZZER:
                    bricklets.PiezoBuzzerBricklet(bricklet_uid,bricklet_variables).start_timer()
                elif bricklet_name == bricklets.PIEZO_SPEAKER:
                    bricklets.PiezoSpeakerBricklet(bricklet_uid,bricklet_variables).start_timer()
                elif bricklet_name == bricklets.PTC_BRICKLET:
                    bricklets.PTCBricklet(bricklet_uid,bricklet_variables).start_timer()
                elif bricklet_name == bricklets.REMOTE_SWITCH:
                    bricklets.RemoteSwitchBricklet(bricklet_uid,bricklet_variables).start_timer()
                elif bricklet_name == bricklets.ROTARY_ENCODER:
                    bricklets.RotaryEncoderBricklet(bricklet_uid,bricklet_variables).start_timer()  
                elif bricklet_name == bricklets.ROTARY_POTI:
                    bricklets.RotaryPotiBricklet(bricklet_uid,bricklet_variables).start_timer()
                elif bricklet_name == bricklets.SEGMENT_DISPLAY_4x7:
                    bricklets.SegmentDisplay4x7Bricklet(bricklet_uid,bricklet_variables).start_timer()  
                elif bricklet_name == bricklets.SOLID_STATE_RELAY:
                    bricklets.SolidStateRelayBricklet(bricklet_uid,bricklet_variables).start_timer()
                elif bricklet_name == bricklets.SOUND_INTENSITY:
                    bricklets.SoundIntensityBricklet(bricklet_uid,bricklet_variables).start_timer()
                elif bricklet_name == bricklets.TEMPERATURE:
                    bricklets.TemperatureBricklet(bricklet_uid,bricklet_variables).start_timer()
                elif bricklet_name == bricklets.TEMPERATURE_IR:
                    bricklets.TemperatureIRBricklet(bricklet_uid,bricklet_variables).start_timer()
                elif bricklet_name == bricklets.TILT:
                    bricklets.TiltBricklet(bricklet_uid,bricklet_variables).start_timer()
                elif bricklet_name == bricklets.VOLTAGE:
                    bricklets.VoltageBricklet(bricklet_uid,bricklet_variables).start_timer()
                elif bricklet_name == bricklets.VOLTAGE_CURRENT:
                    bricklets.VoltageCurrentBricklet(bricklet_uid,bricklet_variables).start_timer()
                else:
                    logging.warning("The bricklet [" +bricklet_name+ "] is not yet supported")   
                              
            except KeyError as key_error:
                msg = bricklet_name +"["+bricklet_uid+"] has no key [" + str(key_error) + "]. Please review the configuration file."
                logging.critical(msg)
                self.stopp(utils.DataLoggerException.DL_MISSING_ARGUMENT)

            except Exception as exc: # FIXME: Catch-All just for debugging purpose 
                msg = "A critical error occur " + str(exc)
                logging.critical( msg)
                self.stopp(utils.DataLoggerException.DL_CRITICAL_ERROR)
                
    def run(self):
        '''
        '''    
        self.general_switch(self._configuration.get_general_section())
        self.xively_switch(self._configuration.get_xively_section())
        self.bricklet_switch(self._configuration.get_bricklets())
        
        """START-WRITE-THREAD"""       
        #create write thread
        #look which thread should be working
        if DataLogger.LOG_TO_FILE:
            DataLogger.Threads.append(threading.Thread(name="CSV Writer Thread", target=utils.writer_thread))
        if DataLogger.LOG_TO_XIVELY:
            DataLogger.Threads.append(threading.Thread(name="Xively Writer Thread", target=utils.xively_thread))
        
        for t in DataLogger.Threads:
            t.start()
        logging.debug("Work Threads started.")    
    
        """START-TIMERS"""
        for t in utils.LoggerTimer.Timers:
            t.start()
        logging.debug("Get-Timers started.")  
      
        """END_CONDITIONS"""
        logging.info("DataLogger is runninng...")
        # TODO Exit condition ?
    
    def stopp(self,error_code):
        '''
        '''
        logging.info("Closing Timers and Threads...")    

        """CLEANUP_AFTER_STOP """
        #set EXIT_FLAG for Get-Timers
        utils.LoggerTimer.EXIT_FLAG = True
        #check if all timers stopped
        for t in utils.LoggerTimer.Timers:
            t.join()    
        logging.debug("Get-Timers stopped.")
    
        #set THREAD_EXIT_FLAG for all work threads
        DataLogger.THREAD_EXIT_FLAG = True
        #wait for all threads to stop
        for th in  DataLogger.Threads:
            th.join()    
        logging.debug("Work Threads stopped.")
    
        if DataLogger.ipcon != None and DataLogger.ipcon.get_connection_state() == IPConnection.CONNECTION_STATE_CONNECTED:
            DataLogger.ipcon.disconnect()
        logging.info("Connection closed successfully.")

        sys.exit(error_code)
    
    
    def add_to_queue(csv):
        '''
        '''
        #Look which queues are logging
        if DataLogger.LOG_TO_FILE:
            DataLogger.Q.put(csv)
        
        if DataLogger.LOG_TO_XIVELY:
            #DataLogger.xively.put(csv)
            logging.warning("Xively is not supported!")
    add_to_queue = staticmethod(add_to_queue)

