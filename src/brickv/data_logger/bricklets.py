from brickv.data_logger.data_logger import DataLogger    #gloabl thread/job queue -> brickelts callbacks/timer
from brickv.data_logger.utils import LoggerTimer   #Timer for getVariable
from brickv.data_logger.utils import CSVData       #bricklets
from brickv.data_logger.utils import Utilities

import logging
###Bricklets and Variables###

#ALL BRICKLETS + FUNCTIONS##################################################################
class AbstractDevice(object):
    """DEBUG and Inheritance only class"""
    def __init__(self, uid, data, datalogger):
        self.uid = uid        
        self.device = None
        self.data = data
        self.identifier = None 
        self.datalogger = datalogger

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
        return "[BRICKLET=" + str(type(self)) + " | <UID="+ str(self.uid) +"> | <IDENTIEFIER=" + str(self.identifier) + "> | <data="+ str(self.data) + ">]"
    
############################################################################################
#Ambient Light
from tinkerforge.bricklet_ambient_light import AmbientLight
AMBIENT_LIGHT = "Ambient Light"
AMBIENT_LIGHT_ILLUMINANCE = "Illuminance"
AMBIENT_LIGHT_ANALOG_VALUE = "Analog Value"
class AmbientLightBricklet(AbstractDevice):
    
    def __init__(self, uid, data, datalogger):
        AbstractDevice.__init__(self, uid, data, datalogger)
        
        self.device = AmbientLight(self.uid, datalogger.ipcon)
        self.identifier = AmbientLight.DEVICE_IDENTIFIER


    def start_timer(self):
        AbstractDevice.start_timer(self)
                
        value1 = Utilities.parse_to_int(self.data[AMBIENT_LIGHT_ANALOG_VALUE])
        value2 = Utilities.parse_to_int(self.data[AMBIENT_LIGHT_ILLUMINANCE])     
        
        self.datalogger.timers.append(LoggerTimer(value1, self._timer_analog_value))      
        self.datalogger.timers.append(LoggerTimer(value2, self._timer_illuminance))

    def _timer_analog_value(self):        
        value = self._try_catch(self.device.get_analog_value)
        csv = CSVData(self.uid, self.identifier, AMBIENT_LIGHT_ANALOG_VALUE, value)
        self.datalogger.add_to_queue(csv)
        
    def _timer_illuminance(self):
        value = self._try_catch(self.device.get_illuminance)
        csv = CSVData(self.uid, self.identifier, AMBIENT_LIGHT_ILLUMINANCE, value)
        self.datalogger.add_to_queue(csv)

############################################################################################
#Analog In          
#TODO: Test with real bricklet                      
from tinkerforge.bricklet_analog_in import AnalogIn
ANALOG_IN = "Analog In"
ANALOG_IN_VOLTAGE = "Voltage"
ANALOG_IN_ANALOG_VALUE = "Analog Value"
class AnalogInBricklet(AbstractDevice):
    
    def __init__(self, uid, data, datalogger):
        AbstractDevice.__init__(self, uid, data, datalogger)
      
        self.device = AnalogIn(self.uid, datalogger.ipcon)
        self.identifier = AnalogIn.DEVICE_IDENTIFIER  


    def start_timer(self):  
        AbstractDevice.start_timer(self)
              
        value1 = Utilities.parse_to_int(self.data[ANALOG_IN_ANALOG_VALUE])
        value2 = Utilities.parse_to_int(self.data[ANALOG_IN_VOLTAGE])
              
        self.datalogger.timers.append(LoggerTimer(value1, self._timer_analog_value))  
        self.datalogger.timers.append(LoggerTimer(value2, self._timer_voltage))

    def _timer_analog_value(self):
        value = self._try_catch(self.device.get_analog_value)
        csv = CSVData(self.uid, self.identifier, ANALOG_IN_ANALOG_VALUE, value)
        self.datalogger.add_to_queue(csv)
        
    def _timer_voltage(self):
        value = self._try_catch(self.device.get_voltage)
        csv = CSVData(self.uid, self.identifier, ANALOG_IN_VOLTAGE, value)
        self.datalogger.add_to_queue(csv)  

############################################################################################
#Analog Out
#TODO: Test with real bricklet  
from tinkerforge.bricklet_analog_out import AnalogOut
ANALOG_OUT = "Analog Out"
ANALOG_OUT_VOLTAGE = "Voltage"
class AnalogOutBricklet(AbstractDevice):
    
    def __init__(self, uid, data, datalogger):
        AbstractDevice.__init__(self, uid, data, datalogger)
            
        self.device = AnalogOut(self.uid, datalogger.ipcon)
        self.identifier = AnalogOut.DEVICE_IDENTIFIER  


    def start_timer(self):   
        AbstractDevice.start_timer(self)
             
        value1 = Utilities.parse_to_int(self.data[ANALOG_OUT_VOLTAGE]) 
        
        self.datalogger.timers.append(LoggerTimer(value1, self._timer_voltage))         

    def _timer_voltage(self):
        value = self._try_catch(self.device.get_voltage)
        csv = CSVData(self.uid, self.identifier, ANALOG_OUT_VOLTAGE, value)
        self.datalogger.add_to_queue(csv)

############################################################################################
#Barometer
from tinkerforge.bricklet_barometer import Barometer
BAROMETER = "Barometer"
BAROMETER_AIR_PRESSURE = "Air Pressure"
BAROMETER_ALTITUDE = "Altitude"
BAROMETER_CHIP_TEMPERATURE = "Chip Temperature"
class BarometerBricklet(AbstractDevice):
    #chip_temperature()
    def __init__(self, uid, data, datalogger):
        AbstractDevice.__init__(self, uid, data, datalogger)
             
        self.device = Barometer(self.uid, datalogger.ipcon)
        self.identifier = Barometer.DEVICE_IDENTIFIER  


    def start_timer(self):        
        AbstractDevice.start_timer(self)
        
        value1 = Utilities.parse_to_int(self.data[BAROMETER_AIR_PRESSURE])
        value2 = Utilities.parse_to_int(self.data[BAROMETER_ALTITUDE])      
        value3 = Utilities.parse_to_int(self.data[BAROMETER_CHIP_TEMPERATURE])  
        
        self.datalogger.timers.append(LoggerTimer(value1, self._timer_air_pressure))
        self.datalogger.timers.append(LoggerTimer(value2, self._timer_altitude))
        self.datalogger.timers.append(LoggerTimer(value3, self._timer_chip_temperature))

    def _timer_air_pressure(self):
        value = self._try_catch(self.device.get_air_pressure)
        csv = CSVData(self.uid, self.identifier, BAROMETER_AIR_PRESSURE, value)
        self.datalogger.add_to_queue(csv)
        
    def _timer_altitude(self):
        value = self._try_catch(self.device.get_altitude)
        csv = CSVData(self.uid, self.identifier, BAROMETER_ALTITUDE, value)
        self.datalogger.add_to_queue(csv)  
         
    def _timer_chip_temperature(self):
        value = self._try_catch(self.device.get_chip_temperature)
        csv = CSVData(self.uid, self.identifier, BAROMETER_CHIP_TEMPERATURE, value)
        self.datalogger.add_to_queue(csv)         

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
class ColorBricklet(AbstractDevice):
    
    def __init__(self, uid, data, datalogger):
        AbstractDevice.__init__(self, uid, data, datalogger)
             
        self.device = Color(self.uid, datalogger.ipcon)
        self.identifier = Color.DEVICE_IDENTIFIER  


    def start_timer(self):     
        AbstractDevice.start_timer(self)
        
        value1 = Utilities.parse_to_int(self.data[COLOR_COLOR])
        value2 = Utilities.parse_to_int(self.data[COLOR_ILLUMINANCE])
        value3 = Utilities.parse_to_int(self.data[COLOR_TEMPERATURE])   
        
        self.datalogger.timers.append(LoggerTimer(value1, self._timer_color))         
        self.datalogger.timers.append(LoggerTimer(value2, self._timer_illuminance))
        self.datalogger.timers.append(LoggerTimer(value3, self._timer_color_temperature))

    def _timer_color(self):
        try:
            r, g, b, c = self.__TEMP_get_color()#self.device.get_color()
            if Utilities.parse_to_bool(self.data[COLOR_RED]):
                self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, COLOR_RED, r))
            if Utilities.parse_to_bool(self.data[COLOR_GREEN]):
                self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, COLOR_GREEN, g))
            if Utilities.parse_to_bool(self.data[COLOR_BLUE]):
                self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, COLOR_BLUE, b))
            if Utilities.parse_to_bool(self.data[COLOR_CLEAR]): 
                self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, COLOR_CLEAR, c))
        except Exception as e:
            self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, COLOR_COLOR, self._exception_msg(e.value, e.description)))
        
    def _timer_illuminance(self):
        value = self._try_catch(self.device.get_illuminance)
        csv = CSVData(self.uid, self.identifier, COLOR_ILLUMINANCE, value)
        self.datalogger.add_to_queue(csv)  
        
    def _timer_color_temperature(self):
        value = self._try_catch(self.device.get_color_temperature)
        csv = CSVData(self.uid, self.identifier, COLOR_ILLUMINANCE, value)
        self.datalogger.add_to_queue(csv) 
        
    def __TEMP_get_color(self):
        return (10, 20, 30, 40)
    
############################################################################################
#TODO: Test with real bricklet  Current12
from tinkerforge.bricklet_current12 import Current12
CURRENT_12 = "Current 12"
CURRENT_12_CURRENT = "Current"
CURRENT_12_ANALOG_VALUE = "Analog Value"
class Current12Bricklet(AbstractDevice):
    
    def __init__(self, uid, data, datalogger):
        AbstractDevice.__init__(self, uid, data, datalogger)
              
        self.device = Current12(self.uid, datalogger.ipcon)
        self.identifier = Current12.DEVICE_IDENTIFIER  


    def start_timer(self):
        AbstractDevice.start_timer(self)  
        
        value1 = Utilities.parse_to_int(self.data[CURRENT_12_ANALOG_VALUE])
        value2 = Utilities.parse_to_int(self.data[CURRENT_12_CURRENT])  
        
        self.datalogger.timers.append(LoggerTimer(value1, self._timer_analog_value))         
        self.datalogger.timers.append(LoggerTimer(value2, self._timer_current))  
    
    def _timer_analog_value(self):
        value = self._try_catch(self.device.get_analog_value)
        csv = CSVData(self.uid, self.identifier, CURRENT_12_ANALOG_VALUE, value)
        self.datalogger.add_to_queue(csv) 
    
    def _timer_current(self):
        value = self._try_catch(self.device.get_current)
        csv = CSVData(self.uid, self.identifier, CURRENT_12_CURRENT, value)
        self.datalogger.add_to_queue(csv)         

############################################################################################
#TODO: Test with real bricklet  Current25
from tinkerforge.bricklet_current25 import Current25
CURRENT_25 = "Current 25"
CURRENT_25_CURRENT = "Current"
CURRENT_25_ANALOG_VALUE = "Analog Value"
class Current25Bricklet(AbstractDevice):
    
    def __init__(self, uid, data, datalogger):
        AbstractDevice.__init__(self, uid, data, datalogger)
      
        self.device = Current25(self.uid, datalogger.ipcon)
        self.identifier = Current25.DEVICE_IDENTIFIER 


    def start_timer(self):
        AbstractDevice.start_timer(self)   
        
        value1 = Utilities.parse_to_int(self.data[CURRENT_25_ANALOG_VALUE])
        value2 = Utilities.parse_to_int(self.data[CURRENT_25_CURRENT])  
        
        self.datalogger.timers.append(LoggerTimer(value1, self._timer_analog_value))         
        self.datalogger.timers.append(LoggerTimer(value2, self._timer_current))  
    
    def _timer_analog_value(self):
        value = self._try_catch(self.device.get_analog_value)
        csv = CSVData(self.uid, self.identifier, CURRENT_25_ANALOG_VALUE, value)
        self.datalogger.add_to_queue(csv) 
        
    def _timer_current(self):
        value = self._try_catch(self.device.get_current)
        csv = CSVData(self.uid, self.identifier, CURRENT_25_CURRENT, value)
        self.datalogger.add_to_queue(csv) 

############################################################################################
#TODO: Test with real bricklet  Distance IR
from tinkerforge.bricklet_distance_ir import DistanceIR
DISTANCE_IR = "Distance IR"
DISTANCE_IR_DISTANCE = "Distance"
DISTANCE_IR_ANALOG_VALUE = "Analog Value"
class DistanceIRBricklet(AbstractDevice):
    
    def __init__(self, uid, data, datalogger):
        AbstractDevice.__init__(self, uid, data, datalogger)
      
        self.device = DistanceIR(self.uid, datalogger.ipcon)
        self.identifier = DistanceIR.DEVICE_IDENTIFIER 


    def start_timer(self):
        AbstractDevice.start_timer(self)   
        
        value1 = Utilities.parse_to_int(self.data[DISTANCE_IR_ANALOG_VALUE])
        value2 = Utilities.parse_to_int(self.data[DISTANCE_IR_DISTANCE])  
        
        self.datalogger.timers.append(LoggerTimer(value1, self._timer_analog_value))         
        self.datalogger.timers.append(LoggerTimer(value2, self._timer_distance))  
    
    def _timer_analog_value(self):
        value = self._try_catch(self.device.get_analog_value)
        csv = CSVData(self.uid, self.identifier, DISTANCE_IR_ANALOG_VALUE, value)
        self.datalogger.add_to_queue(csv) 
        
    def _timer_distance(self):
        value = self._try_catch(self.device.get_analog_value)
        csv = CSVData(self.uid, self.identifier, DISTANCE_IR_DISTANCE, value)
        self.datalogger.add_to_queue(csv)

############################################################################################
#TODO: Test with real bricklet  Distance US
from tinkerforge.bricklet_distance_us import DistanceUS
DISTANCE_US = "Distance US"
DISTANCE_US_DISTANCE = "Distance"
class DistanceUSBricklet(AbstractDevice):
    
    def __init__(self, uid, data, datalogger):
        AbstractDevice.__init__(self, uid, data, datalogger)
             
        self.device = DistanceUS(self.uid, datalogger.ipcon)
        self.identifier = DistanceUS.DEVICE_IDENTIFIER 


    def start_timer(self):
        AbstractDevice.start_timer(self)   
        
        value1 = Utilities.parse_to_int(self.data[DISTANCE_US_DISTANCE])
        
        self.datalogger.timers.append(LoggerTimer(value1, self._timer_distance))   
    
    def _timer_distance(self):
        value = self._try_catch(self.device.get_distance_value)
        csv = CSVData(self.uid, self.identifier, DISTANCE_US_DISTANCE, value)
        self.datalogger.add_to_queue(csv) 
        
############################################################################################
#TODO: Test with real bricklet  Dual Button
from tinkerforge.bricklet_dual_button import DualButton
DUAL_BUTTON = "Dual Button"
DUAL_BUTTON_BUTTONS = "Buttons"
DUAL_BUTTON_BUTTON_L = "button_l"
DUAL_BUTTON_BUTTON_R = "button_r"
DUAL_BUTTON_LEDS = "Leds"
DUAL_BUTTON_LED_L = "led_l"
DUAL_BUTTON_LED_R = "led_r"
class DualButtonBricklet(AbstractDevice):
    
    def __init__(self, uid, data, datalogger):
        AbstractDevice.__init__(self, uid, data, datalogger)
      
        self.device = DualButton(self.uid, datalogger.ipcon)
        self.identifier = DualButton.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        
        value1 = Utilities.parse_to_int(self.data[DUAL_BUTTON_BUTTONS])
        value2 = Utilities.parse_to_int(self.data[DUAL_BUTTON_LEDS])
        
        self.datalogger.timers.append(LoggerTimer(value1, self._timer_buttons))   
        self.datalogger.timers.append(LoggerTimer(value2, self._timer_leds))  
    
    def _timer_buttons(self):
        try:
            button_l, button_r = self.device.get_button_state()
            if Utilities.parse_to_bool(self.data[DUAL_BUTTON_BUTTON_L]):
                self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, DUAL_BUTTON_BUTTON_L, button_l))
            if Utilities.parse_to_bool(self.data[DUAL_BUTTON_BUTTON_R]):
                self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, DUAL_BUTTON_BUTTON_R, button_r))
        except Exception as e:
            self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, DUAL_BUTTON_BUTTONS, self._exception_msg(e.value, e.description)))

    def _timer_leds(self):
        try:
            led_l, led_r = self.device.get_led_state()
            if Utilities.parse_to_bool(self.data[DUAL_BUTTON_LED_L]):
                self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, DUAL_BUTTON_LED_L, led_l))
            if Utilities.parse_to_bool(self.data[DUAL_BUTTON_LED_R]):
                self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, DUAL_BUTTON_LED_R, led_r))
        except Exception as e:
            self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, DUAL_BUTTON_LEDS, self._exception_msg(e.value, e.description)))

############################################################################################
#TODO: Test with real bricklet  Dual Relay
from tinkerforge.bricklet_dual_relay import DualRelay
DUAL_RELAY = "Dual Relay"
DUAL_RELAY_STATE = "State"
DUAL_RELAY_1 = "relay1"
DUAL_RELAY_2 = "relay2"
class DualRelayBricklet(AbstractDevice):
    
    def __init__(self, uid, data, datalogger):
        AbstractDevice.__init__(self, uid, data, datalogger)
     
        self.device = DualRelay(self.uid, datalogger.ipcon)
        self.identifier = DualRelay.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        
        value1 = Utilities.parse_to_int(self.data[DUAL_RELAY_STATE])
        
        self.datalogger.timers.append(LoggerTimer(value1, self._timer_state))  
    
    def _timer_state(self):
        try:
            r1, r2 = self.device.get_state()
            if Utilities.parse_to_bool(self.data[DUAL_RELAY_1]):
                self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, DUAL_RELAY_1, r1))
            if Utilities.parse_to_bool(self.data[DUAL_RELAY_2]):
                self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, DUAL_RELAY_2, r2))
        except Exception as e:
            self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, DUAL_RELAY_STATE, self._exception_msg(e.value, e.description)))

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
class GPSBricklet(AbstractDevice):
    
    def __init__(self, uid, data, datalogger):
        AbstractDevice.__init__(self, uid, data, datalogger)
      
        self.device = GPS(self.uid, datalogger.ipcon)
        self.identifier = GPS.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        
        value1 = Utilities.parse_to_int(self.data[GPS_COORDINATES])
        value2 = Utilities.parse_to_int(self.data[GPS_ALTITUDE])
        value3 = Utilities.parse_to_int(self.data[GPS_MOTION])
        value4 = Utilities.parse_to_int(self.data[GPS_DATE_TIME])
        
        self.datalogger.timers.append(LoggerTimer(value1, self._timer_coordinates))  
        self.datalogger.timers.append(LoggerTimer(value2, self._timer_altitude)) 
        self.datalogger.timers.append(LoggerTimer(value3, self._timer_motion)) 
        self.datalogger.timers.append(LoggerTimer(value4, self._timer_date_time)) 
    
    def _timer_coordinates(self):
        try:
            #check for the FIX Value of get_status()
            fix = self._get_fix_status()
                          
            if fix == GPS.FIX_NO_FIX:
                self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, GPS_COORDINATES, self._exception_msg("Fix-Status="+fix, "GPS Fix-Status was 1, but needs to be 2 or 3 for valid Coordinates.")))
                return

            latitude, ns, longitude, ew, pdop, hdop, vdop, epe = self.device.get_coordinates()     
            #latitude, ns, longitude, ew, pdop, hdop, vdop, epe = self.__TMP_get_coordinates()  #TODO: TMP ONLY       
            if Utilities.parse_to_bool(self.data[GPS_LATITUDE]):
                self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, GPS_LATITUDE, latitude))
            if Utilities.parse_to_bool(self.data[GPS_NS]):
                self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, GPS_NS, ns))
            if Utilities.parse_to_bool(self.data[GPS_LONGITUDE]):
                self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, GPS_LONGITUDE, longitude))
            if Utilities.parse_to_bool(self.data[GPS_EW]):
                self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, GPS_EW, ew))
            if Utilities.parse_to_bool(self.data[GPS_PDOP]):
                self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, GPS_PDOP, pdop))
            if Utilities.parse_to_bool(self.data[GPS_HDOP]):
                self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, GPS_HDOP, hdop))
            if Utilities.parse_to_bool(self.data[GPS_VDOP]):
                self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, GPS_VDOP, vdop))
            if Utilities.parse_to_bool(self.data[GPS_EPE]):
                self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, GPS_EPE, epe))
        except Exception as e:
            self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, GPS_COORDINATES, self._exception_msg(e.value, e.description)))

    def _timer_altitude(self):
        try:
            #check for the FIX Value of get_status()
            fix = self._get_fix_status()
              
            if fix != GPS.FIX_3D_FIX:
                self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, GPS_ALTITUDE, self._exception_msg("Fix-Status="+fix, "GPS Fix-Status was " + fix + ", but needs to be 3 for valid Altitude Values.")))
                return

            altitude, geoidal_separation = self.device.get_altitude()            
            if Utilities.parse_to_bool(self.data[GPS_ALTITUDE_VALUE]):
                self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, GPS_ALTITUDE_VALUE, altitude))
            if Utilities.parse_to_bool(self.data[GPS_GEOIDAL_SEPERATION]):
                self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, GPS_GEOIDAL_SEPERATION, geoidal_separation))
        except Exception as e:
            self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, GPS_ALTITUDE, self._exception_msg(e.value, e.description)))

    def _timer_motion(self):
        try:
            #check for the FIX Value of get_status()
            fix = self._get_fix_status()
              
            if fix == GPS.FIX_NO_FIX:
                self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, GPS_MOTION, self._exception_msg("Fix-Status="+fix, "GPS Fix-Status was " + fix + ", but needs to be 2 or 3 for valid Altitude Values.")))
                return

            course, speed = self.device.get_motion()
            if Utilities.parse_to_bool(self.data[GPS_COURSE]):
                self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, GPS_COURSE, course))
            if Utilities.parse_to_bool(self.data[GPS_SPEED]):
                self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, GPS_SPEED, speed))
        except Exception as e:
            self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, GPS_MOTION, self._exception_msg(e.value, e.description)))

    def _timer_date_time(self):
        try:
            date, time = self.device.get_date_time()
            if Utilities.parse_to_bool(self.data[GPS_DATE]):
                self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, GPS_DATE, date))
            if Utilities.parse_to_bool(self.data[GPS_TIME]):
                self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, GPS_TIME, time))
        except Exception as e:
            self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, GPS_DATE_TIME, self._exception_msg(e.value, e.description)))

    def _get_fix_status(self):
        fix, satellites_view, satellites_used = self.device.get_status()
        #fix, satellites_view, satellites_used = self.__TMP_get_status()#TODO: TMP ONLY
        
        if Utilities.parse_to_bool(self.data[GPS_FIX_STATUS]):
            self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, GPS_FIX_STATUS, fix))
        if Utilities.parse_to_bool(self.data[GPS_SATELLITES_VIEW]):
            self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, GPS_SATELLITES_VIEW, satellites_view))
        if Utilities.parse_to_bool(self.data[GPS_SATELLITES_USED]):
            self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, GPS_SATELLITES_USED, satellites_used))
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
class HallEffectBricklet(AbstractDevice):
    
    def __init__(self, uid, data, datalogger):
        AbstractDevice.__init__(self, uid, data, datalogger)
       
        self.device = HallEffect(self.uid, datalogger.ipcon)
        self.identifier = HallEffect.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        
        value1 = Utilities.parse_to_int(self.data[HALL_EFFECT_VALUE])
        
        self.datalogger.timers.append(LoggerTimer(value1, self._timer_value))   
    
    def _timer_value(self):
        value = self._try_catch(self.device.get_value)
        csv = CSVData(self.uid, self.identifier, HALL_EFFECT_VALUE, value)
        self.datalogger.add_to_queue(csv)         

############################################################################################
#Humidity
from tinkerforge.bricklet_humidity import Humidity
HUMIDITY = "Humidity"
HUMIDITY_HUMIDITY = "Humidity"
HUMIDITY_ANALOG_VALUE = "Analog Value"
class HumidityBricklet(AbstractDevice):
    
    def __init__(self, uid, data, datalogger):
        AbstractDevice.__init__(self, uid, data, datalogger)
              
        self.device = Humidity(self.uid, datalogger.ipcon)
        self.identifier = Humidity.DEVICE_IDENTIFIER

        
    def start_timer(self):
        AbstractDevice.start_timer(self) 
                
        value1 = Utilities.parse_to_int(self.data[HUMIDITY_ANALOG_VALUE])
        value2 = Utilities.parse_to_int(self.data[HUMIDITY_HUMIDITY])       
        
        self.datalogger.timers.append(LoggerTimer(value1, self._timer_analog_value))         
        self.datalogger.timers.append(LoggerTimer(value2, self._timer_humidity))

    def _timer_analog_value(self):
        value = self._try_catch(self.device.get_analog_value)
        csv = CSVData(self.uid, self.identifier, HUMIDITY_ANALOG_VALUE, value)
        self.datalogger.add_to_queue(csv)
        
    def _timer_humidity(self):
        value = self._try_catch(self.device.get_humidity)
        csv = CSVData(self.uid, self.identifier, HUMIDITY_HUMIDITY, value)
        self.datalogger.add_to_queue(csv)   

############################################################################################
#TODO: Test with real bricklet  Industrial Digital In 4
#TODO: Industrial Digital In 4  - variables? Dont know how to log this bricklet!
from tinkerforge.bricklet_industrial_digital_in_4 import IndustrialDigitalIn4
INDUSTRIAL_DIGITAL_IN_4 = "Industrial Digital In 4"
class IndustrialDigitalIn4Bricklet(AbstractDevice):
    
    def __init__(self, uid, data, datalogger):
        AbstractDevice.__init__(self, uid, data, datalogger)
    
        self.device = IndustrialDigitalIn4(self.uid, datalogger.ipcon)
        self.identifier = IndustrialDigitalIn4.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        logging.warning("The IndustrialDigitalIn4Bricklet is not supported for Logging actions!")

############################################################################################
#TODO: Test with real bricklet  Industrial Digital Out 4
#TODO: Industrial Digital Out 4 - variables? Dont know how to log this bricklet!
from tinkerforge.bricklet_industrial_digital_out_4 import IndustrialDigitalOut4
INDUSTRIAL_DIGITAL_OUT_4 = "Industrial Digital Out 4"
class IndustrialDigitalOut4Bricklet(AbstractDevice):
    
    def __init__(self, uid, data, datalogger):
        AbstractDevice.__init__(self, uid, data, datalogger)
     
        self.device = IndustrialDigitalOut4(self.uid, datalogger.ipcon)
        self.identifier = IndustrialDigitalOut4.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        logging.warning("The IndustrialDigitalOut4Bricklet is not supported for Logging actions!")

############################################################################################
#TODO: Test with real bricklet  Industrial Dual 0-20mA
from tinkerforge.bricklet_industrial_dual_0_20ma import IndustrialDual020mA
INDUSTRIAL_DUAL_0_20_MA = "Industrial Dual 0 20 mA"
INDUSTRIAL_DUAL_0_20_MA_CURRENT = "Current"
INDUSTRIAL_DUAL_0_20_MA_SENSOR_0 = "Sensor 0"
INDUSTRIAL_DUAL_0_20_MA_SENSOR_1 = "Sensor 1"
class IndustrialDual020mABricklet(AbstractDevice):
    
    def __init__(self, uid, data, datalogger):
        AbstractDevice.__init__(self, uid, data, datalogger)
   
        self.device = IndustrialDual020mA(self.uid, datalogger.ipcon)
        self.identifier = IndustrialDual020mA.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        
        value1 = Utilities.parse_to_int(self.data[INDUSTRIAL_DUAL_0_20_MA_CURRENT])      
        
        self.datalogger.timers.append(LoggerTimer(value1, self._timer_current))  

    def _timer_current(self):
        try:
            sensor_0 = self.device.get_current(0)
            sensor_1 = self.device.get_current(1)
            
            if Utilities.parse_to_bool(self.data[INDUSTRIAL_DUAL_0_20_MA_SENSOR_0]):
                self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, INDUSTRIAL_DUAL_0_20_MA_SENSOR_0, sensor_0))            
            if Utilities.parse_to_bool(self.data[INDUSTRIAL_DUAL_0_20_MA_SENSOR_1]):
                self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, INDUSTRIAL_DUAL_0_20_MA_SENSOR_1, sensor_1))

        except Exception as e:
            csv = CSVData(self.uid, INDUSTRIAL_DUAL_0_20_MA, self.identifier, self._exception_msg(e.value, e.description))
            self.datalogger.add_to_queue(csv)

############################################################################################
#TODO: Test with real bricklet  Industrial Quad Relay
#TODO: Industrial Industrial Quad Relay - variables? Dont know how to log this bricklet!
from tinkerforge.bricklet_industrial_quad_relay import IndustrialQuadRelay
INDUSTRIAL_QUAD_RELAY = "Industrial Quad Relay"
class IndustrialQuadRelayBricklet(AbstractDevice):
    
    def __init__(self, uid, data, datalogger):
        AbstractDevice.__init__(self, uid, data, datalogger)
      
        self.device = IndustrialQuadRelay(self.uid, datalogger.ipcon)
        self.identifier = IndustrialQuadRelay.DEVICE_IDENTIFIER 
        

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
class IO16Bricklet(AbstractDevice):
    
    def __init__(self, uid, data, datalogger):
        AbstractDevice.__init__(self, uid, data, datalogger)
      
        self.device = IO16(self.uid, datalogger.ipcon)
        self.identifier = IO16.DEVICE_IDENTIFIER 

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        
        value1 = Utilities.parse_to_int(self.data[IO_16_PORTS])      
        
        self.datalogger.timers.append(LoggerTimer(value1, self._timer_ports))  

    def _timer_ports(self):
        try:
            port_a = self.device.get_port('a')
            port_b = self.device.get_port('b')
            
            if Utilities.parse_to_bool(self.data[IO_16_PORT_A]):
                self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, IO_16_PORT_A, port_a))           
            if Utilities.parse_to_bool(self.data[IO_16_PORT_B]):
                self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, IO_16_PORT_B, port_b))

        except Exception as e:
            csv = CSVData(self.uid, self.identifier, IO_16_PORTS, self._exception_msg(e.value, e.description))
            self.datalogger.add_to_queue(csv)

############################################################################################
#TODO: Test with real bricklet  IO-4
from tinkerforge.bricklet_io4 import IO4
IO_4 = "IO-4"
IO_4_VALUE = "Value"
class IO4Bricklet(AbstractDevice):
    
    def __init__(self, uid, data, datalogger):
        AbstractDevice.__init__(self, uid, data, datalogger)
       
        self.device = IO4(self.uid, datalogger.ipcon)
        self.identifier = IO4.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        
        value1 = Utilities.parse_to_int(self.data[IO_4_VALUE])     
        
        self.datalogger.timers.append(LoggerTimer(value1, self._timer_value)) 

    def _timer_value(self):
        value = self._try_catch(self.device.get_value)
        csv = CSVData(self.uid, self.identifier, IO_4_VALUE, value)
        self.datalogger.add_to_queue(csv)

############################################################################################
#TODO: Test with real bricklet  Joystick
from tinkerforge.bricklet_joystick import Joystick
JOYSTICK = "Joystick"
JOYSTICK_POSITION = "Position"
JOYSTICK_POSITION_X = "Position X"
JOYSTICK_POSITION_Y = "Position Y"
JOYSTICK_ANALOG_VALUE = "Analog Value"
JOYSTICK_PRESSED = "Pressed"
class JoystickBricklet(AbstractDevice):
    
    def __init__(self, uid, data, datalogger):
        AbstractDevice.__init__(self, uid, data, datalogger)
      
        self.device = Joystick(self.uid, datalogger.ipcon)
        self.identifier = Joystick.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        
        value1 = Utilities.parse_to_int(self.data[JOYSTICK_POSITION])     
        value2 = Utilities.parse_to_int(self.data[JOYSTICK_ANALOG_VALUE])    
        value3 = Utilities.parse_to_int(self.data[JOYSTICK_PRESSED])    
        
        self.datalogger.timers.append(LoggerTimer(value1, self._timer_position)) 
        self.datalogger.timers.append(LoggerTimer(value2, self._timer_analog_value)) 
        self.datalogger.timers.append(LoggerTimer(value3, self._timer_is_pressed)) 

    def _timer_position(self):
        try:
            x, y = self.device.get_position()

            if Utilities.parse_to_bool(self.data[JOYSTICK_POSITION_X]):
                self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, JOYSTICK_POSITION_X, x))       
            if Utilities.parse_to_bool(self.data[JOYSTICK_POSITION_Y]):
                self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, JOYSTICK_POSITION_Y, y))

        except Exception as e:
            csv = CSVData(self.uid, self.identifier, JOYSTICK_POSITION, self._exception_msg(e.value, e.description))
            self.datalogger.add_to_queue(csv)
        
    def _timer_analog_value(self):
        value = self._try_catch(self.device.get_analog_value)
        csv = CSVData(self.uid, self.identifier, JOYSTICK_ANALOG_VALUE, value)
        self.datalogger.add_to_queue(csv)
    
    def _timer_is_pressed(self):
        value = self._try_catch(self.device.is_pressed)
        csv = CSVData(self.uid, self.identifier, JOYSTICK_PRESSED, value)
        self.datalogger.add_to_queue(csv)

############################################################################################
#TODO: Test with real bricklet  LCD 16x2
#TODO: LCD 16x2 - variables? Dont know how to log this bricklet!
from tinkerforge.bricklet_lcd_16x2 import LCD16x2
LCD_16x2 = "LCD 16x2"
class LCD16x2Bricklet(AbstractDevice):
    
    def __init__(self, uid, data, datalogger):
        AbstractDevice.__init__(self, uid, data, datalogger)
       
        self.device = LCD16x2(self.uid, datalogger.ipcon)
        self.identifier = LCD16x2.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self)         
        logging.warning("The LCD16x2Bricklet is not supported for Logging actions!")

############################################################################################
#TODO: Test with real bricklet  LCD 20x4
#TODO: LCD 20x4 - variables? Dont know how to log this bricklet!
from tinkerforge.bricklet_lcd_20x4 import LCD20x4
LCD_20x4 = "LCD 20x4"
class LCD20x4Bricklet(AbstractDevice):
    
    def __init__(self, uid, data, datalogger):
        AbstractDevice.__init__(self, uid, data, datalogger)
      
        self.device = LCD20x4(self.uid, datalogger.ipcon)
        self.identifier = LCD20x4.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self)
        logging.warning("The LCD20x4Bricklet is not supported for Logging actions!")

############################################################################################
#TODO: Test with real bricklet  LED Strip
from tinkerforge.bricklet_led_strip import LEDStrip
LED_STRIP = "LED Strip"
LED_STRIP_SUPPLY_VOLTAGE = "Supply Voltage"
class LEDStripBricklet(AbstractDevice):
    
    def __init__(self, uid, data, datalogger):
        AbstractDevice.__init__(self, uid, data, datalogger)
     
        self.device = LEDStrip(self.uid, datalogger.ipcon)
        self.identifier = LEDStrip.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        
        value1 = Utilities.parse_to_int(self.data[LED_STRIP_SUPPLY_VOLTAGE])   
        
        self.datalogger.timers.append(LoggerTimer(value1, self._timer_supply_voltage)) 

    def _timer_supply_voltage(self):
        value = self._try_catch(self.device.get_supply_voltage)
        self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, LED_STRIP_SUPPLY_VOLTAGE, value))
        
############################################################################################
#TODO: Test with real bricklet  Line
from tinkerforge.bricklet_line import BrickletLine
LINE = "line"
LINE_REFLECTIVITY = "Reflectivity"
class LineBricklet(AbstractDevice):
    
    def __init__(self, uid, data, datalogger):
        AbstractDevice.__init__(self, uid, data, datalogger)
    
        self.device = BrickletLine(self.uid, datalogger.ipcon)
        self.identifier = BrickletLine.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self)
        
        value1 = Utilities.parse_to_int(self.data[LINE_REFLECTIVITY])   
        
        self.datalogger.timers.append(LoggerTimer(value1, self._timer_refelctivity)) 

    def _timer_refelctivity(self):
        value = self._try_catch(self.device.get_reflectivity)
        self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, LINE_REFLECTIVITY, value))
        
############################################################################################
#TODO: Test with real bricklet  Linear Poti
from tinkerforge.bricklet_linear_poti import BrickletLinearPoti
LINEAR_POTI = "Linear Poti"
LINEAR_POTI_POSITION = "Position"
LINEAR_POTI_ANALOG_VALUE = "Analog Value"
class LinearPotiBricklet(AbstractDevice):
    
    def __init__(self, uid, data, datalogger):
        AbstractDevice.__init__(self, uid, data, datalogger)
              
        self.device = BrickletLinearPoti(self.uid, datalogger.ipcon)
        self.identifier = BrickletLinearPoti.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        
        value1 = Utilities.parse_to_int(self.data[LINEAR_POTI_POSITION])   
        value2 = Utilities.parse_to_int(self.data[LINEAR_POTI_ANALOG_VALUE]) 
        
        self.datalogger.timers.append(LoggerTimer(value1, self._timer_position)) 
        self.datalogger.timers.append(LoggerTimer(value2, self._timer_analog_value)) 

    def _timer_position(self):
        value = self._try_catch(self.device.get_position)
        self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, LINEAR_POTI_POSITION, value))

    def _timer_analog_value(self):
        value = self._try_catch(self.device.get_analog_value)
        self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, LINEAR_POTI_ANALOG_VALUE, value))

############################################################################################
#TODO: Test with real bricklet  Moisture
from tinkerforge.bricklet_moisture import Moisture
MOISTURE = "Moisture"
MOISTURE_MOISTURE_VALUE = "Moisture Value"
class MoistureBricklet(AbstractDevice):
    
    def __init__(self, uid, data, datalogger):
        AbstractDevice.__init__(self, uid, data, datalogger)
       
        self.device = Moisture(self.uid, datalogger.ipcon)
        self.identifier = Moisture.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        
        value1 = Utilities.parse_to_int(self.data[MOISTURE_MOISTURE_VALUE])  
        
        self.datalogger.timers.append(LoggerTimer(value1, self._timer_moisture_value)) 

    def _timer_moisture_value(self):
        value = self._try_catch(self.device.get_moisture_value)
        self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, MOISTURE_MOISTURE_VALUE, value))

############################################################################################
#TODO: Test with real bricklet  Motion Detector
from tinkerforge.bricklet_motion_detector import MotionDetector
MOTION_DETECTOR = "Motion Detector"
MOTION_DETECTOR_MOTION_DETECTED = "Motion Detected"
class MotionDetectorBricklet(AbstractDevice):
    
    def __init__(self, uid, data, datalogger):
        AbstractDevice.__init__(self, uid, data, datalogger)
    
        self.device = MotionDetector(self.uid, datalogger.ipcon)
        self.identifier = MotionDetector.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self)
        
        value1 = Utilities.parse_to_int(self.data[MOTION_DETECTOR_MOTION_DETECTED])  
        
        self.datalogger.timers.append(LoggerTimer(value1, self._timer_motion_detected)) 

    def _timer_motion_detected(self):
        value = self._try_catch(self.device.get_motion_detected)
        self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, MOTION_DETECTOR_MOTION_DETECTED, value))

############################################################################################
#TODO: Test with real bricklet  Multi Touch
from tinkerforge.bricklet_multi_touch import MultiTouch
MULTI_TOUCH = "Multi Touch"
MULTI_TOUCH_TOUCH_STATE = "Touch State"
class MultiTouchBricklet(AbstractDevice):
    
    def __init__(self, uid, data, datalogger):
        AbstractDevice.__init__(self, uid, data, datalogger)
       
        self.device = MultiTouch(self.uid, datalogger.ipcon)
        self.identifier = MultiTouch.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        
        value1 = Utilities.parse_to_int(self.data[MULTI_TOUCH_TOUCH_STATE])  
        
        self.datalogger.timers.append(LoggerTimer(value1, self._timer_touch_state)) 

    def _timer_touch_state(self):
        value = self._try_catch(self.device.get_touch_state)
        self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, MULTI_TOUCH_TOUCH_STATE, value))

############################################################################################
#TODO: Test with real bricklet  NFC/RFID
#TODO: LCD NFC/RFID - variables? Dont know how to log this bricklet!
from tinkerforge.bricklet_nfc_rfid import BrickletNFCRFID
NFC_RFID = "NFC RFID"
#NFC_RFID_STATE = "State"
class NFCRFIDBricklet(AbstractDevice):
    
    def __init__(self, uid, data, datalogger):
        AbstractDevice.__init__(self, uid, data, datalogger)
     
        self.device = BrickletNFCRFID(self.uid, datalogger.ipcon)
        self.identifier = BrickletNFCRFID.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        logging.warning("The NFCRFIDBricklet is not supported for Logging actions!")

############################################################################################
#TODO: Test with real bricklet  Piezo Buzzer
#TODO: Piezo Buzzer - variables? Dont know how to log this bricklet!
from tinkerforge.bricklet_piezo_buzzer import BrickletPiezoBuzzer
PIEZO_BUZZER = "Pirezo Buzzer"
class PiezoBuzzerBricklet(AbstractDevice):
    
    def __init__(self, uid, data, datalogger):
        AbstractDevice.__init__(self, uid, data, datalogger)
       
        self.device = BrickletPiezoBuzzer(self.uid, datalogger.ipcon)
        self.identifier = BrickletPiezoBuzzer.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        logging.warning("The PiezoBuzzerBricklet is not supported for Logging actions!")

############################################################################################
#TODO: Test with real bricklet  Piezo Speaker
#TODO: Piezo Speaker - variables? Dont know how to log this bricklet!
from tinkerforge.bricklet_piezo_speaker import PiezoSpeaker
PIEZO_SPEAKER = "Piezo Speaker"
class PiezoSpeakerBricklet(AbstractDevice):
    
    def __init__(self, uid, data, datalogger):
        AbstractDevice.__init__(self, uid, data, datalogger)
     
        self.device = PiezoSpeaker(self.uid, datalogger.ipcon)
        self.identifier = PiezoSpeaker.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        logging.warning("The PiezoSpeakerBricklet is not supported for Logging actions!")        

############################################################################################
#TODO: Test with real bricklet  PTC
from tinkerforge.bricklet_ptc import PTC
PTC_BRICKLET = "PTC"
PTC_BRICKLET_TEMPERATURE = "Temperature"
PTC_BRICKLET_RESISTANCE = "Resistance"
class PTCBricklet(AbstractDevice):
    
    def __init__(self, uid, data, datalogger):
        AbstractDevice.__init__(self, uid, data, datalogger)
     
        self.device = PTC(self.uid, datalogger.ipcon)
        self.identifier = PTC.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
         
        value1 = Utilities.parse_to_int(self.data[PTC_BRICKLET_TEMPERATURE])  
        value2 = Utilities.parse_to_int(self.data[PTC_BRICKLET_RESISTANCE])  
        
        self.datalogger.timers.append(LoggerTimer(value1, self._timer_temeperature)) 
        self.datalogger.timers.append(LoggerTimer(value2, self._timer_resistance)) 

    def _timer_temeperature(self):
        value = self._try_catch(self.device.get_temperature)
        self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, PTC_BRICKLET_TEMPERATURE, value))
        
    def _timer_resistance(self):
        value = self._try_catch(self.device.get_resistance)
        self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, PTC_BRICKLET_RESISTANCE, value))

############################################################################################
#TODO: Test with real bricklet  Remote Switch
#TODO: Remote Switch - variables? Dont know how to log this bricklet!
from tinkerforge.bricklet_remote_switch import RemoteSwitch
REMOTE_SWITCH = "Remote Switch"
class RemoteSwitchBricklet(AbstractDevice):
    
    def __init__(self, uid, data, datalogger):
        AbstractDevice.__init__(self, uid, data, datalogger)
      
        self.device = RemoteSwitch(self.uid, datalogger.ipcon)
        self.identifier = RemoteSwitch.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        logging.warning("The RemoteSwitchBricklet is not supported for Logging actions!")  

############################################################################################
#TODO: Test with real bricklet  Rotary Encoder
from tinkerforge.bricklet_rotary_encoder import RotaryEncoder
ROTARY_ENCODER = "Rotary Encoder"
ROTARY_ENCODER_COUNT = "Count"
ROTARY_ENCODER_PRESSED = "Pressed"
class RotaryEncoderBricklet(AbstractDevice):
    
    def __init__(self, uid, data, datalogger):
        AbstractDevice.__init__(self, uid, data, datalogger)
      
        self.device = RotaryEncoder(self.uid, datalogger.ipcon)
        self.identifier = RotaryEncoder.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) #get_count(false)
        
        value1 = Utilities.parse_to_int(self.data[ROTARY_ENCODER_COUNT])  
        value2 = Utilities.parse_to_int(self.data[ROTARY_ENCODER_PRESSED])  
        
        self.datalogger.timers.append(LoggerTimer(value1, self._timer_count)) 
        self.datalogger.timers.append(LoggerTimer(value2, self._timer_pressed)) 

    def _timer_count(self):
        try:
            value = self.device.get_count(False)
            self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, ROTARY_ENCODER_COUNT, value))
        except Exception as e:
            self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, ROTARY_ENCODER_COUNT, self._exception_msg(e.value, e.description)))

    def _timer_pressed(self):
        value = self._try_catch(self.device.is_pressed)
        self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, ROTARY_ENCODER_PRESSED, value))

############################################################################################
#TODO: Test with real bricklet  Rotary Poti
from tinkerforge.bricklet_rotary_poti import RotaryPoti
ROTARY_POTI = "Rotary Poti"
ROTARY_POTI_POSITION = "Position"
ROTARY_POTI_ANALOG_VALUE = "Analog Value"
class RotaryPotiBricklet(AbstractDevice):
    
    def __init__(self, uid, data, datalogger):
        AbstractDevice.__init__(self, uid, data, datalogger)
    
        self.device = RotaryPoti(self.uid, datalogger.ipcon)
        self.identifier = RotaryPoti.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        
        value1 = Utilities.parse_to_int(self.data[ROTARY_POTI_POSITION])  
        value2 = Utilities.parse_to_int(self.data[ROTARY_POTI_ANALOG_VALUE])  
        
        self.datalogger.timers.append(LoggerTimer(value1, self._timer_position)) 
        self.datalogger.timers.append(LoggerTimer(value2, self._timer_analog_value)) 
        
    def _timer_position(self):
        value = self._try_catch(self.device.get_position)
        self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, ROTARY_POTI_POSITION, value))
    
    def _timer_analog_value(self):
        value = self._try_catch(self.device.get_analog_value)
        self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, ROTARY_POTI_ANALOG_VALUE, value))

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
class SegmentDisplay4x7Bricklet(AbstractDevice):
    
    def __init__(self, uid, data, datalogger):
        AbstractDevice.__init__(self, uid, data, datalogger)
    
        self.device = BrickletSegmentDisplay4x7(self.uid, datalogger.ipcon)
        self.identifier = BrickletSegmentDisplay4x7.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        
        value1 = Utilities.parse_to_int(self.data[SEGMENT_DISPLAY_4x7_SEGMENTS])  
        value2 = Utilities.parse_to_int(self.data[SEGMENT_DISPLAY_4x7_COUNTER_VALUE])  
        
        self.datalogger.timers.append(LoggerTimer(value1, self._timer_segments)) 
        self.datalogger.timers.append(LoggerTimer(value2, self._timer_counter_value)) 

    def _timer_segments(self):
        try:
            segment, brightness, colon = self.device.get_segments()
            #segment, brightness, colon = self.__TEMP_GET_SEGMENTS()#TODO: debug only
            if Utilities.parse_to_bool(self.data[SEGMENT_DISPLAY_4x7_SEGMENT_1]):
                self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, SEGMENT_DISPLAY_4x7_SEGMENT_1, segment[0]))
            if Utilities.parse_to_bool(self.data[SEGMENT_DISPLAY_4x7_SEGMENT_2]):
                self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, SEGMENT_DISPLAY_4x7_SEGMENT_2, segment[1]))
            if Utilities.parse_to_bool(self.data[SEGMENT_DISPLAY_4x7_SEGMENT_3]):
                self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, SEGMENT_DISPLAY_4x7_SEGMENT_3, segment[2]))
            if Utilities.parse_to_bool(self.data[SEGMENT_DISPLAY_4x7_SEGMENT_4]):
                self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, SEGMENT_DISPLAY_4x7_SEGMENT_4, segment[3]))
            if Utilities.parse_to_bool(self.data[SEGMENT_DISPLAY_4x7_BRIGTHNESS]):
                self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, SEGMENT_DISPLAY_4x7_BRIGTHNESS, brightness))
            if Utilities.parse_to_bool(self.data[SEGMENT_DISPLAY_4x7_COLON]):
                self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, SEGMENT_DISPLAY_4x7_COLON, colon))        
        except Exception as e:
            self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, SEGMENT_DISPLAY_4x7_SEGMENTS, self._exception_msg(e.value, e.description)))

    def _timer_counter_value(self):
        value = self._try_catch(self.device.get_counter_value)
        self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, SEGMENT_DISPLAY_4x7_COUNTER_VALUE, value))

    def __TEMP_GET_SEGMENTS(self):
        #([int, int, int, int], int, bool)
        #segments, brightness und colon.
        return ([1,2,3,4], 50, False)

############################################################################################
#TODO: Test with real bricklet  Solid State Relay
from tinkerforge.bricklet_solid_state_relay import BrickletSolidStateRelay
SOLID_STATE_RELAY = "Solid State Relay"
SOLID_STATE_RELAY_STATE = "State"
class SolidStateRelayBricklet(AbstractDevice):
    
    def __init__(self, uid, data, datalogger):
        AbstractDevice.__init__(self, uid, data, datalogger)
       
        self.device = BrickletSolidStateRelay(self.uid, datalogger.ipcon)
        self.identifier = BrickletSolidStateRelay.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 

        value1 = Utilities.parse_to_int(self.data[SOLID_STATE_RELAY_STATE])  
        
        self.datalogger.timers.append(LoggerTimer(value1, self._timer_state)) 
        
    def _timer_state(self):
        value = self._try_catch(self.device.get_state)
        self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, SOLID_STATE_RELAY_STATE, value))

############################################################################################
#TODO: Test with real bricklet  Sound Intensity
from tinkerforge.bricklet_sound_intensity import BrickletSoundIntensity
SOUND_INTENSITY = "Sound Intensity"
SOUND_INTENSITY_INTENSITY = "Intensity"
class SoundIntensityBricklet(AbstractDevice):
    
    def __init__(self, uid, data, datalogger):
        AbstractDevice.__init__(self, uid, data, datalogger)
      
        self.device = BrickletSoundIntensity(self.uid, datalogger.ipcon)
        self.identifier = BrickletSoundIntensity.DEVICE_IDENTIFIER 
        

    def start_timer(self):#get_intensity
        AbstractDevice.start_timer(self) 
        
        value1 = Utilities.parse_to_int(self.data[SOUND_INTENSITY_INTENSITY])  
        
        self.datalogger.timers.append(LoggerTimer(value1, self._timer_intensity)) 
        
    def _timer_intensity(self):
        value = self._try_catch(self.device.get_intensity)
        self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, SOUND_INTENSITY_INTENSITY, value))

############################################################################################
#TODO: Test with real bricklet  Temperature
from tinkerforge.bricklet_temperature import BrickletTemperature
TEMPERATURE = "Temperature"
TEMPERATURE_TEMPERATURE = "Temperature"
class TemperatureBricklet(AbstractDevice):
    
    def __init__(self, uid, data, datalogger):
        AbstractDevice.__init__(self, uid, data, datalogger)
              
        self.device = BrickletTemperature(self.uid, datalogger.ipcon)
        self.identifier = BrickletTemperature.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        
        value1 = Utilities.parse_to_int(self.data[TEMPERATURE_TEMPERATURE])  
        
        self.datalogger.timers.append(LoggerTimer(value1, self._timer_temperature)) 
        
    def _timer_temperature(self):
        value = self._try_catch(self.device.get_temperature)
        self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, TEMPERATURE_TEMPERATURE, value))

############################################################################################
#TODO: Temperature IR
from tinkerforge.bricklet_temperature_ir import BrickletTemperatureIR
TEMPERATURE_IR = "Temperature IR"
TEMPERATURE_IR_AMBIENT_TEMPERATURE = "Ambient Temperature"
TEMPERATURE_IR_OBJECT_TEMPERATURE ="Object Temperature"
class TemperatureIRBricklet(AbstractDevice):
    
    def __init__(self, uid, data, datalogger):
        AbstractDevice.__init__(self, uid, data, datalogger)
      
        self.device = BrickletTemperatureIR(self.uid, datalogger.ipcon)
        self.identifier = BrickletTemperatureIR.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        
        value1 = Utilities.parse_to_int(self.data[TEMPERATURE_IR_AMBIENT_TEMPERATURE])  
        value2 = Utilities.parse_to_int(self.data[TEMPERATURE_IR_OBJECT_TEMPERATURE])  
        
        self.datalogger.timers.append(LoggerTimer(value1, self._timer_ambient_temperature)) 
        self.datalogger.timers.append(LoggerTimer(value2, self._timer_object_temperature))
        
    def _timer_ambient_temperature(self):
        value = self._try_catch(self.device.get_ambient_temperature)
        self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, TEMPERATURE_IR_AMBIENT_TEMPERATURE, value))
        
    def _timer_object_temperature(self):
        value = self._try_catch(self.device.get_object_temperature)
        self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, TEMPERATURE_IR_OBJECT_TEMPERATURE, value))

############################################################################################
#TODO: Test with real bricklet  Tilt
from tinkerforge.bricklet_tilt import BrickletTilt
TILT = "Tilt"
TILT_STATE = "State"
class TiltBricklet(AbstractDevice):
    
    def __init__(self, uid, data, datalogger):
        AbstractDevice.__init__(self, uid, data, datalogger)
  
        self.device = BrickletTilt(self.uid, datalogger.ipcon)
        self.identifier = BrickletTilt.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        
        value1 = Utilities.parse_to_int(self.data[TILT_STATE])  
        
        self.datalogger.timers.append(LoggerTimer(value1, self._timer_state))
        
    def _timer_state(self):
        value = self._try_catch(self.device.get_tilt_state)
        self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, TILT_STATE, value))

############################################################################################
#TODO: Test with real bricklet  Voltage
from tinkerforge.bricklet_voltage import BrickletVoltage
VOLTAGE = "Voltage"
VOLTAGE_VOLTAGE = "Voltage"
VOLTAGE_ANALOG_VALUE = "Analog Value"
class VoltageBricklet(AbstractDevice):
    
    def __init__(self, uid, data, datalogger):
        AbstractDevice.__init__(self, uid, data, datalogger)
 
        self.device = BrickletVoltage(self.uid, datalogger.ipcon)
        self.identifier = BrickletVoltage.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        
        value1 = Utilities.parse_to_int(self.data[VOLTAGE_VOLTAGE])  
        value2 = Utilities.parse_to_int(self.data[VOLTAGE_ANALOG_VALUE])  
        
        self.datalogger.timers.append(LoggerTimer(value1, self._timer_voltage)) 
        self.datalogger.timers.append(LoggerTimer(value2, self._timer_analog_value))
        
    def _timer_voltage(self):
        value = self._try_catch(self.device.get_voltage)
        self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, VOLTAGE_VOLTAGE, value))
        
    def _timer_analog_value(self):
        value = self._try_catch(self.device.get_analog_value)
        self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, VOLTAGE_ANALOG_VALUE, value))

############################################################################################
#TODO: Test with real bricklet  Voltage/Current
from tinkerforge.bricklet_voltage_current import BrickletVoltageCurrent
VOLTAGE_CURRENT = "Voltage Current"
VOLTAGE_CURRENT_CURRENT = "Current"
VOLTAGE_CURRENT_VOLTAGE = "Voltage"
VOLTAGE_CURRENT_POWER = "Power"
class VoltageCurrentBricklet(AbstractDevice):
    
    def __init__(self, uid, data, datalogger):
        AbstractDevice.__init__(self, uid, data, datalogger)
      
        self.device = BrickletVoltageCurrent(self.uid, datalogger.ipcon)
        self.identifier = BrickletVoltageCurrent.DEVICE_IDENTIFIER 
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        
        value1 = Utilities.parse_to_int(self.data[VOLTAGE_CURRENT_CURRENT])  
        value2 = Utilities.parse_to_int(self.data[VOLTAGE_CURRENT_VOLTAGE])  
        value3 = Utilities.parse_to_int(self.data[VOLTAGE_CURRENT_POWER])
        
        self.datalogger.timers.append(LoggerTimer(value1, self._timer_current)) 
        self.datalogger.timers.append(LoggerTimer(value2, self._timer_voltage))
        self.datalogger.timers.append(LoggerTimer(value3, self._timer_power))
        
    def _timer_current(self):
        value = self._try_catch(self.device.get_current)
        self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, VOLTAGE_CURRENT_CURRENT, value))
        
    def _timer_voltage(self):
        value = self._try_catch(self.device.get_voltage)
        self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, VOLTAGE_CURRENT_VOLTAGE, value))
        
    def _timer_power(self):
        value = self._try_catch(self.device.get_power)
        self.datalogger.add_to_queue(CSVData(self.uid, self.identifier, VOLTAGE_CURRENT_POWER, value))
