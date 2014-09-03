from data_logger_utils import LoggerTimer   #Timer for getVariable
from data_logger_utils import Q             #gloabl thread/job queue -> brickelts callbacks/timer
from data_logger_utils import CSVData       #bricklets

import data_logger_utils as dlu             #for gloabl variables

###Sections###
GENERAL_SECTION = "GENERAL"
GENERAL_LOG_TO_FILE = "log_to_file"
GENERAL_PATH_TO_FILE = "path_to_file"

XIVELY_SECTION = "XIVELY"
XIVELY_ACTIVE = "active"
XIVELY_AGENT_DESCRIPTION = "agent_description"
XIVELY_FEED = "feed"
XIVELY_API_KEY = "api_key"
XIVELY_UPDATE_RATE = "update_rate"
###Bricklets and Variables###

#ALL BRICKLETS + FUNCTIONS
#Ambient Light
AMBIENT_LIGHT = "Ambient Light"
AMBIENT_LIGHT_ILLUMINANCE = "Illuminance"
AMBIENT_LIGHT_ANALOG_VALUE = "Analog Value"

#Analog In    
#Analog Out
#Barometer
from tinkerforge.bricklet_barometer import Barometer

BAROMETER = "Barometer"
BAROMETER_AIR_PRESSURE = "Air Pressure"
BAROMETER_ALTITUDE = "Altitude"

class Barometer_Bricklet():
    
    def __init__(self, uid):
        self.uid = uid        
        self.__device = Barometer(self.uid, dlu.IPCON)


    def start_timer(self, data):        
        value1 = data[BAROMETER_AIR_PRESSURE]
        value2 = data[BAROMETER_ALTITUDE]
        
        if value1 != 0:
            dlu.CB_COUNT += 1
            dlu.CB_SUM += value1            
        if value2 != 0:
            dlu.CB_COUNT += 1
            dlu.CB_SUM += value2        
        
        t = LoggerTimer(value1, self.__timer_air_pressure)
        LoggerTimer.Timers.append(t)         
        t = LoggerTimer(value2, self.__timer_altitude)
        LoggerTimer.Timers.append(t)

    def __timer_air_pressure(self):
        value = self.__device.get_air_pressure()
        csv = CSVData(self.uid, BAROMETER, BAROMETER_AIR_PRESSURE, value)
        Q.put(csv)
        print "BAR_AP : " + str(value)
        
    def __timer_altitude(self):
        value = self.__device.get_altitude()
        csv = CSVData(self.uid, BAROMETER, BAROMETER_ALTITUDE, value)
        Q.put(csv)   
        print "BAR_AL : " + str(value)

#Breakout
#Color
#Current12
#Current25
#Distance IR
#Distance US
#Dual Button
#Dual Relay
#GPS
#Hall Effect
#Humidity
HUMIDITY = "Humidity"
HUMIDITY_HUMIDITY = "Humidity"
HUMIDITY_ANALOG_VALUE = "Analog Value"
#Industrial Digital In 4
#Industrial Digital Out 4
#Industrial Dual 0-20mA
#Industrial Quad Relay
#IO-16
#IO-4
#Joystick
#LCD 16x2
#LCD 20x4
#LED Strip
#Line
#Linear Poti
#Moisture
#Motion Detector
#Multi Touch
#NFC/RFID
#Piezo Buzzer
#Piezo Speaker
#PTC
#Remote Switch
#Rotary Encoder
#Rotary Poti
#Segment Display 4x7
#Solid State Relay
#Sound Intensity
#Temperature
#Temperature IR
#Tilt
#Voltage
#Voltage/Current