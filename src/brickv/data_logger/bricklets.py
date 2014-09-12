from brickv.data_logger.utils import LoggerTimer   #Timer for getVariable
from brickv.data_logger.utils import DataLogger    #gloabl thread/job queue -> brickelts callbacks/timer
from brickv.data_logger.utils import CSVData       #bricklets

import logging

#TODO: DBG ONLY!
class TEMP_EXCEPTION(Exception):
    
    def __init__(self, value, desc):
        self.value = value
        self.description = desc

###Bricklets and Variables###

#ALL BRICKLETS + FUNCTIONS##################################################################
class AbstractBricklet(object):
    """DEBUG and Inheritance only class"""
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = None
        self._data = data


    def start_timer(self):
        logging.debug("[" + self.__str__() + " | <data="+ str(self._data) +">]")
                
        
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
        return "Bricklet=" + str(type(self)) + " | <UID="+ self.uid +">"
    
############################################################################################
#Ambient Light
from tinkerforge.bricklet_ambient_light import AmbientLight
AMBIENT_LIGHT = "Ambient Light"
AMBIENT_LIGHT_ILLUMINANCE = "Illuminance"
AMBIENT_LIGHT_ANALOG_VALUE = "Analog Value"
class AmbientLightBricklet(AbstractBricklet):
    
    def __init__(self, uid, data):
        self.uid = uid  
        self._device = AmbientLight(self.uid, DataLogger.ipcon)
        self._data = data


    def start_timer(self):
        AbstractBricklet.start_timer(self)
                
        value1 = DataLogger.parse_to_int(self._data[AMBIENT_LIGHT_ANALOG_VALUE])
        value2 = DataLogger.parse_to_int(self._data[AMBIENT_LIGHT_ILLUMINANCE])     
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_analog_value))      
        LoggerTimer.Timers.append(LoggerTimer(value2, self._timer_illuminance))

    def _timer_analog_value(self):        
        value = self._try_catch(self._device.get_analog_value)
        csv = CSVData(self.uid, AMBIENT_LIGHT, AMBIENT_LIGHT_ANALOG_VALUE, value)
        DataLogger.add_to_queue(csv)
        
    def _timer_illuminance(self):
        value = self._try_catch(self._device.get_illuminance)
        csv = CSVData(self.uid, AMBIENT_LIGHT, AMBIENT_LIGHT_ILLUMINANCE, value)
        DataLogger.add_to_queue(csv)  

############################################################################################
#Analog In          
#TODO: Test with real bricklet                      
from tinkerforge.bricklet_analog_in import AnalogIn
ANALOG_IN = "Analog In"
ANALOG_IN_VOLTAGE = "Voltage"
ANALOG_IN_ANALOG_VALUE = "Analog Value"
class AnalogInBricklet(AbstractBricklet):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = AnalogIn(self.uid, DataLogger.ipcon)
        self._data = data


    def start_timer(self):  
        AbstractBricklet.start_timer(self)
              
        value1 = DataLogger.parse_to_int(self._data[ANALOG_IN_ANALOG_VALUE])
        value2 = DataLogger.parse_to_int(self._data[ANALOG_IN_VOLTAGE])
              
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_analog_value))  
        LoggerTimer.Timers.append(LoggerTimer(value2, self._timer_voltage))

    def _timer_analog_value(self):
        value = self._try_catch(self._device.get_analog_value)
        csv = CSVData(self.uid, ANALOG_IN, ANALOG_IN_ANALOG_VALUE, value)
        DataLogger.add_to_queue(csv)
        
    def _timer_voltage(self):
        value = self._try_catch(self._device.get_voltage)
        csv = CSVData(self.uid, ANALOG_IN, ANALOG_IN_VOLTAGE, value)
        DataLogger.add_to_queue(csv)  

############################################################################################
#Analog Out
#TODO: Test with real bricklet  
from tinkerforge.bricklet_analog_out import AnalogOut
ANALOG_OUT = "Analog Out"
ANALOG_OUT_VOLTAGE = "Voltage"
class AnalogOutBricklet(AbstractBricklet):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = AnalogOut(self.uid, DataLogger.ipcon)
        self._data = data


    def start_timer(self):   
        AbstractBricklet.start_timer(self)
             
        value1 = DataLogger.parse_to_int(self._data[ANALOG_OUT_VOLTAGE]) 
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_voltage))         

    def _timer_voltage(self):
        value = self._try_catch(self._device.get_voltage)
        csv = CSVData(self.uid, ANALOG_OUT, ANALOG_OUT_VOLTAGE, value)
        DataLogger.add_to_queue(csv)

############################################################################################
#Barometer
from tinkerforge.bricklet_barometer import Barometer
BAROMETER = "Barometer"
BAROMETER_AIR_PRESSURE = "Air Pressure"
BAROMETER_ALTITUDE = "Altitude"
BAROMETER_CHIP_TEMPERATURE = "Chip Temperature"
class BarometerBricklet(AbstractBricklet):
    #chip_temperature()
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = Barometer(self.uid, DataLogger.ipcon)
        self._data = data


    def start_timer(self):        
        AbstractBricklet.start_timer(self)
        
        value1 = DataLogger.parse_to_int(self._data[BAROMETER_AIR_PRESSURE])
        value2 = DataLogger.parse_to_int(self._data[BAROMETER_ALTITUDE])      
        value3 = DataLogger.parse_to_int(self._data[BAROMETER_CHIP_TEMPERATURE])  
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_air_pressure))
        LoggerTimer.Timers.append(LoggerTimer(value2, self._timer_altitude))
        LoggerTimer.Timers.append(LoggerTimer(value3, self._timer_chip_temperature))

    def _timer_air_pressure(self):
        value = self._try_catch(self._device.get_air_pressure)
        csv = CSVData(self.uid, BAROMETER, BAROMETER_AIR_PRESSURE, value)
        DataLogger.add_to_queue(csv)
        
    def _timer_altitude(self):
        value = self._try_catch(self._device.get_altitude)
        csv = CSVData(self.uid, BAROMETER, BAROMETER_ALTITUDE, value)
        DataLogger.add_to_queue(csv)  
         
    def _timer_chip_temperature(self):
        value = self._try_catch(self._device.get_chip_temperature)
        csv = CSVData(self.uid, BAROMETER, BAROMETER_CHIP_TEMPERATURE, value)
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
class ColorBricklet(AbstractBricklet):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = Color(self.uid, DataLogger.ipcon)
        self._data = data


    def start_timer(self):     
        AbstractBricklet.start_timer(self)
        
        value1 = DataLogger.parse_to_int(self._data[COLOR_COLOR])
        value2 = DataLogger.parse_to_int(self._data[COLOR_ILLUMINANCE])
        value3 = DataLogger.parse_to_int(self._data[COLOR_TEMPERATURE])   
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_color))         
        LoggerTimer.Timers.append(LoggerTimer(value2, self._timer_illuminance))
        LoggerTimer.Timers.append(LoggerTimer(value3, self._timer_color_temperature))

    def _timer_color(self):
        try:
            r, g, b, c = self.__TEMP_get_color()#self._device.get_color()
            DataLogger.add_to_queue(CSVData(self.uid, COLOR, COLOR_RED, r))
            DataLogger.add_to_queue(CSVData(self.uid, COLOR, COLOR_GREEN, g))
            DataLogger.add_to_queue(CSVData(self.uid, COLOR, COLOR_BLUE, b))
            DataLogger.add_to_queue(CSVData(self.uid, COLOR, COLOR_CLEAR, c))
        except Exception as e:
            DataLogger.add_to_queue(CSVData(self.uid, COLOR, COLOR_COLOR, self._exception_msg(e.value, e.description)))
        
    def _timer_illuminance(self):
        value = self._try_catch(self._device.get_illuminance)
        csv = CSVData(self.uid, COLOR, COLOR_ILLUMINANCE, value)
        DataLogger.add_to_queue(csv)  
        
    def _timer_color_temperature(self):
        value = self._try_catch(self._device.get_color_temperature)
        csv = CSVData(self.uid, COLOR, COLOR_ILLUMINANCE, value)
        DataLogger.add_to_queue(csv) 
        
    def __TEMP_get_color(self):
        return (10, 20, 30, 40)
    
############################################################################################
#TODO: Test with real bricklet  Current12
from tinkerforge.bricklet_current12 import Current12
CURRENT_12 = "Current 12"
CURRENT_12_CURRENT = "Current"
CURRENT_12_ANALOG_VALUE = "Analog Value"
class Current12Bricklet(AbstractBricklet):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = Current12(self.uid, DataLogger.ipcon)
        self._data = data


    def start_timer(self):
        AbstractBricklet.start_timer(self)  
        
        value1 = DataLogger.parse_to_int(self._data[CURRENT_12_ANALOG_VALUE])
        value2 = DataLogger.parse_to_int(self._data[CURRENT_12_CURRENT])  
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_analog_value))         
        LoggerTimer.Timers.append(LoggerTimer(value2, self._timer_current))  
    
    def _timer_analog_value(self):
        value = self._try_catch(self._device.get_analog_value)
        csv = CSVData(self.uid, CURRENT_12, CURRENT_12_ANALOG_VALUE, value)
        DataLogger.add_to_queue(csv) 
    
    def _timer_current(self):
        value = self._try_catch(self._device.get_current)
        csv = CSVData(self.uid, CURRENT_12, CURRENT_12_CURRENT, value)
        DataLogger.add_to_queue(csv)         

############################################################################################
#TODO: Test with real bricklet  Current25
from tinkerforge.bricklet_current25 import Current25
CURRENT_25 = "Current 25"
CURRENT_25_CURRENT = "Current"
CURRENT_25_ANALOG_VALUE = "Analog Value"
class Current25Bricklet(AbstractBricklet):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = Current25(self.uid, DataLogger.ipcon)
        self._data = data


    def start_timer(self):
        AbstractBricklet.start_timer(self)   
        
        value1 = DataLogger.parse_to_int(self._data[CURRENT_25_ANALOG_VALUE])
        value2 = DataLogger.parse_to_int(self._data[CURRENT_25_CURRENT])  
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_analog_value))         
        LoggerTimer.Timers.append(LoggerTimer(value2, self._timer_current))  
    
    def _timer_analog_value(self):
        value = self._try_catch(self._device.get_analog_value)
        csv = CSVData(self.uid, CURRENT_25, CURRENT_25_ANALOG_VALUE, value)
        DataLogger.add_to_queue(csv) 
        
    def _timer_current(self):
        value = self._try_catch(self._device.get_current)
        csv = CSVData(self.uid, CURRENT_25, CURRENT_25_CURRENT, value)
        DataLogger.add_to_queue(csv) 

############################################################################################
#TODO: Test with real bricklet  Distance IR
from tinkerforge.bricklet_distance_ir import DistanceIR
DISTANCE_IR = "Distance IR"
DISTANCE_IR_DISTANCE = "Distance"
DISTANCE_IR_ANALOG_VALUE = "Analog Value"
class DistanceIRBricklet(AbstractBricklet):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = DistanceIR(self.uid, DataLogger.ipcon)
        self._data = data


    def start_timer(self):
        AbstractBricklet.start_timer(self)   
        
        value1 = DataLogger.parse_to_int(self._data[DISTANCE_IR_ANALOG_VALUE])
        value2 = DataLogger.parse_to_int(self._data[DISTANCE_IR_DISTANCE])  
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_analog_value))         
        LoggerTimer.Timers.append(LoggerTimer(value2, self._timer_distance))  
    
    def _timer_analog_value(self):
        value = self._try_catch(self._device.get_analog_value)
        csv = CSVData(self.uid, DISTANCE_IR, DISTANCE_IR_ANALOG_VALUE, value)
        DataLogger.add_to_queue(csv) 
        
    def _timer_distance(self):
        value = self._try_catch(self._device.get_analog_value)
        csv = CSVData(self.uid, DISTANCE_IR, DISTANCE_IR_DISTANCE, value)
        DataLogger.add_to_queue(csv)

############################################################################################
#TODO: Test with real bricklet  Distance US
from tinkerforge.bricklet_distance_us import DistanceUS
DISTANCE_US = "Distance US"
DISTANCE_US_DISTANCE = "Distance"
class DistanceUSBricklet(AbstractBricklet):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = DistanceUS(self.uid, DataLogger.ipcon)
        self._data = data


    def start_timer(self):
        AbstractBricklet.start_timer(self)   
        
        value1 = DataLogger.parse_to_int(self._data[DISTANCE_US_DISTANCE])
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_distance))   
    
    def _timer_distance(self):
        value = self._try_catch(self._device.get_distance_value)
        csv = CSVData(self.uid, DISTANCE_US, DISTANCE_US_DISTANCE, value)
        DataLogger.add_to_queue(csv) 
        
############################################################################################
#TODO: Test with real bricklet  Dual Button
#TODO: Dual Button variables
from tinkerforge.bricklet_dual_button import DualButton
DUAL_BUTTON = "Dual Button"
DUAL_BUTTON_BUTTONS = "Buttons"
DUAL_BUTTON_BUTTON_L = "button_l"
DUAL_BUTTON_BUTTON_R = "button_r"
DUAL_BUTTON_LEDS = "Leds"
DUAL_BUTTON_LED_L = "led_l"
DUAL_BUTTON_LED_R = "led_r"
class DualButtonBricklet(AbstractBricklet):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = DualButton(self.uid, DataLogger.ipcon)
        self._data = data
        

    def start_timer(self):
        AbstractBricklet.start_timer(self) 
        
        value1 = DataLogger.parse_to_int(self._data[DUAL_BUTTON_BUTTONS])
        value2 = DataLogger.parse_to_int(self._data[DUAL_BUTTON_LEDS])
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_buttons))   
        LoggerTimer.Timers.append(LoggerTimer(value2, self._timer_leds))  
    
    def _timer_buttons(self):
        try:
            button_l, button_r = self._device.get_button_state()
            DataLogger.add_to_queue(CSVData(self.uid, DUAL_BUTTON, DUAL_BUTTON_BUTTON_L, button_l))
            DataLogger.add_to_queue(CSVData(self.uid, DUAL_BUTTON, DUAL_BUTTON_BUTTON_R, button_r))
        except Exception as e:
            DataLogger.add_to_queue(CSVData(self.uid, DUAL_BUTTON, DUAL_BUTTON_BUTTONS, self._exception_msg(e.value, e.description)))

    def _timer_leds(self):
        try:
            led_l, led_r = self._device.get_led_state()
            DataLogger.add_to_queue(CSVData(self.uid, DUAL_BUTTON, DUAL_BUTTON_LED_L, led_l))
            DataLogger.add_to_queue(CSVData(self.uid, DUAL_BUTTON, DUAL_BUTTON_LED_R, led_r))
        except Exception as e:
            DataLogger.add_to_queue(CSVData(self.uid, DUAL_BUTTON, DUAL_BUTTON_LEDS, self._exception_msg(e.value, e.description)))

############################################################################################
#TODO: Test with real bricklet  Dual Relay
#TODO: Dual Relay variables
from tinkerforge.bricklet_dual_relay import DualRelay
DUAL_RELAY = "Dual Relay"
DUAL_RELAY_STATE = "State"
DUAL_RELAY_1 = "relay1"
DUAL_RELAY_2 = "relay2"
class DualRelayBricklet(AbstractBricklet):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = DualRelay(self.uid, DataLogger.ipcon)
        self._data = data
        

    def start_timer(self):
        AbstractBricklet.start_timer(self) 
        
        value1 = DataLogger.parse_to_int(self._data[DUAL_RELAY_STATE])
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_state))  
    
    def _timer_state(self):
        try:
            r1, r2 = self._device.get_state()
            DataLogger.add_to_queue(CSVData(self.uid, DUAL_RELAY, DUAL_RELAY_1, r1))
            DataLogger.add_to_queue(CSVData(self.uid, DUAL_RELAY, DUAL_RELAY_2, r2))
        except Exception as e:
            DataLogger.add_to_queue(CSVData(self.uid, DUAL_RELAY, DUAL_RELAY_STATE, self._exception_msg(e.value, e.description)))

############################################################################################
#TODO: Test with real bricklet  GPS
#TODO: GPS variables
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
GPS_GEOIDAL_SEPERATION = "Geoidal Seperation"
GPS_MOTION = "Motion"
GPS_COURSE = "Course"
GPS_SPEED = "Speed"
GPS_DATE_TIME = "Date Time"
GPS_DATE= "Date"
GPS_TIME = "Time"
class GPSBricklet(AbstractBricklet):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = GPS(self.uid, DataLogger.ipcon)
        self._data = data
        

    def start_timer(self):
        AbstractBricklet.start_timer(self) 
        
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
            fix, satellites_view, satellites_used = self._device.get_status()
            #fix, satellites_view, satellites_used = self.__TMP_get_status()#TODO: TMP ONLY
            DataLogger.add_to_queue(CSVData(self.uid, GPS_BRICKLET, GPS_FIX_STATUS, fix))
            DataLogger.add_to_queue(CSVData(self.uid, GPS_BRICKLET, GPS_SATELLITES_VIEW, satellites_view))
            DataLogger.add_to_queue(CSVData(self.uid, GPS_BRICKLET, GPS_SATELLITES_USED, satellites_used))
              
            if fix == GPS.FIX_NO_FIX:
                DataLogger.add_to_queue(CSVData(self.uid, GPS_BRICKLET, GPS_COORDINATES, self._exception_msg("Fix-Status="+fix, "GPS Fix-Status was 1, but needs to be 2 or 3 for valid Coordinates.")))
                return

            latitude, ns, longitude, ew, pdop, hdop, vdop, epe = self._device.get_coordinates()     
            #latitude, ns, longitude, ew, pdop, hdop, vdop, epe = self.__TMP_get_coordinates()  #TODO: TMP ONLY       
            DataLogger.add_to_queue(CSVData(self.uid, GPS_BRICKLET, GPS_LATITUDE, latitude))
            DataLogger.add_to_queue(CSVData(self.uid, GPS_BRICKLET, GPS_NS, ns))
            DataLogger.add_to_queue(CSVData(self.uid, GPS_BRICKLET, GPS_LONGITUDE, longitude))
            DataLogger.add_to_queue(CSVData(self.uid, GPS_BRICKLET, GPS_EW, ew))
            DataLogger.add_to_queue(CSVData(self.uid, GPS_BRICKLET, GPS_PDOP, pdop))
            DataLogger.add_to_queue(CSVData(self.uid, GPS_BRICKLET, GPS_HDOP, hdop))
            DataLogger.add_to_queue(CSVData(self.uid, GPS_BRICKLET, GPS_VDOP, vdop))
            DataLogger.add_to_queue(CSVData(self.uid, GPS_BRICKLET, GPS_EPE, epe))
        except Exception as e:
            DataLogger.add_to_queue(CSVData(self.uid, GPS_BRICKLET, GPS_COORDINATES, self._exception_msg(e.value, e.description)))

    def _timer_altitude(self):
        try:
            #check for the FIX Value of get_status()
            fix, satellites_view, satellites_used = self._device.get_status()
            DataLogger.add_to_queue(CSVData(self.uid, GPS_BRICKLET, GPS_FIX_STATUS, fix))
            DataLogger.add_to_queue(CSVData(self.uid, GPS_BRICKLET, GPS_SATELLITES_VIEW, satellites_view))
            DataLogger.add_to_queue(CSVData(self.uid, GPS_BRICKLET, GPS_SATELLITES_USED, satellites_used))
              
            if fix != GPS.FIX_3D_FIX:
                DataLogger.add_to_queue(CSVData(self.uid, GPS_BRICKLET, GPS_ALTITUDE, self._exception_msg("Fix-Status="+fix, "GPS Fix-Status was " + fix + ", but needs to be 3 for valid Altitude Values.")))
                return

            altitude, geoidal_separation = self._device.get_altitude()            
            DataLogger.add_to_queue(CSVData(self.uid, GPS_ALTITUDE, GPS_ALTITUDE, altitude))
            DataLogger.add_to_queue(CSVData(self.uid, GPS_ALTITUDE, GPS_GEOIDAL_SEPERATION, geoidal_separation))
        except Exception as e:
            DataLogger.add_to_queue(CSVData(self.uid, GPS_BRICKLET, GPS_ALTITUDE, self._exception_msg(e.value, e.description)))

    def _timer_motion(self):
        try:
            #check for the FIX Value of get_status()
            fix, satellites_view, satellites_used = self._device.get_status()
            DataLogger.add_to_queue(CSVData(self.uid, GPS_BRICKLET, GPS_FIX_STATUS, fix))
            DataLogger.add_to_queue(CSVData(self.uid, GPS_BRICKLET, GPS_SATELLITES_VIEW, satellites_view))
            DataLogger.add_to_queue(CSVData(self.uid, GPS_BRICKLET, GPS_SATELLITES_USED, satellites_used))
              
            if fix == GPS.FIX_NO_FIX:
                DataLogger.add_to_queue(CSVData(self.uid, GPS_BRICKLET, GPS_MOTION, self._exception_msg("Fix-Status="+fix, "GPS Fix-Status was " + fix + ", but needs to be 2 or 3 for valid Altitude Values.")))
                return

            course, speed = self._device.get_motion()
            DataLogger.add_to_queue(CSVData(self.uid, GPS_BRICKLET, GPS_COURSE, course))
            DataLogger.add_to_queue(CSVData(self.uid, GPS_BRICKLET, GPS_SPEED, speed))
        except Exception as e:
            DataLogger.add_to_queue(CSVData(self.uid, GPS_BRICKLET, GPS_MOTION, self._exception_msg(e.value, e.description)))

    def _timer_date_time(self):
        try:
            date, time = self._device.get_date_time()
            DataLogger.add_to_queue(CSVData(self.uid, GPS_BRICKLET, GPS_DATE, date))
            DataLogger.add_to_queue(CSVData(self.uid, GPS_BRICKLET, GPS_TIME, time))
        except Exception as e:
            DataLogger.add_to_queue(CSVData(self.uid, GPS_BRICKLET, GPS_DATE_TIME, self._exception_msg(e.value, e.description)))

    
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
class HallEffectBricklet(AbstractBricklet):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = HallEffect(self.uid, DataLogger.ipcon)
        self._data = data
        

    def start_timer(self):
        AbstractBricklet.start_timer(self) 
        
        value1 = DataLogger.parse_to_int(self._data[HALL_EFFECT_VALUE])
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_value))   
    
    def _timer_value(self):
        value = self._try_catch(self._device.get_value)
        csv = CSVData(self.uid, HALL_EFFECT, HALL_EFFECT_VALUE, value)
        DataLogger.add_to_queue(csv)         

############################################################################################
#Humidity
from tinkerforge.bricklet_humidity import Humidity
HUMIDITY = "Humidity"
HUMIDITY_HUMIDITY = "Humidity"
HUMIDITY_ANALOG_VALUE = "Analog Value"
class HumidityBricklet(AbstractBricklet):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = Humidity(self.uid, DataLogger.ipcon)
        self._data = data
        

    def start_timer(self):
        AbstractBricklet.start_timer(self) 
                
        value1 = DataLogger.parse_to_int(self._data[HUMIDITY_ANALOG_VALUE])
        value2 = DataLogger.parse_to_int(self._data[HUMIDITY_HUMIDITY])       
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_analog_value))         
        LoggerTimer.Timers.append(LoggerTimer(value2, self._timer_humidity))

    def _timer_analog_value(self):
        value = self._try_catch(self._device.get_analog_value)
        csv = CSVData(self.uid, HUMIDITY, HUMIDITY_ANALOG_VALUE, value)
        DataLogger.add_to_queue(csv)
        
    def _timer_humidity(self):
        value = self._try_catch(self._device.get_humidity)
        csv = CSVData(self.uid, HUMIDITY, HUMIDITY_HUMIDITY, value)
        DataLogger.add_to_queue(csv)   

############################################################################################
#TODO: Test with real bricklet  Industrial Digital In 4
#TODO: Industrial Digital In 4  - variables? Dont know how to log this bricklet!
from tinkerforge.bricklet_industrial_digital_in_4 import IndustrialDigitalIn4
INDUSTRIAL_DIGITAL_IN_4 = "Industrial Digital In 4"
class IndustrialDigitalIn4Bricklet(AbstractBricklet):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = IndustrialDigitalIn4(self.uid, DataLogger.ipcon)
        self._data = data
        

    def start_timer(self):
        AbstractBricklet.start_timer(self) 
        logging.warning("The IndustrialDigitalIn4Bricklet is not supported for Logging actions!")

############################################################################################
#TODO: Test with real bricklet  Industrial Digital Out 4
#TODO: Industrial Digital Out 4 - variables? Dont know how to log this bricklet!
from tinkerforge.bricklet_industrial_digital_out_4 import IndustrialDigitalOut4
INDUSTRIAL_DIGITAL_OUT_4 = "Industrial Digital Out 4"
class IndustrialDigitalOut4Bricklet(AbstractBricklet):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = IndustrialDigitalOut4(self.uid, DataLogger.ipcon)
        self._data = data
        

    def start_timer(self):
        AbstractBricklet.start_timer(self) 
        logging.warning("The IndustrialDigitalOut4Bricklet is not supported for Logging actions!")

############################################################################################
#TODO: Test with real bricklet  Industrial Dual 0-20mA
from tinkerforge.bricklet_industrial_dual_0_20ma import IndustrialDual020mA
INDUSTRIAL_DUAL_0_20_MA = "Industrial Dual 0 20 mA"
INDUSTRIAL_DUAL_0_20_MA_CURRENT = "Current"
INDUSTRIAL_DUAL_0_20_MA_SENSOR_0 = "Sensor 0"
INDUSTRIAL_DUAL_0_20_MA_SENSOR_1 = "Sensor 1"
class IndustrialDual020mABricklet(AbstractBricklet):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = IndustrialDual020mA(self.uid, DataLogger.ipcon)
        self._data = data
        

    def start_timer(self):
        AbstractBricklet.start_timer(self) 
        
        value1 = DataLogger.parse_to_int(self._data[INDUSTRIAL_DUAL_0_20_MA_CURRENT])      
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_current))  

    def _timer_current(self):
        try:
            sensor_0 = self._device.get_current(0)
            sensor_1 = self._device.get_current(1)
            
            csv = CSVData(self.uid, INDUSTRIAL_DUAL_0_20_MA, INDUSTRIAL_DUAL_0_20_MA_SENSOR_0, sensor_0)
            DataLogger.add_to_queue(csv)            
            csv = CSVData(self.uid, INDUSTRIAL_DUAL_0_20_MA, INDUSTRIAL_DUAL_0_20_MA_SENSOR_1, sensor_1)
            DataLogger.add_to_queue(csv)

        except Exception as e:
            csv = CSVData(self.uid, INDUSTRIAL_DUAL_0_20_MA, INDUSTRIAL_DUAL_0_20_MA_CURRENT, self._exception_msg(e.value, e.description))
            DataLogger.add_to_queue(csv)

############################################################################################
#TODO: Test with real bricklet  Industrial Quad Relay
#TODO: Industrial Industrial Quad Relay - variables? Dont know how to log this bricklet!
from tinkerforge.bricklet_industrial_quad_relay import IndustrialQuadRelay
INDUSTRIAL_QUAD_RELAY = "Industrial Quad Relay"
class IndustrialQuadRelayBricklet(AbstractBricklet):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = IndustrialQuadRelay(self.uid, DataLogger.ipcon)
        self._data = data
        

    def start_timer(self):
        AbstractBricklet.start_timer(self) 
        logging.warning("The IndustrialQuadRelayBricklet is not supported for Logging actions!")

############################################################################################
#TODO: Test with real bricklet  IO-16
#TODO: IO-16 variables
from tinkerforge.bricklet_io16 import IO16
IO_16 = "IO-16"
IO_16_PORTS = "Ports"
IO_16_PORT_A = "Port A"
IO_16_PORT_B = "Port B"
class IO16Bricklet(AbstractBricklet):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = IO16(self.uid, DataLogger.ipcon)
        self._data = data
        

    def start_timer(self):
        AbstractBricklet.start_timer(self) 
        
        value1 = DataLogger.parse_to_int(self._data[IO_16_PORTS])      
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_ports))  

    def _timer_ports(self):
        try:
            port_a = self._device.get_port('a')
            port_b = self._device.get_port('b')
            
            csv = CSVData(self.uid, IO_16, IO_16_PORT_A, port_a)
            DataLogger.add_to_queue(csv)            
            csv = CSVData(self.uid, IO_16, IO_16_PORT_B, port_b)
            DataLogger.add_to_queue(csv)

        except Exception as e:
            csv = CSVData(self.uid, IO_16, IO_16_PORTS, self._exception_msg(e.value, e.description))
            DataLogger.add_to_queue(csv)

############################################################################################
#TODO: Test with real bricklet  IO-4
#TODO: IO-4 variables
from tinkerforge.bricklet_io4 import IO4
IO_4 = "IO-4"
IO_4_VALUE = "Value"
class IO4Bricklet(AbstractBricklet):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = IO4(self.uid, DataLogger.ipcon)
        self._data = data
        

    def start_timer(self):
        AbstractBricklet.start_timer(self) 
        
        value1 = DataLogger.parse_to_int(self._data[IO_4_VALUE])     
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_value)) 

    def _timer_value(self):
        value = self._try_catch(self._device.get_value)
        csv = CSVData(self.uid, IO_4, IO_4_VALUE, value)
        DataLogger.add_to_queue(csv)

############################################################################################
#TODO: Test with real bricklet  Joystick
from tinkerforge.bricklet_joystick import Joystick
JOYSTICK = "Joystick"
JOYSTICK_POSITION = "Position"
JOYSTICK_POSITION_X = "Position X"
JOYSTICK_POSITION_Y = "Position Y"
JOYSTICK_ANALOG_VALUE = "Analog Value"
JOYSTICK_PRESSED = "Pressed"
class JoystickBricklet(AbstractBricklet):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = Joystick(self.uid, DataLogger.ipcon)
        self._data = data
        

    def start_timer(self):
        AbstractBricklet.start_timer(self) 
        
        value1 = DataLogger.parse_to_int(self._data[JOYSTICK_POSITION])     
        value2 = DataLogger.parse_to_int(self._data[JOYSTICK_ANALOG_VALUE])    
        value3 = DataLogger.parse_to_int(self._data[JOYSTICK_PRESSED])    
        
        LoggerTimer.Timers.append(LoggerTimer(value1, self._timer_position)) 
        LoggerTimer.Timers.append(LoggerTimer(value2, self._timer_analog_value)) 
        LoggerTimer.Timers.append(LoggerTimer(value3, self._timer_is_pressed)) 

    def _timer_position(self):
        try:
            x, y = self._device.get_position()
            
            csv = CSVData(self.uid, JOYSTICK, JOYSTICK_POSITION_X, x)
            DataLogger.add_to_queue(csv)            
            csv = CSVData(self.uid, JOYSTICK, JOYSTICK_POSITION_Y, y)
            DataLogger.add_to_queue(csv)

        except Exception as e:
            csv = CSVData(self.uid, JOYSTICK, JOYSTICK_POSITION, self._exception_msg(e.value, e.description))
            DataLogger.add_to_queue(csv)
        
    def _timer_analog_value(self):
        value = self._try_catch(self._device.get_analog_value)
        csv = CSVData(self.uid, JOYSTICK, JOYSTICK_ANALOG_VALUE, value)
        DataLogger.add_to_queue(csv)
    
    def _timer_is_pressed(self):
        value = self._try_catch(self._device.is_pressed)
        csv = CSVData(self.uid, JOYSTICK, JOYSTICK_PRESSED, value)
        DataLogger.add_to_queue(csv)

############################################################################################
#TODO: Test with real bricklet  LCD 16x2
#TODO: LCD 16x2 - variables? Dont know how to log this bricklet!
from tinkerforge.bricklet_lcd_16x2 import LCD16x2
LCD_16x2 = "LCD 16x2"
class LCD16x2Bricklet(AbstractBricklet):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = LCD16x2(self.uid, DataLogger.ipcon)
        self._data = data
        

    def start_timer(self):
        AbstractBricklet.start_timer(self)         
        logging.warning("The LCD16x2Bricklet is not supported for Logging actions!")

############################################################################################
#TODO: Test with real bricklet  LCD 20x4
#TODO: LCD 20x4 - variables? Dont know how to log this bricklet!
from tinkerforge.bricklet_lcd_20x4 import LCD20x4
LCD_20x4 = "LCD 20x4"
class LCD20x4Bricklet(AbstractBricklet):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = LCD20x4(self.uid, DataLogger.ipcon)
        self._data = data
        

    def start_timer(self):
        AbstractBricklet.start_timer(self)
        logging.warning("The LCD20x4Bricklet is not supported for Logging actions!")

############################################################################################
#TODO: Test with real bricklet  LED Strip
from tinkerforge.bricklet_led_strip import LEDStrip
LED_STRIP = "LED Strip"
LED_STRIP_FRAME_DURATION = "Frame Duration"
LED_STRIP_SUPPLY_VOLTAGE = "Supply Voltage"
LED_STRIP_CLOCK_FEQUENCY = "Clock Frequency"
class LEDStripBricklet(AbstractBricklet):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = LEDStrip(self.uid, DataLogger.ipcon)
        self._data = data
        

    def start_timer(self):
        AbstractBricklet.start_timer(self) 

############################################################################################
#TODO: Test with real bricklet  Line
from tinkerforge.bricklet_line import BrickletLine
LINE = "line"
LINE_REFLECTIVITY = "Reflectivity"
class LineBricklet(AbstractBricklet):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = BrickletLine(self.uid, DataLogger.ipcon)
        self._data = data
        

    def start_timer(self):
        AbstractBricklet.start_timer(self) 

############################################################################################
#TODO: Test with real bricklet  Linear Poti
from tinkerforge.bricklet_linear_poti import BrickletLinearPoti
LINEAR_POTI = "Linear Poti"
LINEAR_POTI_POSITION = "Position"
LINEAR_POTI_ANALOG_VALUE = "Analog Value"
class LinearPotiBricklet(AbstractBricklet):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = BrickletLinearPoti(self.uid, DataLogger.ipcon)
        self._data = data
        

    def start_timer(self):
        AbstractBricklet.start_timer(self) 

############################################################################################
#TODO: Test with real bricklet  Moisture
from tinkerforge.bricklet_moisture import Moisture
MOISTURE = "Moisture"
MOISTURE_MOISTURE_VALUE = "Moisture Value"
class MoistureBricklet(AbstractBricklet):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = Moisture(self.uid, DataLogger.ipcon)
        self._data = data
        

    def start_timer(self):
        AbstractBricklet.start_timer(self) 

############################################################################################
#TODO: Test with real bricklet  Motion Detector
#TODO: Motion Detector variables
from tinkerforge.bricklet_motion_detector import MotionDetector
MOTION_DETECTOR = "Motion Detector"
class MotionDetectorBricklet(AbstractBricklet):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = MotionDetector(self.uid, DataLogger.ipcon)
        self._data = data
        

    def start_timer(self):
        AbstractBricklet.start_timer(self) 

############################################################################################
#TODO: Test with real bricklet  Multi Touch
from tinkerforge.bricklet_multi_touch import MultiTouch
MULTI_TOUCH = "Multi Touch"
MULTI_TOUCH_TOUCH_STATE = "Touch State"
class MultiTouchBricklet(AbstractBricklet):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = MultiTouch(self.uid, DataLogger.ipcon)
        self._data = data
        

    def start_timer(self):
        AbstractBricklet.start_timer(self) 

############################################################################################
#TODO: Test with real bricklet  NFC/RFID
#TODO: LCD NFC/RFID variables
from tinkerforge.bricklet_nfc_rfid import BrickletNFCRFID
NFC_RFID = "NFC RFID"
NFC_RFID_STATE = "State"
class NFCRFIDBricklet(AbstractBricklet):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = BrickletNFCRFID(self.uid, DataLogger.ipcon)
        self._data = data
        

    def start_timer(self):
        AbstractBricklet.start_timer(self) 

############################################################################################
#TODO: Test with real bricklet  Piezo Buzzer
#TODO: Piezo Buzzer variables
from tinkerforge.bricklet_piezo_buzzer import BrickletPiezoBuzzer
PIEZO_BUZZER = "Pirezo Buzzer"
class PiezoBuzzerBricklet(AbstractBricklet):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = BrickletPiezoBuzzer(self.uid, DataLogger.ipcon)
        self._data = data
        

    def start_timer(self):
        AbstractBricklet.start_timer(self) 

############################################################################################
#TODO: Test with real bricklet  Piezo Speaker
#TODO: Piezo Speaker variables
from tinkerforge.bricklet_piezo_speaker import PiezoSpeaker
PIEZO_SPEAKER = "Piezo Speaker"
class PiezoSpeakerBricklet(AbstractBricklet):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = PiezoSpeaker(self.uid, DataLogger.ipcon)
        self._data = data
        

    def start_timer(self):
        AbstractBricklet.start_timer(self) 

############################################################################################
#TODO: Test with real bricklet  PTC
from tinkerforge.bricklet_ptc import PTC
PTC_BRICKLET = "PTC"
PTC_BRICKLET_TEMPERATURE = "Temperature"
PTC_BRICKLET_RESISTANCE = "Resistance"
class PTCBricklet(AbstractBricklet):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = PTC(self.uid, DataLogger.ipcon)
        self._data = data
        

    def start_timer(self):
        AbstractBricklet.start_timer(self) 

############################################################################################
#TODO: Test with real bricklet  Remote Switch
#TODO: Remote Switch variables
from tinkerforge.bricklet_remote_switch import RemoteSwitch
REMOTE_SWITCH = "Remote Switch"
class RemoteSwitchBricklet(AbstractBricklet):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = RemoteSwitch(self.uid, DataLogger.ipcon)
        self._data = data
        

    def start_timer(self):
        AbstractBricklet.start_timer(self) 

############################################################################################
#TODO: Test with real bricklet  Rotary Encoder
from tinkerforge.bricklet_rotary_encoder import RotaryEncoder
ROTARY_ENCODER = "Rotary Encoder"
ROTARY_ENCODER_COUNT = "Count"
class RotaryEncoderBricklet(AbstractBricklet):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = RotaryEncoder(self.uid, DataLogger.ipcon)
        self._data = data
        

    def start_timer(self):
        AbstractBricklet.start_timer(self) 

############################################################################################
#TODO: Test with real bricklet  Rotary Poti
from tinkerforge.bricklet_rotary_poti import RotaryPoti
ROTARY_POTI = "Rotary Poti"
ROTARY_POTI_POSITION = "Position"
ROTARY_POTI_ANALOG_VALUE = "Analog Value"
class RotaryPotiBricklet(AbstractBricklet):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = RotaryPoti(self.uid, DataLogger.ipcon)
        self._data = data
        

    def start_timer(self):
        AbstractBricklet.start_timer(self) 

############################################################################################
#TODO: Test with real bricklet  Segment Display 4x7
from tinkerforge.bricklet_segment_display_4x7 import BrickletSegmentDisplay4x7 
SEGMENT_DISPLAY_4x7 = "Segment Display 4x7"
SEGMENT_DISPLAY_4x7_SEGMENTS = "Segments"
SEGMENT_DISPLAY_4x7_COUNTER_VALUE = "Counter Value"
class SegmentDisplay4x7Bricklet(AbstractBricklet):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = BrickletSegmentDisplay4x7(self.uid, DataLogger.ipcon)
        self._data = data
        

    def start_timer(self):
        AbstractBricklet.start_timer(self) 

############################################################################################
#TODO: Test with real bricklet  Solid State Relay
from tinkerforge.bricklet_solid_state_relay import BrickletSolidStateRelay
SOLID_STATE_RELAY = "Solid State Relay"
SOLID_STATE_RELAY_STATE = "State"
SOLID_STATE_RELAY_MONOFLOP = "Monoflop"
class SolidStateRelayBricklet(AbstractBricklet):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = BrickletSolidStateRelay(self.uid, DataLogger.ipcon)
        self._data = data
        

    def start_timer(self):
        AbstractBricklet.start_timer(self) 

############################################################################################
#TODO: Test with real bricklet  Sound Intensity
from tinkerforge.bricklet_sound_intensity import BrickletSoundIntensity
SOUND_INTENSITY = "Sound Intensity"
SOUND_INTENSITY_INTENSITY = "Intensity"
class SoundIntensityBricklet(AbstractBricklet):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = BrickletSoundIntensity(self.uid, DataLogger.ipcon)
        self._data = data
        

    def start_timer(self):
        AbstractBricklet.start_timer(self) 

############################################################################################
#TODO: Test with real bricklet  Temperature
from tinkerforge.bricklet_temperature import BrickletTemperature
TEMPERATURE = "Temperature"
TEMPERATURE_TEMPERATURE = "Temperature"
class TemperatureBricklet(AbstractBricklet):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = BrickletTemperature(self.uid, DataLogger.ipcon)
        self._data = data
        

    def start_timer(self):
        AbstractBricklet.start_timer(self) 

############################################################################################
#TODO: Temperature IR
from tinkerforge.bricklet_temperature_ir import BrickletTemperatureIR
TEMPERATURE_IR = "Temperature IR"
TEMPERATURE_IR_AMBIENT_TEMPERATURE = "Ambient Temperature"
TEMPERATURE_IR_OBJECT_TEMPERATURE ="Object Temperature"
class TemperatureIRBricklet(AbstractBricklet):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = BrickletTemperatureIR(self.uid, DataLogger.ipcon)
        self._data = data
        

    def start_timer(self):
        AbstractBricklet.start_timer(self) 

############################################################################################
#TODO: Test with real bricklet  Tilt
from tinkerforge.bricklet_tilt import BrickletTilt
TILT = "Tilt"
TILT_STATE = "State"
class TiltBricklet(AbstractBricklet):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = BrickletTilt(self.uid, DataLogger.ipcon)
        self._data = data
        

    def start_timer(self):
        AbstractBricklet.start_timer(self) 

############################################################################################
#TODO: Test with real bricklet  Voltage
from tinkerforge.bricklet_voltage import BrickletVoltage
VOLTAGE = "Voltage"
VOLTAGE_VOLTAGE = "Voltage"
VOLTAGE_ANALOG_VALUE = "Analog Value"
class VoltageBricklet(AbstractBricklet):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = BrickletVoltage(self.uid, DataLogger.ipcon)
        self._data = data
        

    def start_timer(self):
        AbstractBricklet.start_timer(self) 

############################################################################################
#TODO: Test with real bricklet  Voltage/Current
from tinkerforge.bricklet_voltage_current import BrickletVoltageCurrent
VOLTAGE_CURRENT = "Voltage Current"
VOLTAGE_CURRENT_CURRENT = "Current"
VOLTAGE_CURRENT_VOLTAGE = "Voltage"
VOLTAGE_CURRENT_POWER = "Power"
class VoltageCurrentBricklet(AbstractBricklet):
    
    def __init__(self, uid, data):
        self.uid = uid        
        self._device = BrickletVoltageCurrent(self.uid, DataLogger.ipcon)
        self._data = data
        

    def start_timer(self):
        AbstractBricklet.start_timer(self) 
