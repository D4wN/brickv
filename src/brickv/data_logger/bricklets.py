from brickv.data_logger.utils import LoggerTimer   #Timer for getVariable
from brickv.data_logger.utils import CSVData       #bricklets
from brickv.data_logger.utils import Utilities
from brickv.data_logger.data_logger import DataLogger #gloabl thread/job queue -> brickelts callbacks/timer

import logging, sys

def string_to_class(string):
    return reduce(getattr, string.split("."), sys.modules[__name__])

###Bricklets and Variables#############################################################
SIMPLE_DEVICE = "SimpleDevice"
SPECIAL_DEVICE = "SpecialDevice"
COMPLEX_DEVICE = "ComplexDevice"
DEVICE_NAME = "name"
DEVICE_CLASS = "class"
DEVICE_UID = "uid"
DEVICE_VALUES = "values"
DEVICE_VALUES_NAME = "name"
DEVICE_VALUES_ARGS = "args"
DEVICE_VALUES_INTERVAL = "interval"

COMPLEX_DEVICE_VARIABLES = "variables"
COMPLEX_DEVICE_VARIABLES_NAME = "var_name"
COMPLEX_DEVICE_VARIABLES_BOOL = "var_bool"
class AbstractDevice(object):
    """DEBUG and Inheritance only class"""
    def __init__(self, data, datalogger):
        print str(data)               
        self.datalogger = datalogger
        self.data = data
        self.uid = self.data[DEVICE_UID] 
        self.identifier = None 
        self.device = None
        
        

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
        return "[BRICKLET=" + str(self.data[DEVICE_CLASS]) + " | <UID="+ str(self.uid) +"> | <IDENTIEFIER=" + str(self.identifier) + "> | <data="+ str(self.data) + ">]"

class SimpleDevice(AbstractDevice):
    
    def __init__(self, data, datalogger):  
        AbstractDevice.__init__(self, data, datalogger)     
        self.device = self.data[DEVICE_CLASS](self.uid, self.datalogger.ipcon)
        self.identifier = self.data[DEVICE_CLASS].DEVICE_IDENTIFIER  


    def start_timer(self):  
        AbstractDevice.start_timer(self)
                      
        for value in self.data[DEVICE_VALUES]:
            interval = self.data[DEVICE_VALUES][value][DEVICE_VALUES_INTERVAL]
            func_name = "_timer"
            var_name = value
            self.datalogger.timers.append(LoggerTimer(interval, func_name, var_name, self)) 

    def _timer(self, var_name):        
        #CSVDATA=[uid->memeber, name/identety->member, var_name->parameter, raw_data->function]
        value = None
        try:
            getter_name = self.data[DEVICE_VALUES][var_name][DEVICE_VALUES_NAME]
            getter_args = self.data[DEVICE_VALUES][var_name][DEVICE_VALUES_ARGS]
        
            if getter_args:
                value = getattr(self.device, getter_name)(*getter_args)
            else:
                value = getattr(self.device, getter_name)()
        except Exception as e:
            try:
                value = self._exception_msg(e.value, e.description)
            except Exception as ex:
                value = self._exception_msg(str(self.identifier)+"-"+str(var_name), ex)
        
        logging.debug(var_name+": "+str(value))                 


############################################################################################
#DEVICE#####################################################################################
############################################################################################
#Ambient Light
from tinkerforge.bricklet_ambient_light import AmbientLight
AMBIENT_LIGHT = "Ambient Light"
AMBIENT_LIGHT_ILLUMINANCE = "Illuminance"
AMBIENT_LIGHT_ANALOG_VALUE = "Analog Value"

############################################################################################
#Analog In          
#TODO: Test with real bricklet                      
from tinkerforge.bricklet_analog_in import AnalogIn
ANALOG_IN = "Analog In"
ANALOG_IN_VOLTAGE = "Voltage"
ANALOG_IN_ANALOG_VALUE = "Analog Value"

############################################################################################
#Analog Out
#TODO: Test with real bricklet  
from tinkerforge.bricklet_analog_out import AnalogOut
ANALOG_OUT = "Analog Out"
ANALOG_OUT_VOLTAGE = "Voltage"

############################################################################################
#Barometer
from tinkerforge.bricklet_barometer import Barometer
BAROMETER = "Barometer"
BAROMETER_AIR_PRESSURE = "Air Pressure"
BAROMETER_ALTITUDE = "Altitude"
BAROMETER_CHIP_TEMPERATURE = "Chip Temperature"

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
    
############################################################################################
#TODO: Test with real bricklet  Current12
from tinkerforge.bricklet_current12 import Current12
CURRENT_12 = "Current 12"
CURRENT_12_CURRENT = "Current"
CURRENT_12_ANALOG_VALUE = "Analog Value"

############################################################################################
#TODO: Test with real bricklet  Current25
from tinkerforge.bricklet_current25 import Current25
CURRENT_25 = "Current 25"
CURRENT_25_CURRENT = "Current"
CURRENT_25_ANALOG_VALUE = "Analog Value"

############################################################################################
#TODO: Test with real bricklet  Distance IR
from tinkerforge.bricklet_distance_ir import DistanceIR
DISTANCE_IR = "Distance IR"
DISTANCE_IR_DISTANCE = "Distance"
DISTANCE_IR_ANALOG_VALUE = "Analog Value"

############################################################################################
#TODO: Test with real bricklet  Distance US
from tinkerforge.bricklet_distance_us import DistanceUS
DISTANCE_US = "Distance US"
DISTANCE_US_DISTANCE = "Distance"
        
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

############################################################################################
#TODO: Test with real bricklet  Dual Relay
from tinkerforge.bricklet_dual_relay import DualRelay
DUAL_RELAY = "Dual Relay"
DUAL_RELAY_STATE = "State"
DUAL_RELAY_1 = "relay1"
DUAL_RELAY_2 = "relay2"

############################################################################################
#TODO: Test with real bricklet  Hall Effect
from tinkerforge.bricklet_hall_effect import HallEffect
HALL_EFFECT = "Hall Effect"
HALL_EFFECT_VALUE = "Value"

############################################################################################
#Humidity
from tinkerforge.bricklet_humidity import Humidity
HUMIDITY = "Humidity"
HUMIDITY_HUMIDITY = "Humidity"
HUMIDITY_ANALOG_VALUE = "Analog Value"

############################################################################################
#TODO: Test with real bricklet  Industrial Digital In 4
#TODO: Industrial Digital In 4  - variables? Dont know how to log this bricklet!
from tinkerforge.bricklet_industrial_digital_in_4 import IndustrialDigitalIn4
INDUSTRIAL_DIGITAL_IN_4 = "Industrial Digital In 4"

############################################################################################
#TODO: Test with real bricklet  Industrial Digital Out 4
#TODO: Industrial Digital Out 4 - variables? Dont know how to log this bricklet!
from tinkerforge.bricklet_industrial_digital_out_4 import IndustrialDigitalOut4
INDUSTRIAL_DIGITAL_OUT_4 = "Industrial Digital Out 4"

############################################################################################
#TODO: Test with real bricklet  Industrial Dual 0-20mA
from tinkerforge.bricklet_industrial_dual_0_20ma import IndustrialDual020mA
INDUSTRIAL_DUAL_0_20_MA = "Industrial Dual 0 20 mA"
INDUSTRIAL_DUAL_0_20_MA_CURRENT = "Current"
INDUSTRIAL_DUAL_0_20_MA_SENSOR_0 = "Sensor 0"
INDUSTRIAL_DUAL_0_20_MA_SENSOR_1 = "Sensor 1"

############################################################################################
#TODO: Test with real bricklet  Industrial Quad Relay
#TODO: Industrial Industrial Quad Relay - variables? Dont know how to log this bricklet!
from tinkerforge.bricklet_industrial_quad_relay import IndustrialQuadRelay
INDUSTRIAL_QUAD_RELAY = "Industrial Quad Relay"

############################################################################################
#TODO: Test with real bricklet  IO-16
from tinkerforge.bricklet_io16 import IO16
IO_16 = "IO-16"
IO_16_PORTS = "Ports"
IO_16_PORT_A = "Port A"
IO_16_PORT_B = "Port B"

############################################################################################
#TODO: Test with real bricklet  IO-4
from tinkerforge.bricklet_io4 import IO4
IO_4 = "IO-4"
IO_4_VALUE = "Value"


############################################################################################
#TODO: Test with real bricklet  Joystick
from tinkerforge.bricklet_joystick import Joystick
JOYSTICK = "Joystick"
JOYSTICK_POSITION = "Position"
JOYSTICK_POSITION_X = "Position X"
JOYSTICK_POSITION_Y = "Position Y"
JOYSTICK_ANALOG_VALUE = "Analog Value"
JOYSTICK_PRESSED = "Pressed"

############################################################################################
#TODO: Test with real bricklet  LCD 16x2
#TODO: LCD 16x2 - variables? Dont know how to log this bricklet!
from tinkerforge.bricklet_lcd_16x2 import LCD16x2
LCD_16x2 = "LCD 16x2"

############################################################################################
#TODO: Test with real bricklet  LCD 20x4
#TODO: LCD 20x4 - variables? Dont know how to log this bricklet!
from tinkerforge.bricklet_lcd_20x4 import LCD20x4
LCD_20x4 = "LCD 20x4"

############################################################################################
#TODO: Test with real bricklet  LED Strip
from tinkerforge.bricklet_led_strip import LEDStrip
LED_STRIP = "LED Strip"
LED_STRIP_SUPPLY_VOLTAGE = "Supply Voltage"
        
############################################################################################
#TODO: Test with real bricklet  Line
from tinkerforge.bricklet_line import BrickletLine
LINE = "line"
LINE_REFLECTIVITY = "Reflectivity"
        
############################################################################################
#TODO: Test with real bricklet  Linear Poti
from tinkerforge.bricklet_linear_poti import BrickletLinearPoti
LINEAR_POTI = "Linear Poti"
LINEAR_POTI_POSITION = "Position"
LINEAR_POTI_ANALOG_VALUE = "Analog Value"

############################################################################################
#TODO: Test with real bricklet  Moisture
from tinkerforge.bricklet_moisture import Moisture
MOISTURE = "Moisture"
MOISTURE_MOISTURE_VALUE = "Moisture Value"

############################################################################################
#TODO: Test with real bricklet  Motion Detector
from tinkerforge.bricklet_motion_detector import MotionDetector
MOTION_DETECTOR = "Motion Detector"
MOTION_DETECTOR_MOTION_DETECTED = "Motion Detected"

############################################################################################
#TODO: Test with real bricklet  Multi Touch
from tinkerforge.bricklet_multi_touch import MultiTouch
MULTI_TOUCH = "Multi Touch"
MULTI_TOUCH_TOUCH_STATE = "Touch State"

############################################################################################
#TODO: Test with real bricklet  NFC/RFID
#TODO: LCD NFC/RFID - variables? Dont know how to log this bricklet!
from tinkerforge.bricklet_nfc_rfid import BrickletNFCRFID
NFC_RFID = "NFC RFID"

############################################################################################
#TODO: Test with real bricklet  Piezo Buzzer
#TODO: Piezo Buzzer - variables? Dont know how to log this bricklet!
from tinkerforge.bricklet_piezo_buzzer import BrickletPiezoBuzzer
PIEZO_BUZZER = "Pirezo Buzzer"

############################################################################################
#TODO: Test with real bricklet  Piezo Speaker
#TODO: Piezo Speaker - variables? Dont know how to log this bricklet!
from tinkerforge.bricklet_piezo_speaker import PiezoSpeaker
PIEZO_SPEAKER = "Piezo Speaker"

############################################################################################
#TODO: Test with real bricklet  PTC
from tinkerforge.bricklet_ptc import PTC
PTC_BRICKLET = "PTC"
PTC_BRICKLET_TEMPERATURE = "Temperature"
PTC_BRICKLET_RESISTANCE = "Resistance"

############################################################################################
#TODO: Test with real bricklet  Remote Switch
#TODO: Remote Switch - variables? Dont know how to log this bricklet!
from tinkerforge.bricklet_remote_switch import RemoteSwitch
REMOTE_SWITCH = "Remote Switch"

############################################################################################
#TODO: Test with real bricklet  Rotary Encoder
from tinkerforge.bricklet_rotary_encoder import RotaryEncoder
ROTARY_ENCODER = "Rotary Encoder"
ROTARY_ENCODER_COUNT = "Count"
ROTARY_ENCODER_PRESSED = "Pressed"

############################################################################################
#TODO: Test with real bricklet  Rotary Poti
from tinkerforge.bricklet_rotary_poti import RotaryPoti
ROTARY_POTI = "Rotary Poti"
ROTARY_POTI_POSITION = "Position"
ROTARY_POTI_ANALOG_VALUE = "Analog Value"

############################################################################################
#TODO: Test with real bricklet  Solid State Relay
from tinkerforge.bricklet_solid_state_relay import BrickletSolidStateRelay
SOLID_STATE_RELAY = "Solid State Relay"
SOLID_STATE_RELAY_STATE = "State"

############################################################################################
#TODO: Test with real bricklet  Sound Intensity
from tinkerforge.bricklet_sound_intensity import BrickletSoundIntensity
SOUND_INTENSITY = "Sound Intensity"
SOUND_INTENSITY_INTENSITY = "Intensity"

############################################################################################
#TODO: Test with real bricklet  Temperature
from tinkerforge.bricklet_temperature import BrickletTemperature
TEMPERATURE = "Temperature"
TEMPERATURE_TEMPERATURE = "Temperature"

############################################################################################
#TODO: Temperature IR
from tinkerforge.bricklet_temperature_ir import BrickletTemperatureIR
TEMPERATURE_IR = "Temperature IR"
TEMPERATURE_IR_AMBIENT_TEMPERATURE = "Ambient Temperature"
TEMPERATURE_IR_OBJECT_TEMPERATURE ="Object Temperature"

############################################################################################
#TODO: Test with real bricklet  Tilt
from tinkerforge.bricklet_tilt import BrickletTilt
TILT = "Tilt"
TILT_STATE = "State"

############################################################################################
#TODO: Test with real bricklet  Voltage
from tinkerforge.bricklet_voltage import BrickletVoltage
VOLTAGE = "Voltage"
VOLTAGE_VOLTAGE = "Voltage"
VOLTAGE_ANALOG_VALUE = "Analog Value"

############################################################################################
#TODO: Test with real bricklet  Voltage/Current
from tinkerforge.bricklet_voltage_current import BrickletVoltageCurrent
VOLTAGE_CURRENT = "Voltage Current"
VOLTAGE_CURRENT_CURRENT = "Current"
VOLTAGE_CURRENT_VOLTAGE = "Voltage"
VOLTAGE_CURRENT_POWER = "Power"

############################################################################################
#SPECIAL_DEVICES############################################################################
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