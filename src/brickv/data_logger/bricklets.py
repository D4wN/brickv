from brickv.data_logger.utils import LoggerTimer   #Timer for getVariable
from brickv.data_logger.utils import DataLogger    #gloabl thread/job queue -> brickelts callbacks/timer
from brickv.data_logger.utils import CSVData       #bricklets

import logging
###Bricklets and Variables###

#ALL BRICKLETS + FUNCTIONS##################################################################
class AbstractDevice(object):
    """DEBUG and Inheritance only class"""
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = None
        self._data = data
        self._identifier = None 

    def start_timer(self):
        logging.debug(self.__str__())
                
        
    def _try_catch(self, func):
        value = "[NYI-FAIL-TIMER]"
        #err = 0
        try:
            value = func()
        except Exception as e:
            value = self._exception_msg(e.value, e.description)
            #err = 1
        return value
    
    def _exception_msg(self, value, msg):
        return "ERROR[" + str(value) + "]: " + str(msg)
    
    def __str__(self):
        return "[DEVICE=" + str(type(self)) + " | <UID="+ str(self.uid) +"> | <IDENTIEFIER=" + str(self._identifier) + "> | <data="+ str(self._data) + ">]"
    
############################################################################################
#Ambient Light
from tinkerforge.bricklet_ambient_light import AmbientLight
AMBIENT_LIGHT = "Ambient Light"
AMBIENT_LIGHT_ILLUMINANCE = "Illuminance"
AMBIENT_LIGHT_ANALOG_VALUE = "Analog Value"
AMBIENT_LIGHT_CLASS = "AmbientLight"
class AmbientLightBricklet(AbstractDevice):
    
    def __init__(self, uid, data):
        self.uid = uid  
        self._device = AmbientLight(self.uid, DataLogger.ipcon)
        self._data = data
        self._identifier = AmbientLight.DEVICE_IDENTIFIER      


    def start_timer(self):
        AbstractDevice.start_timer(self)
                
        value1 = DataLogger.parse_to_int(self._data[AMBIENT_LIGHT_ANALOG_VALUE])
        value2 = DataLogger.parse_to_int(self._data[AMBIENT_LIGHT_ILLUMINANCE])     
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_analog_value))      
        LoggerTimer.Timers.append(LoggerTimer(value2, self._timer_illuminance))

    def _timer_analog_value(self):        
        value = self._try_catch(self._device.get_analog_value)
        csv = CSVData(self.uid, self._identifier, AMBIENT_LIGHT_ANALOG_VALUE, value)
        DataLogger.add_to_queue(csv)
        
    def _timer_illuminance(self):
        value = self._try_catch(self._device.get_illuminance)
        csv = CSVData(self.uid, self._identifier, AMBIENT_LIGHT_ILLUMINANCE, value)
        DataLogger.add_to_queue(csv)  

############################################################################################
#Analog In          
#TODO: Test with real bricklet                      
from tinkerforge.bricklet_analog_in import AnalogIn
ANALOG_IN = "Analog In"
ANALOG_IN_VOLTAGE = "Voltage"
ANALOG_IN_ANALOG_VALUE = "Analog Value"
ANALOG_IN_CLASS = "AnalogIn"
class AnalogInBricklet(AbstractDevice):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = AnalogIn(self.uid, DataLogger.ipcon)
        self._data = data
        self._identifier = AnalogIn.DEVICE_IDENTIFIER  


    def start_timer(self):  
        AbstractDevice.start_timer(self)
              
        value1 = DataLogger.parse_to_int(self._data[ANALOG_IN_ANALOG_VALUE])
        value2 = DataLogger.parse_to_int(self._data[ANALOG_IN_VOLTAGE])
              
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_analog_value))  
        LoggerTimer.Timers.append(LoggerTimer(value2, self._timer_voltage))

    def _timer_analog_value(self):
        value = self._try_catch(self._device.get_analog_value)
        csv = CSVData(self.uid, self._identifier, ANALOG_IN_ANALOG_VALUE, value)
        DataLogger.add_to_queue(csv)
        
    def _timer_voltage(self):
        value = self._try_catch(self._device.get_voltage)
        csv = CSVData(self.uid, self._identifier, ANALOG_IN_VOLTAGE, value)
        DataLogger.add_to_queue(csv)  

############################################################################################
#Analog Out
#TODO: Test with real bricklet  
from tinkerforge.bricklet_analog_out import AnalogOut
ANALOG_OUT = "Analog Out"
ANALOG_OUT_VOLTAGE = "Voltage"
ANALOG_OUT_CLASS = "AnalogOut"
class AnalogOutBricklet(AbstractDevice):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = AnalogOut(self.uid, DataLogger.ipcon)
        self._data = data
        self._identifier = AnalogOut.DEVICE_IDENTIFIER  


    def start_timer(self):   
        AbstractDevice.start_timer(self)
             
        value1 = DataLogger.parse_to_int(self._data[ANALOG_OUT_VOLTAGE]) 
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_voltage))         

    def _timer_voltage(self):
        value = self._try_catch(self._device.get_voltage)
        csv = CSVData(self.uid, self._identifier, ANALOG_OUT_VOLTAGE, value)
        DataLogger.add_to_queue(csv)

############################################################################################
#Barometer
from tinkerforge.bricklet_barometer import Barometer
BAROMETER = "Barometer"
BAROMETER_AIR_PRESSURE = "Air Pressure"
BAROMETER_ALTITUDE = "Altitude"
BAROMETER_CHIP_TEMPERATURE = "Chip Temperature"
BAROMETER_CLASS = "Barometer"
class BarometerBricklet(AbstractDevice):
    #chip_temperature()
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = Barometer(self.uid, DataLogger.ipcon)
        self._data = data
        self._identifier = Barometer.DEVICE_IDENTIFIER  


    def start_timer(self):        
        AbstractDevice.start_timer(self)
        
        value1 = DataLogger.parse_to_int(self._data[BAROMETER_AIR_PRESSURE])
        value2 = DataLogger.parse_to_int(self._data[BAROMETER_ALTITUDE])      
        value3 = DataLogger.parse_to_int(self._data[BAROMETER_CHIP_TEMPERATURE])  
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_air_pressure))
        LoggerTimer.Timers.append(LoggerTimer(value2, self._timer_altitude))
        LoggerTimer.Timers.append(LoggerTimer(value3, self._timer_chip_temperature))

    def _timer_air_pressure(self):
        value = self._try_catch(self._device.get_air_pressure)
        csv = CSVData(self.uid, self._identifier, BAROMETER_AIR_PRESSURE, value)
        DataLogger.add_to_queue(csv)
        
    def _timer_altitude(self):
        value = self._try_catch(self._device.get_altitude)
        csv = CSVData(self.uid, self._identifier, BAROMETER_ALTITUDE, value)
        DataLogger.add_to_queue(csv)  
         
    def _timer_chip_temperature(self):
        value = self._try_catch(self._device.get_chip_temperature)
        csv = CSVData(self.uid, self._identifier, BAROMETER_CHIP_TEMPERATURE, value)
        DataLogger.add_to_queue(csv)         

############################################################################################
#Color
#TODO: Test with real bricklet  
from tinkerforge.bricklet_color import Color
COLOR = "Color"
COLOR_RED = "Red"
COLOR_GREEN = "Green"
COLOR_BLUE = "Blue"
COLOR_CLEAR = "Clear"
COLOR_COLOR = "Rgbc"
COLOR_ILLUMINANCE = "Illuminance"
COLOR_TEMPERATURE = "Color Temperature"
COLOR_CLASS = "Color"
class ColorBricklet(AbstractDevice):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = Color(self.uid, DataLogger.ipcon)
        self._data = data
        self._identifier = Color.DEVICE_IDENTIFIER  


    def start_timer(self):     
        AbstractDevice.start_timer(self)
        
        value1 = DataLogger.parse_to_int(self._data[COLOR_COLOR])
        value2 = DataLogger.parse_to_int(self._data[COLOR_ILLUMINANCE])
        value3 = DataLogger.parse_to_int(self._data[COLOR_TEMPERATURE])   
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_color))         
        LoggerTimer.Timers.append(LoggerTimer(value2, self._timer_illuminance))
        LoggerTimer.Timers.append(LoggerTimer(value3, self._timer_color_temperature))

    def _timer_color(self):
        try:
            r, g, b, c = self.__TEMP_get_color()#self._device.get_color()
            if DataLogger.parse_to_bool(self._data[COLOR_RED]):
                DataLogger.add_to_queue(CSVData(self.uid, self._identifier, COLOR_RED, r))
            if DataLogger.parse_to_bool(self._data[COLOR_GREEN]):
                DataLogger.add_to_queue(CSVData(self.uid, self._identifier, COLOR_GREEN, g))
            if DataLogger.parse_to_bool(self._data[COLOR_BLUE]):
                DataLogger.add_to_queue(CSVData(self.uid, self._identifier, COLOR_BLUE, b))
            if DataLogger.parse_to_bool(self._data[COLOR_CLEAR]): 
                DataLogger.add_to_queue(CSVData(self.uid, self._identifier, COLOR_CLEAR, c))
        except Exception as e:
            DataLogger.add_to_queue(CSVData(self.uid, self._identifier, COLOR_COLOR, self._exception_msg(e.value, e.description)))
        
    def _timer_illuminance(self):
        value = self._try_catch(self._device.get_illuminance)
        csv = CSVData(self.uid, self._identifier, COLOR_ILLUMINANCE, value)
        DataLogger.add_to_queue(csv)  
        
    def _timer_color_temperature(self):
        value = self._try_catch(self._device.get_color_temperature)
        csv = CSVData(self.uid, self._identifier, COLOR_ILLUMINANCE, value)
        DataLogger.add_to_queue(csv) 
        
    def __TEMP_get_color(self):
        return (10, 20, 30, 40)
    
############################################################################################
#TODO: Test with real bricklet  Current12
from tinkerforge.bricklet_current12 import Current12
CURRENT_12 = "Current 12"
CURRENT_12_CURRENT = "Current"
CURRENT_12_ANALOG_VALUE = "Analog Value"
CURRENT_12_CLASS = "Current12"
class Current12Bricklet(AbstractDevice):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = Current12(self.uid, DataLogger.ipcon)
        self._data = data
        self._identifier = Current12.DEVICE_IDENTIFIER  


    def start_timer(self):
        AbstractDevice.start_timer(self)  
        
        value1 = DataLogger.parse_to_int(self._data[CURRENT_12_ANALOG_VALUE])
        value2 = DataLogger.parse_to_int(self._data[CURRENT_12_CURRENT])  
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_analog_value))         
        LoggerTimer.Timers.append(LoggerTimer(value2, self._timer_current))  
    
    def _timer_analog_value(self):
        value = self._try_catch(self._device.get_analog_value)
        csv = CSVData(self.uid, self._identifier, CURRENT_12_ANALOG_VALUE, value)
        DataLogger.add_to_queue(csv) 
    
    def _timer_current(self):
        value = self._try_catch(self._device.get_current)
        csv = CSVData(self.uid, self._identifier, CURRENT_12_CURRENT, value)
        DataLogger.add_to_queue(csv)         

############################################################################################
#TODO: Test with real bricklet  Current25
from tinkerforge.bricklet_current25 import Current25
CURRENT_25 = "Current 25"
CURRENT_25_CURRENT = "Current"
CURRENT_25_ANALOG_VALUE = "Analog Value"
CURRENT_25_CLASS = "Current25"
class Current25Bricklet(AbstractDevice):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = Current25(self.uid, DataLogger.ipcon)
        self._data = data
        self._identifier = Current25.DEVICE_IDENTIFIER 


    def start_timer(self):
        AbstractDevice.start_timer(self)   
        
        value1 = DataLogger.parse_to_int(self._data[CURRENT_25_ANALOG_VALUE])
        value2 = DataLogger.parse_to_int(self._data[CURRENT_25_CURRENT])  
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_analog_value))         
        LoggerTimer.Timers.append(LoggerTimer(value2, self._timer_current))  
    
    def _timer_analog_value(self):
        value = self._try_catch(self._device.get_analog_value)
        csv = CSVData(self.uid, self._identifier, CURRENT_25_ANALOG_VALUE, value)
        DataLogger.add_to_queue(csv) 
        
    def _timer_current(self):
        value = self._try_catch(self._device.get_current)
        csv = CSVData(self.uid, self._identifier, CURRENT_25_CURRENT, value)
        DataLogger.add_to_queue(csv) 

############################################################################################
#TODO: Test with real bricklet  Distance IR
from tinkerforge.bricklet_distance_ir import DistanceIR
DISTANCE_IR = "Distance IR"
DISTANCE_IR_DISTANCE = "Distance"
DISTANCE_IR_ANALOG_VALUE = "Analog Value"
DISTANCE_IR_CLASS = "DistanceIR"
class DistanceIRBricklet(AbstractDevice):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = DistanceIR(self.uid, DataLogger.ipcon)
        self._data = data
        self._identifier = DistanceIR.DEVICE_IDENTIFIER 


    def start_timer(self):
        AbstractDevice.start_timer(self)   
        
        value1 = DataLogger.parse_to_int(self._data[DISTANCE_IR_ANALOG_VALUE])
        value2 = DataLogger.parse_to_int(self._data[DISTANCE_IR_DISTANCE])  
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_analog_value))         
        LoggerTimer.Timers.append(LoggerTimer(value2, self._timer_distance))  
    
    def _timer_analog_value(self):
        value = self._try_catch(self._device.get_analog_value)
        csv = CSVData(self.uid, self._identifier, DISTANCE_IR_ANALOG_VALUE, value)
        DataLogger.add_to_queue(csv) 
        
    def _timer_distance(self):
        value = self._try_catch(self._device.get_analog_value)
        csv = CSVData(self.uid, self._identifier, DISTANCE_IR_DISTANCE, value)
        DataLogger.add_to_queue(csv)

############################################################################################
#TODO: Test with real bricklet  Distance US
from tinkerforge.bricklet_distance_us import DistanceUS
DISTANCE_US = "Distance US"
DISTANCE_US_DISTANCE = "Distance"
DISTANCE_US_CLASS = "DistanceUS"
class DistanceUSBricklet(AbstractDevice):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = DistanceUS(self.uid, DataLogger.ipcon)
        self._data = data
        self._identifier = DistanceUS.DEVICE_IDENTIFIER 


    def start_timer(self):
        AbstractDevice.start_timer(self)   
        
        value1 = DataLogger.parse_to_int(self._data[DISTANCE_US_DISTANCE])
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_distance))   
    
    def _timer_distance(self):
        value = self._try_catch(self._device.get_distance_value)
        csv = CSVData(self.uid, self._identifier, DISTANCE_US_DISTANCE, value)
        DataLogger.add_to_queue(csv) 
        
############################################################################################
#TODO: Test with real bricklet  Dual Button
from tinkerforge.bricklet_dual_button import DualButton
DUAL_BUTTON = "Dual Button"
DUAL_BUTTON_BUTTONS = "Buttons"
DUAL_BUTTON_BUTTON_L = "Button_L"
DUAL_BUTTON_BUTTON_R = "Button_R"
DUAL_BUTTON_LEDS = "Leds"
DUAL_BUTTON_LED_L = "Led_L"
DUAL_BUTTON_LED_R = "Led_R"
DUAL_BUTTON_CLASS = "DualButton"
class DualButtonBricklet(AbstractDevice):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = DualButton(self.uid, DataLogger.ipcon)
        self._data = data
        self._identifier = DualButton.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        
        value1 = DataLogger.parse_to_int(self._data[DUAL_BUTTON_BUTTONS])
        value2 = DataLogger.parse_to_int(self._data[DUAL_BUTTON_LEDS])
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_buttons))   
        LoggerTimer.Timers.append(LoggerTimer(value2, self._timer_leds))  
        
    
    def _timer_buttons(self):
        try:
            button_l, button_r = self._device.get_button_state()
            if DataLogger.parse_to_bool(self._data[DUAL_BUTTON_BUTTON_L]):
                DataLogger.add_to_queue(CSVData(self.uid, self._identifier, DUAL_BUTTON_BUTTON_L, button_l))
            if DataLogger.parse_to_bool(self._data[DUAL_BUTTON_BUTTON_R]):
                DataLogger.add_to_queue(CSVData(self.uid, self._identifier, DUAL_BUTTON_BUTTON_R, button_r))
        except Exception as e:
            DataLogger.add_to_queue(CSVData(self.uid, self._identifier, DUAL_BUTTON_BUTTONS, self._exception_msg(e.value, e.description)))

    def _timer_leds(self):
        try:
            led_l, led_r = self._device.get_led_state()
            if DataLogger.parse_to_bool(self._data[DUAL_BUTTON_LED_L]):
                DataLogger.add_to_queue(CSVData(self.uid, self._identifier, DUAL_BUTTON_LED_L, led_l))
            if DataLogger.parse_to_bool(self._data[DUAL_BUTTON_LED_R]):
                DataLogger.add_to_queue(CSVData(self.uid, self._identifier, DUAL_BUTTON_LED_R, led_r))
        except Exception as e:
            DataLogger.add_to_queue(CSVData(self.uid, self._identifier, DUAL_BUTTON_LEDS, self._exception_msg(e.value, e.description)))

############################################################################################
#TODO: Test with real bricklet  Dual Relay
from tinkerforge.bricklet_dual_relay import DualRelay
DUAL_RELAY = "Dual Relay"
DUAL_RELAY_STATE = "State"
DUAL_RELAY_1 = "Relay1"
DUAL_RELAY_2 = "Relay2"
DUAL_RELAY_CLASS = "DualRelay"
class DualRelayBricklet(AbstractDevice):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = DualRelay(self.uid, DataLogger.ipcon)
        self._data = data
        self._identifier = DualRelay.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        
        value1 = DataLogger.parse_to_int(self._data[DUAL_RELAY_STATE])
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_state))  
    
    def _timer_state(self):
        try:
            r1, r2 = self._device.get_state()
            if DataLogger.parse_to_bool(self._data[DUAL_RELAY_1]):
                DataLogger.add_to_queue(CSVData(self.uid, self._identifier, DUAL_RELAY_1, r1))
            if DataLogger.parse_to_bool(self._data[DUAL_RELAY_2]):
                DataLogger.add_to_queue(CSVData(self.uid, self._identifier, DUAL_RELAY_2, r2))
        except Exception as e:
            DataLogger.add_to_queue(CSVData(self.uid, self._identifier, DUAL_RELAY_STATE, self._exception_msg(e.value, e.description)))

############################################################################################
#TODO: Test with real bricklet  GPS
from tinkerforge.bricklet_gps import GPS
GPS_BRICKLET = "GPS"
GPS_FIX_STATUS = "Fix Status"
GPS_SATELLITES_VIEW = "Satellites View"
GPS_SATELLITES_USED = "Satellites Used"
GPS_COORDINATES = "Coordinates"
GPS_LATITUDE = "Latitude"
GPS_NS = "Ns"
GPS_LONGITUDE = "Longitude"
GPS_EW = "Ew"
GPS_PDOP = "Pdop"
GPS_HDOP = "Hdop"
GPS_VDOP = "Vdop"
GPS_EPE = "Epe"
GPS_ALTITUDE = "Altitude"
GPS_ALTITUDE_VALUE = "Altitude Value"
GPS_GEOIDAL_SEPERATION = "Geoidal Seperation"
GPS_MOTION = "Motion"
GPS_COURSE = "Course"
GPS_SPEED = "Speed"
GPS_DATE_TIME = "Date Time"
GPS_DATE= "Date"
GPS_TIME = "Time"
GPS_CLASS = "GPS"
class GPSBricklet(AbstractDevice):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = GPS(self.uid, DataLogger.ipcon)
        self._data = data
        self._identifier = GPS.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        
        value1 = DataLogger.parse_to_int(self._data[GPS_COORDINATES])
        value2 = DataLogger.parse_to_int(self._data[GPS_ALTITUDE])
        value3 = DataLogger.parse_to_int(self._data[GPS_MOTION])
        value4 = DataLogger.parse_to_int(self._data[GPS_DATE_TIME])
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_coordinates))  
        LoggerTimer.Timers.append(LoggerTimer(value2, self._timer_altitude)) 
        LoggerTimer.Timers.append(LoggerTimer(value3, self._timer_motion)) 
        LoggerTimer.Timers.append(LoggerTimer(value4, self._timer_date_time)) 
    
    def _timer_coordinates(self):
        try:
            #check for the FIX Value of get_status()
            fix = self._get_fix_status()
                          
            if fix == GPS.FIX_NO_FIX:
                DataLogger.add_to_queue(CSVData(self.uid, self._identifier, GPS_COORDINATES, self._exception_msg("Fix-Status="+fix, "GPS Fix-Status was 1, but needs to be 2 or 3 for valid Coordinates.")))
                return

            latitude, ns, longitude, ew, pdop, hdop, vdop, epe = self._device.get_coordinates()     
            #latitude, ns, longitude, ew, pdop, hdop, vdop, epe = self.__TMP_get_coordinates()  #TODO: TMP ONLY       
            if DataLogger.parse_to_bool(self._data[GPS_LATITUDE]):
                DataLogger.add_to_queue(CSVData(self.uid, self._identifier, GPS_LATITUDE, latitude))
            if DataLogger.parse_to_bool(self._data[GPS_NS]):
                DataLogger.add_to_queue(CSVData(self.uid, self._identifier, GPS_NS, ns))
            if DataLogger.parse_to_bool(self._data[GPS_LONGITUDE]):
                DataLogger.add_to_queue(CSVData(self.uid, self._identifier, GPS_LONGITUDE, longitude))
            if DataLogger.parse_to_bool(self._data[GPS_EW]):
                DataLogger.add_to_queue(CSVData(self.uid, self._identifier, GPS_EW, ew))
            if DataLogger.parse_to_bool(self._data[GPS_PDOP]):
                DataLogger.add_to_queue(CSVData(self.uid, self._identifier, GPS_PDOP, pdop))
            if DataLogger.parse_to_bool(self._data[GPS_HDOP]):
                DataLogger.add_to_queue(CSVData(self.uid, self._identifier, GPS_HDOP, hdop))
            if DataLogger.parse_to_bool(self._data[GPS_VDOP]):
                DataLogger.add_to_queue(CSVData(self.uid, self._identifier, GPS_VDOP, vdop))
            if DataLogger.parse_to_bool(self._data[GPS_EPE]):
                DataLogger.add_to_queue(CSVData(self.uid, self._identifier, GPS_EPE, epe))
        except Exception as e:
            DataLogger.add_to_queue(CSVData(self.uid, self._identifier, GPS_COORDINATES, self._exception_msg(e.value, e.description)))

    def _timer_altitude(self):
        try:
            #check for the FIX Value of get_status()
            fix = self._get_fix_status()
              
            if fix != GPS.FIX_3D_FIX:
                DataLogger.add_to_queue(CSVData(self.uid, self._identifier, GPS_ALTITUDE, self._exception_msg("Fix-Status="+fix, "GPS Fix-Status was " + fix + ", but needs to be 3 for valid Altitude Values.")))
                return

            altitude, geoidal_separation = self._device.get_altitude()            
            if DataLogger.parse_to_bool(self._data[GPS_ALTITUDE_VALUE]):
                DataLogger.add_to_queue(CSVData(self.uid, self._identifier, GPS_ALTITUDE_VALUE, altitude))
            if DataLogger.parse_to_bool(self._data[GPS_GEOIDAL_SEPERATION]):
                DataLogger.add_to_queue(CSVData(self.uid, self._identifier, GPS_GEOIDAL_SEPERATION, geoidal_separation))
        except Exception as e:
            DataLogger.add_to_queue(CSVData(self.uid, self._identifier, GPS_ALTITUDE, self._exception_msg(e.value, e.description)))

    def _timer_motion(self):
        try:
            #check for the FIX Value of get_status()
            fix = self._get_fix_status()
              
            if fix == GPS.FIX_NO_FIX:
                DataLogger.add_to_queue(CSVData(self.uid, self._identifier, GPS_MOTION, self._exception_msg("Fix-Status="+fix, "GPS Fix-Status was " + fix + ", but needs to be 2 or 3 for valid Altitude Values.")))
                return

            course, speed = self._device.get_motion()
            if DataLogger.parse_to_bool(self._data[GPS_COURSE]):
                DataLogger.add_to_queue(CSVData(self.uid, self._identifier, GPS_COURSE, course))
            if DataLogger.parse_to_bool(self._data[GPS_SPEED]):
                DataLogger.add_to_queue(CSVData(self.uid, self._identifier, GPS_SPEED, speed))
        except Exception as e:
            DataLogger.add_to_queue(CSVData(self.uid, self._identifier, GPS_MOTION, self._exception_msg(e.value, e.description)))

    def _timer_date_time(self):
        try:
            date, time = self._device.get_date_time()
            if DataLogger.parse_to_bool(self._data[GPS_DATE]):
                DataLogger.add_to_queue(CSVData(self.uid, self._identifier, GPS_DATE, date))
            if DataLogger.parse_to_bool(self._data[GPS_TIME]):
                DataLogger.add_to_queue(CSVData(self.uid, self._identifier, GPS_TIME, time))
        except Exception as e:
            DataLogger.add_to_queue(CSVData(self.uid, self._identifier, GPS_DATE_TIME, self._exception_msg(e.value, e.description)))

    def _get_fix_status(self):
        fix, satellites_view, satellites_used = self._device.get_status()
        #fix, satellites_view, satellites_used = self.__TMP_get_status()#TODO: TMP ONLY
        
        if DataLogger.parse_to_bool(self._data[GPS_FIX_STATUS]):
            DataLogger.add_to_queue(CSVData(self.uid, self._identifier, GPS_FIX_STATUS, fix))
        if DataLogger.parse_to_bool(self._data[GPS_SATELLITES_VIEW]):
            DataLogger.add_to_queue(CSVData(self.uid, self._identifier, GPS_SATELLITES_VIEW, satellites_view))
        if DataLogger.parse_to_bool(self._data[GPS_SATELLITES_USED]):
            DataLogger.add_to_queue(CSVData(self.uid, self._identifier, GPS_SATELLITES_USED, satellites_used))
        return fix
    
    #TODO: delete Dummys
    def __TMP_get_status(self):
        #fix, satellites_view, satellites_used
        return (2, 10, 8)

    def __TMP_get_coordinates(self):
        #latitude, ns, longitude, ew, pdop, hdop, vdop, epe
        #int, chr, int, chr, int, int, int, int)
        return (57123468, 'N', 46012357, 'E', 1, 2, 3, 42)
    
############################################################################################
#TODO: Test with real bricklet  Hall Effect
from tinkerforge.bricklet_hall_effect import HallEffect
HALL_EFFECT = "Hall Effect"
HALL_EFFECT_VALUE = "Value"
HALL_EFFECT_CLASS = "HallEffect"
class HallEffectBricklet(AbstractDevice):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = HallEffect(self.uid, DataLogger.ipcon)
        self._data = data
        self._identifier = HallEffect.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        
        value1 = DataLogger.parse_to_int(self._data[HALL_EFFECT_VALUE])
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_value))   
    
    def _timer_value(self):
        value = self._try_catch(self._device.get_value)
        csv = CSVData(self.uid, self._identifier, HALL_EFFECT_VALUE, value)
        DataLogger.add_to_queue(csv)         

############################################################################################
#Humidity
from tinkerforge.bricklet_humidity import Humidity
HUMIDITY = "Humidity"
HUMIDITY_HUMIDITY = "Humidity"
HUMIDITY_ANALOG_VALUE = "Analog Value"
HUMIDITY_CLASS = "Humidity"
class HumidityBricklet(AbstractDevice):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = Humidity(self.uid, DataLogger.ipcon)
        self._data = data
        self._identifier = Humidity.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
                
        value1 = DataLogger.parse_to_int(self._data[HUMIDITY_ANALOG_VALUE])
        value2 = DataLogger.parse_to_int(self._data[HUMIDITY_HUMIDITY])       
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_analog_value))         
        LoggerTimer.Timers.append(LoggerTimer(value2, self._timer_humidity))

    def _timer_analog_value(self):
        value = self._try_catch(self._device.get_analog_value)
        csv = CSVData(self.uid, self._identifier, HUMIDITY_ANALOG_VALUE, value)
        DataLogger.add_to_queue(csv)
        
    def _timer_humidity(self):
        value = self._try_catch(self._device.get_humidity)
        csv = CSVData(self.uid, self._identifier, HUMIDITY_HUMIDITY, value)
        DataLogger.add_to_queue(csv)   

############################################################################################
#TODO: Test with real bricklet  Industrial Digital In 4
#TODO: Industrial Digital In 4  - variables? Dont know how to log this bricklet!
from tinkerforge.bricklet_industrial_digital_in_4 import IndustrialDigitalIn4
INDUSTRIAL_DIGITAL_IN_4 = "Industrial Digital In 4"
INDUSTRIAL_DIGITIAL_IN_4_CLASS = "IndustrialDigitalIn4"
class IndustrialDigitalIn4Bricklet(AbstractDevice):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = IndustrialDigitalIn4(self.uid, DataLogger.ipcon)
        self._data = data
        self._identifier = IndustrialDigitalIn4.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        logging.warning("The IndustrialDigitalIn4Bricklet is not supported for Logging actions!")

############################################################################################
#TODO: Test with real bricklet  Industrial Digital Out 4
#TODO: Industrial Digital Out 4 - variables? Dont know how to log this bricklet!
from tinkerforge.bricklet_industrial_digital_out_4 import IndustrialDigitalOut4
INDUSTRIAL_DIGITAL_OUT_4 = "Industrial Digital Out 4"
INDUSTRIAL_DIGITAL_OUT_4_CLASS  = "IndustrialDigitalOut4"
class IndustrialDigitalOut4Bricklet(AbstractDevice):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = IndustrialDigitalOut4(self.uid, DataLogger.ipcon)
        self._data = data
        self._identifier = IndustrialDigitalOut4.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        logging.warning("The IndustrialDigitalOut4Bricklet is not supported for Logging actions!")

############################################################################################
#TODO: Test with real bricklet  Industrial Dual 0-20mA
from tinkerforge.bricklet_industrial_dual_0_20ma import IndustrialDual020mA
INDUSTRIAL_DUAL_0_20_MA = "Industrial Dual 0 20 mA"
INDUSTRIAL_DUAL_0_20_MA_CURRENT = "Current"
INDUSTRIAL_DUAL_0_20_MA_CURRENT_0 = "Current 0"
INDUSTRIAL_DUAL_0_20_MA_CURRENT_1 = "Current 1"
INDUSTRIAL_DUAL_0_20_MA_CLASS = "IndustrialDual020mA"
class IndustrialDual020mABricklet(AbstractDevice):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = IndustrialDual020mA(self.uid, DataLogger.ipcon)
        self._data = data
        self._identifier = IndustrialDual020mA.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        
        value1 = DataLogger.parse_to_int(self._data[INDUSTRIAL_DUAL_0_20_MA_CURRENT])      
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_current))  

    def _timer_current(self):
        try:
            sensor_0 = self._device.get_current(0)
            sensor_1 = self._device.get_current(1)
            
            if DataLogger.parse_to_bool(self._data[INDUSTRIAL_DUAL_0_20_MA_CURRENT_0]):
                DataLogger.add_to_queue(CSVData(self.uid, self._identifier, INDUSTRIAL_DUAL_0_20_MA_CURRENT_0, sensor_0))            
            if DataLogger.parse_to_bool(self._data[INDUSTRIAL_DUAL_0_20_MA_CURRENT_1]):
                DataLogger.add_to_queue(CSVData(self.uid, self._identifier, INDUSTRIAL_DUAL_0_20_MA_CURRENT_1, sensor_1))

        except Exception as e:
            csv = CSVData(self.uid, INDUSTRIAL_DUAL_0_20_MA, self._identifier, self._exception_msg(e.value, e.description))
            DataLogger.add_to_queue(csv)

############################################################################################
#TODO: Test with real bricklet  Industrial Quad Relay
#TODO: Industrial Industrial Quad Relay - variables? Dont know how to log this bricklet!
from tinkerforge.bricklet_industrial_quad_relay import IndustrialQuadRelay
INDUSTRIAL_QUAD_RELAY = "Industrial Quad Relay"
INDUSTRIAL_QUAD_RELAY_CLASS = "IndustrialQuadRelay"
class IndustrialQuadRelayBricklet(AbstractDevice):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = IndustrialQuadRelay(self.uid, DataLogger.ipcon)
        self._data = data
        self._identifier = IndustrialQuadRelay.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        logging.warning("The IndustrialQuadRelayBricklet is not supported for Logging actions!")

############################################################################################
#TODO: Test with real bricklet  IO-16
from tinkerforge.bricklet_io16 import IO16
IO_16 = "IO-16"
IO_16_PORTS = "Ports"
IO_16_PORT_A = "Port A"
IO_16_PORT_B = "Port B"
IO_16_CLASS = "IO16"
class IO16Bricklet(AbstractDevice):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = IO16(self.uid, DataLogger.ipcon)
        self._data = data
        self._identifier = IO16.DEVICE_IDENTIFIER 

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        
        value1 = DataLogger.parse_to_int(self._data[IO_16_PORTS])      
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_ports))  

    def _timer_ports(self):
        try:
            port_a = self._device.get_port('a')
            port_b = self._device.get_port('b')
            
            if DataLogger.parse_to_bool(self._data[IO_16_PORT_A]):
                DataLogger.add_to_queue(CSVData(self.uid, self._identifier, IO_16_PORT_A, port_a))           
            if DataLogger.parse_to_bool(self._data[IO_16_PORT_B]):
                DataLogger.add_to_queue(CSVData(self.uid, self._identifier, IO_16_PORT_B, port_b))

        except Exception as e:
            csv = CSVData(self.uid, self._identifier, IO_16_PORTS, self._exception_msg(e.value, e.description))
            DataLogger.add_to_queue(csv)

############################################################################################
#TODO: Test with real bricklet  IO-4
from tinkerforge.bricklet_io4 import IO4
IO_4 = "IO-4"
IO_4_VALUE = "Value"
IO_4_CLASS = "IO4"
class IO4Bricklet(AbstractDevice):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = IO4(self.uid, DataLogger.ipcon)
        self._data = data
        self._identifier = IO4.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        
        value1 = DataLogger.parse_to_int(self._data[IO_4_VALUE])     
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_value)) 

    def _timer_value(self):
        value = self._try_catch(self._device.get_value)
        csv = CSVData(self.uid, self._identifier, IO_4_VALUE, value)
        DataLogger.add_to_queue(csv)

############################################################################################
#TODO: Test with real bricklet  Joystick
from tinkerforge.bricklet_joystick import Joystick
JOYSTICK = "Joystick"
JOYSTICK_POSITION = "Position"
JOYSTICK_POSITION_X = "Position X"
JOYSTICK_POSITION_Y = "Position Y"
JOYSTICK_ANALOG_VALUE = "Analog Value"
JOYSTICK_ANALOG_VALUE_X = "Analog X"
JOYSTICK_ANALOG_VALUE_Y = "Analog Y"
JOYSTICK_PRESSED = "Pressed"
JOYSTICK_CLASS = "Joystick"
class JoystickBricklet(AbstractDevice):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = Joystick(self.uid, DataLogger.ipcon)
        self._data = data
        self._identifier = Joystick.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        
        value1 = DataLogger.parse_to_int(self._data[JOYSTICK_POSITION])     
        value2 = DataLogger.parse_to_int(self._data[JOYSTICK_ANALOG_VALUE])    
        value3 = DataLogger.parse_to_int(self._data[JOYSTICK_PRESSED])    
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_position)) 
        LoggerTimer.Timers.append(LoggerTimer(value2, self._timer_analog_value)) 
        LoggerTimer.Timers.append(LoggerTimer(value3, self._timer_is_pressed)) 

    def _timer_position(self):
        try:
            x, y = self._device.get_position()

            if DataLogger.parse_to_bool(self._data[JOYSTICK_POSITION_X]):
                DataLogger.add_to_queue(CSVData(self.uid, self._identifier, JOYSTICK_POSITION_X, x))       
            if DataLogger.parse_to_bool(self._data[JOYSTICK_POSITION_Y]):
                DataLogger.add_to_queue(CSVData(self.uid, self._identifier, JOYSTICK_POSITION_Y, y))

        except Exception as e:
            csv = CSVData(self.uid, self._identifier, JOYSTICK_POSITION, self._exception_msg(e.value, e.description))
            DataLogger.add_to_queue(csv)
        
    def _timer_analog_value(self):
        value = self._try_catch(self._device.get_analog_value)
        csv = CSVData(self.uid, self._identifier, JOYSTICK_ANALOG_VALUE, value)
        DataLogger.add_to_queue(csv)
    
    def _timer_is_pressed(self):
        value = self._try_catch(self._device.is_pressed)
        csv = CSVData(self.uid, self._identifier, JOYSTICK_PRESSED, value)
        DataLogger.add_to_queue(csv)

############################################################################################
#TODO: Test with real bricklet  LCD 16x2
#TODO: LCD 16x2 - variables? Dont know how to log this bricklet!
from tinkerforge.bricklet_lcd_16x2 import LCD16x2
LCD_16x2 = "LCD 16x2"
LCD_16x2_CLASS = "LCD16x2"
class LCD16x2Bricklet(AbstractDevice):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = LCD16x2(self.uid, DataLogger.ipcon)
        self._data = data
        self._identifier = LCD16x2.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self)         
        logging.warning("The LCD16x2Bricklet is not supported for Logging actions!")

############################################################################################
#TODO: Test with real bricklet  LCD 20x4
#TODO: LCD 20x4 - variables? Dont know how to log this bricklet!
from tinkerforge.bricklet_lcd_20x4 import LCD20x4
LCD_20x4 = "LCD 20x4"
LCD_20x4_CLASS = "LCD_20x4"
class LCD20x4Bricklet(AbstractDevice):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = LCD20x4(self.uid, DataLogger.ipcon)
        self._data = data
        self._identifier = LCD20x4.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self)
        logging.warning("The LCD20x4Bricklet is not supported for Logging actions!")

############################################################################################
#TODO: Test with real bricklet  LED Strip
from tinkerforge.bricklet_led_strip import LEDStrip
LED_STRIP = "LED Strip"
LED_STRIP_SUPPLY_VOLTAGE = "Supply Voltage"
LED_STRIP_CLASS = "LEDStrip"
class LEDStripBricklet(AbstractDevice):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = LEDStrip(self.uid, DataLogger.ipcon)
        self._data = data
        self._identifier = LEDStrip.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        
        value1 = DataLogger.parse_to_int(self._data[LED_STRIP_SUPPLY_VOLTAGE])   
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_supply_voltage)) 

    def _timer_supply_voltage(self):
        value = self._try_catch(self._device.get_supply_voltage)
        DataLogger.add_to_queue(CSVData(self.uid, self._identifier, LED_STRIP_SUPPLY_VOLTAGE, value))
        
############################################################################################
#TODO: Test with real bricklet  Line
from tinkerforge.bricklet_line import BrickletLine
LINE = "line"
LINE_REFLECTIVITY = "Reflectivity"
LINE_CLASS = "BrickletLine"
class LineBricklet(AbstractDevice):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = BrickletLine(self.uid, DataLogger.ipcon)
        self._data = data
        self._identifier = BrickletLine.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self)
        
        value1 = DataLogger.parse_to_int(self._data[LINE_REFLECTIVITY])   
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_refelctivity)) 

    def _timer_refelctivity(self):
        value = self._try_catch(self._device.get_reflectivity)
        DataLogger.add_to_queue(CSVData(self.uid, self._identifier, LINE_REFLECTIVITY, value))
        
############################################################################################
#TODO: Test with real bricklet  Linear Poti
from tinkerforge.bricklet_linear_poti import BrickletLinearPoti
LINEAR_POTI = "Linear Poti"
LINEAR_POTI_POSITION = "Position"
LINEAR_POTI_ANALOG_VALUE = "Analog Value"
LINEAR_POTI_CLASS = "BrickletLinearPoti"
class LinearPotiBricklet(AbstractDevice):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = BrickletLinearPoti(self.uid, DataLogger.ipcon)
        self._data = data
        self._identifier = BrickletLinearPoti.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        
        value1 = DataLogger.parse_to_int(self._data[LINEAR_POTI_POSITION])   
        value2 = DataLogger.parse_to_int(self._data[LINEAR_POTI_ANALOG_VALUE]) 
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_position)) 
        LoggerTimer.Timers.append(LoggerTimer(value2, self._timer_analog_value)) 

    def _timer_position(self):
        value = self._try_catch(self._device.get_position)
        DataLogger.add_to_queue(CSVData(self.uid, self._identifier, LINEAR_POTI_POSITION, value))

    def _timer_analog_value(self):
        value = self._try_catch(self._device.get_analog_value)
        DataLogger.add_to_queue(CSVData(self.uid, self._identifier, LINEAR_POTI_ANALOG_VALUE, value))

############################################################################################
#TODO: Test with real bricklet  Moisture
from tinkerforge.bricklet_moisture import Moisture
MOISTURE = "Moisture"
MOISTURE_MOISTURE_VALUE = "Moisture Value"
MOISTURE_CLASS = "Moisture"
class MoistureBricklet(AbstractDevice):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = Moisture(self.uid, DataLogger.ipcon)
        self._data = data
        self._identifier = Moisture.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        
        value1 = DataLogger.parse_to_int(self._data[MOISTURE_MOISTURE_VALUE])  
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_moisture_value)) 

    def _timer_moisture_value(self):
        value = self._try_catch(self._device.get_moisture_value)
        DataLogger.add_to_queue(CSVData(self.uid, self._identifier, MOISTURE_MOISTURE_VALUE, value))

############################################################################################
#TODO: Test with real bricklet  Motion Detector
from tinkerforge.bricklet_motion_detector import MotionDetector
MOTION_DETECTOR = "Motion Detector"
MOTION_DETECTOR_MOTION_DETECTED = "Motion Detected"
MOTION_DETECTOR_CLASS = "MotionDetector"
class MotionDetectorBricklet(AbstractDevice):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = MotionDetector(self.uid, DataLogger.ipcon)
        self._data = data
        self._identifier = MotionDetector.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self)
        
        value1 = DataLogger.parse_to_int(self._data[MOTION_DETECTOR_MOTION_DETECTED])  
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_motion_detected)) 

    def _timer_motion_detected(self):
        value = self._try_catch(self._device.get_motion_detected)
        DataLogger.add_to_queue(CSVData(self.uid, self._identifier, MOTION_DETECTOR_MOTION_DETECTED, value))

############################################################################################
#TODO: Test with real bricklet  Multi Touch
from tinkerforge.bricklet_multi_touch import MultiTouch
MULTI_TOUCH = "Multi Touch"
MULTI_TOUCH_TOUCH_STATE = "Touch State"
MULTI_TOUCH_CLASS = "MultiTouch"
class MultiTouchBricklet(AbstractDevice):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = MultiTouch(self.uid, DataLogger.ipcon)
        self._data = data
        self._identifier = MultiTouch.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        
        value1 = DataLogger.parse_to_int(self._data[MULTI_TOUCH_TOUCH_STATE])  
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_touch_state)) 

    def _timer_touch_state(self):
        value = self._try_catch(self._device.get_touch_state)
        DataLogger.add_to_queue(CSVData(self.uid, self._identifier, MULTI_TOUCH_TOUCH_STATE, value))

############################################################################################
#TODO: Test with real bricklet  NFC/RFID
#TODO: LCD NFC/RFID - variables? Dont know how to log this bricklet!
from tinkerforge.bricklet_nfc_rfid import BrickletNFCRFID
NFC_RFID = "NFC RFID"
#NFC_RFID_STATE = "State"
NFC_RFID_CLASS = "BrickletNFCRFID"
class NFCRFIDBricklet(AbstractDevice):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = BrickletNFCRFID(self.uid, DataLogger.ipcon)
        self._data = data
        self._identifier = BrickletNFCRFID.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        logging.warning("The NFCRFIDBricklet is not supported for Logging actions!")

############################################################################################
#TODO: Test with real bricklet  Piezo Buzzer
#TODO: Piezo Buzzer - variables? Dont know how to log this bricklet!
from tinkerforge.bricklet_piezo_buzzer import BrickletPiezoBuzzer
PIEZO_BUZZER = "Pirezo Buzzer"
PIEZO_BUZZER_CLASS = "BrickletPiezoBuzzer"
class PiezoBuzzerBricklet(AbstractDevice):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = BrickletPiezoBuzzer(self.uid, DataLogger.ipcon)
        self._data = data
        self._identifier = BrickletPiezoBuzzer.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        logging.warning("The PiezoBuzzerBricklet is not supported for Logging actions!")

############################################################################################
#TODO: Test with real bricklet  Piezo Speaker
#TODO: Piezo Speaker - variables? Dont know how to log this bricklet!
from tinkerforge.bricklet_piezo_speaker import PiezoSpeaker
PIEZO_SPEAKER = "Piezo Speaker"
PIEZO_SPEAKER_CLASS = "PiezoSpeaker"
class PiezoSpeakerBricklet(AbstractDevice):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = PiezoSpeaker(self.uid, DataLogger.ipcon)
        self._data = data
        self._identifier = PiezoSpeaker.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        logging.warning("The PiezoSpeakerBricklet is not supported for Logging actions!")        

############################################################################################
#TODO: Test with real bricklet  PTC
from tinkerforge.bricklet_ptc import PTC
PTC_BRICKLET = "PTC"
PTC_BRICKLET_TEMPERATURE = "Temperature"
PTC_BRICKLET_RESISTANCE = "Resistance"
PTC_BRICKLET_CLASS = "PTC"
class PTCBricklet(AbstractDevice):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = PTC(self.uid, DataLogger.ipcon)
        self._data = data
        self._identifier = PTC.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
         
        value1 = DataLogger.parse_to_int(self._data[PTC_BRICKLET_TEMPERATURE])  
        value2 = DataLogger.parse_to_int(self._data[PTC_BRICKLET_RESISTANCE])  
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_temeperature)) 
        LoggerTimer.Timers.append(LoggerTimer(value2, self._timer_resistance)) 

    def _timer_temeperature(self):
        value = self._try_catch(self._device.get_temperature)
        DataLogger.add_to_queue(CSVData(self.uid, self._identifier, PTC_BRICKLET_TEMPERATURE, value))
        
    def _timer_resistance(self):
        value = self._try_catch(self._device.get_resistance)
        DataLogger.add_to_queue(CSVData(self.uid, self._identifier, PTC_BRICKLET_RESISTANCE, value))

############################################################################################
#TODO: Test with real bricklet  Remote Switch
#TODO: Remote Switch - variables? Dont know how to log this bricklet!
from tinkerforge.bricklet_remote_switch import RemoteSwitch
REMOTE_SWITCH = "Remote Switch"
REMOTE_SWITCH_CLASS = "RemoteSwitch"
class RemoteSwitchBricklet(AbstractDevice):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = RemoteSwitch(self.uid, DataLogger.ipcon)
        self._data = data
        self._identifier = RemoteSwitch.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        logging.warning("The RemoteSwitchBricklet is not supported for Logging actions!")  

############################################################################################
#TODO: Test with real bricklet  Rotary Encoder
from tinkerforge.bricklet_rotary_encoder import RotaryEncoder
ROTARY_ENCODER = "Rotary Encoder"
ROTARY_ENCODER_COUNT = "Count"
ROTARY_ENCODER_PRESSED = "Pressed"
ROTARY_ENCODER_CLASS = "RotaryEncoder"
class RotaryEncoderBricklet(AbstractDevice):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = RotaryEncoder(self.uid, DataLogger.ipcon)
        self._data = data
        self._identifier = RotaryEncoder.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) #get_count(false)
        
        value1 = DataLogger.parse_to_int(self._data[ROTARY_ENCODER_COUNT])  
        value2 = DataLogger.parse_to_int(self._data[ROTARY_ENCODER_PRESSED])  
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_count)) 
        LoggerTimer.Timers.append(LoggerTimer(value2, self._timer_pressed)) 

    def _timer_count(self):
        try:
            value = self._device.get_count(False)
            DataLogger.add_to_queue(CSVData(self.uid, self._identifier, ROTARY_ENCODER_COUNT, value))
        except Exception as e:
            DataLogger.add_to_queue(CSVData(self.uid, self._identifier, ROTARY_ENCODER_COUNT, self._exception_msg(e.value, e.description)))

    def _timer_pressed(self):
        value = self._try_catch(self._device.is_pressed)
        DataLogger.add_to_queue(CSVData(self.uid, self._identifier, ROTARY_ENCODER_PRESSED, value))

############################################################################################
#TODO: Test with real bricklet  Rotary Poti
from tinkerforge.bricklet_rotary_poti import RotaryPoti
ROTARY_POTI = "Rotary Poti"
ROTARY_POTI_POSITION = "Position"
ROTARY_POTI_ANALOG_VALUE = "Analog Value"
ROTARY_POTI_CLASS = "RotaryPoti"
class RotaryPotiBricklet(AbstractDevice):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = RotaryPoti(self.uid, DataLogger.ipcon)
        self._data = data
        self._identifier = RotaryPoti.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        
        value1 = DataLogger.parse_to_int(self._data[ROTARY_POTI_POSITION])  
        value2 = DataLogger.parse_to_int(self._data[ROTARY_POTI_ANALOG_VALUE])  
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_position)) 
        LoggerTimer.Timers.append(LoggerTimer(value2, self._timer_analog_value)) 
        
    def _timer_position(self):
        value = self._try_catch(self._device.get_position)
        DataLogger.add_to_queue(CSVData(self.uid, self._identifier, ROTARY_POTI_POSITION, value))
    
    def _timer_analog_value(self):
        value = self._try_catch(self._device.get_analog_value)
        DataLogger.add_to_queue(CSVData(self.uid, self._identifier, ROTARY_POTI_ANALOG_VALUE, value))

############################################################################################
#TODO: Test with real bricklet  Segment Display 4x7
from tinkerforge.bricklet_segment_display_4x7 import BrickletSegmentDisplay4x7 
SEGMENT_DISPLAY_4x7 = "Segment Display 4x7"
SEGMENT_DISPLAY_4x7_SEGMENTS = "Segments"
SEGMENT_DISPLAY_4x7_SEGMENT_1 = "Segment 1"
SEGMENT_DISPLAY_4x7_SEGMENT_2 = "Segment 2"
SEGMENT_DISPLAY_4x7_SEGMENT_3 = "Segment 3"
SEGMENT_DISPLAY_4x7_SEGMENT_4 = "Segment 4"
SEGMENT_DISPLAY_4x7_BRIGTHNESS = "Brightness"
SEGMENT_DISPLAY_4x7_COLON = "Colon"
SEGMENT_DISPLAY_4x7_COUNTER_VALUE = "Counter Value"
SEGMENT_DISPLAY_4x7_CLASS = "BrickletSegmentDisplay4x7"
class SegmentDisplay4x7Bricklet(AbstractDevice):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = BrickletSegmentDisplay4x7(self.uid, DataLogger.ipcon)
        self._data = data
        self._identifier = BrickletSegmentDisplay4x7.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        
        value1 = DataLogger.parse_to_int(self._data[SEGMENT_DISPLAY_4x7_SEGMENTS])  
        value2 = DataLogger.parse_to_int(self._data[SEGMENT_DISPLAY_4x7_COUNTER_VALUE])  
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_segments)) 
        LoggerTimer.Timers.append(LoggerTimer(value2, self._timer_counter_value)) 

    def _timer_segments(self):
        try:
            segment, brightness, colon = self._device.get_segments()
            #segment, brightness, colon = self.__TEMP_GET_SEGMENTS()#TODO: debug only
            if DataLogger.parse_to_bool(self._data[SEGMENT_DISPLAY_4x7_SEGMENT_1]):
                DataLogger.add_to_queue(CSVData(self.uid, self._identifier, SEGMENT_DISPLAY_4x7_SEGMENT_1, segment[0]))
            if DataLogger.parse_to_bool(self._data[SEGMENT_DISPLAY_4x7_SEGMENT_2]):
                DataLogger.add_to_queue(CSVData(self.uid, self._identifier, SEGMENT_DISPLAY_4x7_SEGMENT_2, segment[1]))
            if DataLogger.parse_to_bool(self._data[SEGMENT_DISPLAY_4x7_SEGMENT_3]):
                DataLogger.add_to_queue(CSVData(self.uid, self._identifier, SEGMENT_DISPLAY_4x7_SEGMENT_3, segment[2]))
            if DataLogger.parse_to_bool(self._data[SEGMENT_DISPLAY_4x7_SEGMENT_4]):
                DataLogger.add_to_queue(CSVData(self.uid, self._identifier, SEGMENT_DISPLAY_4x7_SEGMENT_4, segment[3]))
            if DataLogger.parse_to_bool(self._data[SEGMENT_DISPLAY_4x7_BRIGTHNESS]):
                DataLogger.add_to_queue(CSVData(self.uid, self._identifier, SEGMENT_DISPLAY_4x7_BRIGTHNESS, brightness))
            if DataLogger.parse_to_bool(self._data[SEGMENT_DISPLAY_4x7_COLON]):
                DataLogger.add_to_queue(CSVData(self.uid, self._identifier, SEGMENT_DISPLAY_4x7_COLON, colon))        
        except Exception as e:
            DataLogger.add_to_queue(CSVData(self.uid, self._identifier, SEGMENT_DISPLAY_4x7_SEGMENTS, self._exception_msg(e.value, e.description)))

    def _timer_counter_value(self):
        value = self._try_catch(self._device.get_counter_value)
        DataLogger.add_to_queue(CSVData(self.uid, self._identifier, SEGMENT_DISPLAY_4x7_COUNTER_VALUE, value))

    def __TEMP_GET_SEGMENTS(self):
        #([int, int, int, int], int, bool)
        #segments, brightness und colon.
        return ([1,2,3,4], 50, False)

############################################################################################
#TODO: Test with real bricklet  Solid State Relay
from tinkerforge.bricklet_solid_state_relay import BrickletSolidStateRelay
SOLID_STATE_RELAY = "Solid State Relay"
SOLID_STATE_RELAY_STATE = "State"
SOLID_STATE_RELAY_CLASS = "BrickletSolidStateRelay"
class SolidStateRelayBricklet(AbstractDevice):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = BrickletSolidStateRelay(self.uid, DataLogger.ipcon)
        self._data = data
        self._identifier = BrickletSolidStateRelay.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 

        value1 = DataLogger.parse_to_int(self._data[SOLID_STATE_RELAY_STATE])  
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_state)) 
        
    def _timer_state(self):
        value = self._try_catch(self._device.get_state)
        DataLogger.add_to_queue(CSVData(self.uid, self._identifier, SOLID_STATE_RELAY_STATE, value))

############################################################################################
#TODO: Test with real bricklet  Sound Intensity
from tinkerforge.bricklet_sound_intensity import BrickletSoundIntensity
SOUND_INTENSITY = "Sound Intensity"
SOUND_INTENSITY_INTENSITY = "Intensity"
SOUND_INTENSITY_CLASS = "BrickletSoundIntensity"
class SoundIntensityBricklet(AbstractDevice):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = BrickletSoundIntensity(self.uid, DataLogger.ipcon)
        self._data = data
        self._identifier = BrickletSoundIntensity.DEVICE_IDENTIFIER 
        

    def start_timer(self):#get_intensity
        AbstractDevice.start_timer(self) 
        
        value1 = DataLogger.parse_to_int(self._data[SOUND_INTENSITY_INTENSITY])  
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_intensity)) 
        
    def _timer_intensity(self):
        value = self._try_catch(self._device.get_intensity)
        DataLogger.add_to_queue(CSVData(self.uid, self._identifier, SOUND_INTENSITY_INTENSITY, value))

############################################################################################
#TODO: Test with real bricklet  Temperature
from tinkerforge.bricklet_temperature import BrickletTemperature
TEMPERATURE = "Temperature"
TEMPERATURE_TEMPERATURE = "Temperature"
TEMPERATURE_CLASS = "BrickletTemperature"
class TemperatureBricklet(AbstractDevice):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = BrickletTemperature(self.uid, DataLogger.ipcon)
        self._data = data
        self._identifier = BrickletTemperature.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        
        value1 = DataLogger.parse_to_int(self._data[TEMPERATURE_TEMPERATURE])  
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_temperature)) 
        
    def _timer_temperature(self):
        value = self._try_catch(self._device.get_temperature)
        DataLogger.add_to_queue(CSVData(self.uid, self._identifier, TEMPERATURE_TEMPERATURE, value))

############################################################################################
#TODO: Temperature IR
from tinkerforge.bricklet_temperature_ir import BrickletTemperatureIR
TEMPERATURE_IR = "Temperature IR"
TEMPERATURE_IR_AMBIENT_TEMPERATURE = "Ambient Temperature"
TEMPERATURE_IR_OBJECT_TEMPERATURE ="Object Temperature"
TEMPERATURE_IR_CLASS = "BrickletTemperatureIR"
class TemperatureIRBricklet(AbstractDevice):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = BrickletTemperatureIR(self.uid, DataLogger.ipcon)
        self._data = data
        self._identifier = BrickletTemperatureIR.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        
        value1 = DataLogger.parse_to_int(self._data[TEMPERATURE_IR_AMBIENT_TEMPERATURE])  
        value2 = DataLogger.parse_to_int(self._data[TEMPERATURE_IR_OBJECT_TEMPERATURE])  
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_ambient_temperature)) 
        LoggerTimer.Timers.append(LoggerTimer(value2, self._timer_object_temperature))
        
    def _timer_ambient_temperature(self):
        value = self._try_catch(self._device.get_ambient_temperature)
        DataLogger.add_to_queue(CSVData(self.uid, self._identifier, TEMPERATURE_IR_AMBIENT_TEMPERATURE, value))
        
    def _timer_object_temperature(self):
        value = self._try_catch(self._device.get_object_temperature)
        DataLogger.add_to_queue(CSVData(self.uid, self._identifier, TEMPERATURE_IR_OBJECT_TEMPERATURE, value))

############################################################################################
#TODO: Test with real bricklet  Tilt
from tinkerforge.bricklet_tilt import BrickletTilt
TILT = "Tilt"
TILT_STATE = "State"
TILT_CLASS = "BrickletTilt"
class TiltBricklet(AbstractDevice):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = BrickletTilt(self.uid, DataLogger.ipcon)
        self._data = data
        self._identifier = BrickletTilt.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        
        value1 = DataLogger.parse_to_int(self._data[TILT_STATE])  
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_state))
        
    def _timer_state(self):
        value = self._try_catch(self._device.get_tilt_state)
        DataLogger.add_to_queue(CSVData(self.uid, self._identifier, TILT_STATE, value))

############################################################################################
#TODO: Test with real bricklet  Voltage
from tinkerforge.bricklet_voltage import BrickletVoltage
VOLTAGE = "Voltage"
VOLTAGE_VOLTAGE = "Voltage"
VOLTAGE_ANALOG_VALUE = "Analog Value"
VOLTAGE_CLASS = "BrickletVoltage"
class VoltageBricklet(AbstractDevice):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = BrickletVoltage(self.uid, DataLogger.ipcon)
        self._data = data
        self._identifier = BrickletVoltage.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        
        value1 = DataLogger.parse_to_int(self._data[VOLTAGE_VOLTAGE])  
        value2 = DataLogger.parse_to_int(self._data[VOLTAGE_ANALOG_VALUE])  
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_voltage)) 
        LoggerTimer.Timers.append(LoggerTimer(value2, self._timer_analog_value))
        
    def _timer_voltage(self):
        value = self._try_catch(self._device.get_voltage)
        DataLogger.add_to_queue(CSVData(self.uid, self._identifier, VOLTAGE_VOLTAGE, value))
        
    def _timer_analog_value(self):
        value = self._try_catch(self._device.get_analog_value)
        DataLogger.add_to_queue(CSVData(self.uid, self._identifier, VOLTAGE_ANALOG_VALUE, value))

############################################################################################
#TODO: Test with real bricklet  Voltage/Current
from tinkerforge.bricklet_voltage_current import BrickletVoltageCurrent
VOLTAGE_CURRENT = "Voltage Current"
VOLTAGE_CURRENT_CURRENT = "Current"
VOLTAGE_CURRENT_VOLTAGE = "Voltage"
VOLTAGE_CURRENT_POWER = "Power"
VOLTAGE_CURRENT_CLASS = "BrickletVoltageCurrent"
class VoltageCurrentBricklet(AbstractDevice):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = BrickletVoltageCurrent(self.uid, DataLogger.ipcon)
        self._data = data
        self._identifier = BrickletVoltageCurrent.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        
        value1 = DataLogger.parse_to_int(self._data[VOLTAGE_CURRENT_CURRENT])  
        value2 = DataLogger.parse_to_int(self._data[VOLTAGE_CURRENT_VOLTAGE])  
        value3 = DataLogger.parse_to_int(self._data[VOLTAGE_CURRENT_POWER])
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_current)) 
        LoggerTimer.Timers.append(LoggerTimer(value2, self._timer_voltage))
        LoggerTimer.Timers.append(LoggerTimer(value3, self._timer_power))
        
    def _timer_current(self):
        value = self._try_catch(self._device.get_current)
        DataLogger.add_to_queue(CSVData(self.uid, self._identifier, VOLTAGE_CURRENT_CURRENT, value))
        
    def _timer_voltage(self):
        value = self._try_catch(self._device.get_voltage)
        DataLogger.add_to_queue(CSVData(self.uid, self._identifier, VOLTAGE_CURRENT_VOLTAGE, value))
        
    def _timer_power(self):
        value = self._try_catch(self._device.get_power)
        DataLogger.add_to_queue(CSVData(self.uid, self._identifier, VOLTAGE_CURRENT_POWER, value))
        
#ALL BRICKS + FUNCTIONS#####################################################################

############################################################################################
#TODO: Test with real brick  DC
from tinkerforge.brick_dc import DC
DC_BRICK = "Dc"
DC_CURRENT_VELOCITY = "Current Velocity"
DC_IS_ENABLED = "Is Enabled"
DC_STACK_INPUT_VOLTAGE = "Stack Input Voltage"
DC_EXTERNAL_INPUT_VOLTAGE = "External Input Voltage"
DC_CURRENT_CONSUMPTION = "Current Consumption"
DC_BRICK_CLASS = "DC"
class DCBrick(AbstractDevice):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = DC(self.uid, DataLogger.ipcon)
        self._data = data
        self._identifier = DC.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        
        value1 = DataLogger.parse_to_int(self._data[DC_CURRENT_VELOCITY])  
        value2 = DataLogger.parse_to_int(self._data[DC_IS_ENABLED])  
        value3 = DataLogger.parse_to_int(self._data[DC_STACK_INPUT_VOLTAGE])
        value4 = DataLogger.parse_to_int(self._data[DC_EXTERNAL_INPUT_VOLTAGE])
        value5 = DataLogger.parse_to_int(self._data[DC_CURRENT_CONSUMPTION])
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_current_velocity)) 
        LoggerTimer.Timers.append(LoggerTimer(value2, self._timer_is_enabled))
        LoggerTimer.Timers.append(LoggerTimer(value3, self._timer_stack_input_voltage))
        LoggerTimer.Timers.append(LoggerTimer(value4, self._timer_external_input_voltage))
        LoggerTimer.Timers.append(LoggerTimer(value5, self.current_consumption_timer_current))
        
    def _timer_current_velocity(self):
        value = self._try_catch(self._device.get_current_velocity)
        DataLogger.add_to_queue(CSVData(self.uid, self._identifier, DC_CURRENT_VELOCITY, value))
        
    def _timer_is_enabled(self):
        value = self._try_catch(self._device.is_enabled)
        DataLogger.add_to_queue(CSVData(self.uid, self._identifier, DC_IS_ENABLED, value))
    
    def _timer_stack_input_voltage(self):
        value = self._try_catch(self._device.get_stack_input_voltage)
        DataLogger.add_to_queue(CSVData(self.uid, self._identifier, DC_STACK_INPUT_VOLTAGE, value))
        
    def _timer_external_input_voltage(self):
        value = self._try_catch(self._device.get_external_input_voltage)
        DataLogger.add_to_queue(CSVData(self.uid, self._identifier, DC_EXTERNAL_INPUT_VOLTAGE, value))
        
    def current_consumption_timer_current(self):
        value = self._try_catch(self._device.get_current_consumption)
        DataLogger.add_to_queue(CSVData(self.uid, self._identifier, DC_CURRENT_CONSUMPTION, value))
        
############################################################################################
#TODO: Test with real brick  IMU
from tinkerforge.brick_imu import IMU
IMU_BRICK = "Imu"
IMU_ORIENTATION = "Orientation"
IMU_ORIENTATION_ROLL = " Roll"
IMU_ORIENTATION_PITCH = " Pitch"
IMU_ORIENTATION_YAW = "Yaw"
class IMUBrick(AbstractDevice):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = IMU(self.uid, DataLogger.ipcon)
        self._data = data
        self._identifier = IMU.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        
        value1 = DataLogger.parse_to_int(self._data[IMU_ORIENTATION])
        value2 = DataLogger.parse_to_int(self._data[IMU_ORIENTATION])
        value3 = DataLogger.parse_to_int(self._data[IMU_ORIENTATION])
        value4 = DataLogger.parse_to_int(self._data[IMU_ORIENTATION])
        value5 = DataLogger.parse_to_int(self._data[IMU_ORIENTATION])
        value6 = DataLogger.parse_to_int(self._data[IMU_ORIENTATION])
        value7 = DataLogger.parse_to_int(self._data[IMU_ORIENTATION])
        value8 = DataLogger.parse_to_int(self._data[IMU_ORIENTATION])
        value9 = DataLogger.parse_to_int(self._data[IMU_ORIENTATION])
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_orientation))
        LoggerTimer.Timers.append(LoggerTimer(value2, self._timer_orientation))
        LoggerTimer.Timers.append(LoggerTimer(value3, self._timer_orientation))
        LoggerTimer.Timers.append(LoggerTimer(value4, self._timer_orientation))
        LoggerTimer.Timers.append(LoggerTimer(value5, self._timer_orientation))
        LoggerTimer.Timers.append(LoggerTimer(value6, self._timer_orientation))
        LoggerTimer.Timers.append(LoggerTimer(value7, self._timer_orientation))
        LoggerTimer.Timers.append(LoggerTimer(value8, self._timer_orientation))
        LoggerTimer.Timers.append(LoggerTimer(value9, self._timer_orientation))
        
        
    def _timer_orientation(self):
        try:
            roll, pitch, yaw = self._device.get_orientation()
            if DataLogger.parse_to_bool(self._data[IMU_ORIENTATION_ROLL]):
                DataLogger.add_to_queue(CSVData(self.uid, self._identifier, IMU_ORIENTATION_ROLL, roll))
            if DataLogger.parse_to_bool(self._data[IMU_ORIENTATION_PITCH]):
                DataLogger.add_to_queue(CSVData(self.uid, self._identifier, IMU_ORIENTATION_PITCH, pitch))
            if DataLogger.parse_to_bool(self._data[IMU_ORIENTATION_YAW]):
                DataLogger.add_to_queue(CSVData(self.uid, self._identifier, IMU_ORIENTATION_YAW, yaw))
            
        except Exception as e:
            DataLogger.add_to_queue(CSVData(self.uid, self._identifier, IMU_ORIENTATION, self._exception_msg(e.value, e.description)))
    
    def _timer_o2rientation(self):
        value = self._try_catch(self._device.get_orientation)
        DataLogger.add_to_queue(CSVData(self.uid, self._identifier, IMU_ORIENTATION, value))
        try:
            pass
        except Exception as e:
            DataLogger.add_to_queue(CSVData(self.uid, self._identifier, IMU_ORIENTATION, self._exception_msg(e.value, e.description)))
     