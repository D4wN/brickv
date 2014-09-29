import sys, tinkerforge, utils, data_logger

#import ALL supported bricklets and bricks
from tinkerforge.bricklet_ambient_light import AmbientLight
from tinkerforge.bricklet_analog_in import AnalogIn
from tinkerforge.bricklet_analog_out import AnalogOut
from tinkerforge.bricklet_barometer import Barometer
from tinkerforge.bricklet_color import Color
from tinkerforge.bricklet_current12 import Current12
from tinkerforge.bricklet_current25 import Current25
from tinkerforge.bricklet_distance_ir import DistanceIR
from tinkerforge.bricklet_distance_us import DistanceUS
from tinkerforge.bricklet_dual_button import DualButton
from tinkerforge.bricklet_dual_relay import DualRelay
from tinkerforge.bricklet_hall_effect import HallEffect
from tinkerforge.bricklet_humidity import Humidity
from tinkerforge.bricklet_industrial_dual_0_20ma import IndustrialDual020mA
from tinkerforge.bricklet_io16 import IO16
from tinkerforge.bricklet_io4 import IO4
from tinkerforge.bricklet_joystick import Joystick
from tinkerforge.bricklet_led_strip import LEDStrip
from tinkerforge.bricklet_line import BrickletLine
from tinkerforge.bricklet_linear_poti import BrickletLinearPoti
from tinkerforge.bricklet_moisture import Moisture
from tinkerforge.bricklet_motion_detector import MotionDetector
from tinkerforge.bricklet_multi_touch import MultiTouch
from tinkerforge.bricklet_ptc import PTC
from tinkerforge.bricklet_rotary_encoder import RotaryEncoder
from tinkerforge.bricklet_rotary_poti import RotaryPoti
from tinkerforge.bricklet_solid_state_relay import BrickletSolidStateRelay
from tinkerforge.bricklet_sound_intensity import BrickletSoundIntensity
from tinkerforge.bricklet_temperature import BrickletTemperature
from tinkerforge.bricklet_temperature_ir import BrickletTemperatureIR
from tinkerforge.bricklet_tilt import BrickletTilt
from tinkerforge.bricklet_voltage import BrickletVoltage
from tinkerforge.bricklet_voltage_current import BrickletVoltageCurrent
from tinkerforge.bricklet_gps import GPS
from tinkerforge.bricklet_segment_display_4x7 import BrickletSegmentDisplay4x7 

def string_to_class(string):
    return reduce(getattr, string.split("."), sys.modules[__name__])

class Identifier(object):
    """
        This class is for all identification strings of the bricklets and bricks.
    """
    ###Devices
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
    
    COMPLEX_DEVICE_VALUES_NAME = "var_name"
    COMPLEX_DEVICE_VALUES_BOOL = "var_bool"
    
    SPECIAL_DEVICE_VALUE = "special_values"
    SPECIAL_DEVICE_BOOL = "special_bool"

    ###Bricks
    #TODO: write bricks
    ###Bricklets
    AMBIENT_LIGHT = "Ambient Light"
    AMBIENT_LIGHT_ILLUMINANCE = "Illuminance"
    AMBIENT_LIGHT_ANALOG_VALUE = "Analog Value"
    
    ANALOG_IN = "Analog In"
    ANALOG_IN_VOLTAGE = "Voltage"
    ANALOG_IN_ANALOG_VALUE = "Analog Value"
    
    ANALOG_OUT = "Analog Out"
    ANALOG_OUT_VOLTAGE = "Voltage"
    
    BAROMETER = "Barometer"
    BAROMETER_AIR_PRESSURE = "Air Pressure"
    BAROMETER_ALTITUDE = "Altitude"
    BAROMETER_CHIP_TEMPERATURE = "Chip Temperature"
    
    COLOR = "Color"
    COLOR_RED = "Red"
    COLOR_GREEN = "Green"
    COLOR_BLUE = "Blue"
    COLOR_CLEAR = "Clear"
    COLOR_COLOR = "Rgbc"
    COLOR_ILLUMINANCE = "Illuminance"
    COLOR_TEMPERATURE = "Color Temperature"
    
    CURRENT_12 = "Current 12"
    CURRENT_12_CURRENT = "Current"
    CURRENT_12_ANALOG_VALUE = "Analog Value"
    
    CURRENT_25 = "Current 25"
    CURRENT_25_CURRENT = "Current"
    CURRENT_25_ANALOG_VALUE = "Analog Value"
    
    DISTANCE_IR = "Distance IR"
    DISTANCE_IR_DISTANCE = "Distance"
    DISTANCE_IR_ANALOG_VALUE = "Analog Value"
    
    DISTANCE_US = "Distance US"
    DISTANCE_US_DISTANCE = "Distance"
    
    DUAL_BUTTON = "Dual Button"
    DUAL_BUTTON_BUTTONS = "Buttons"
    DUAL_BUTTON_BUTTON_L = "button_l"
    DUAL_BUTTON_BUTTON_R = "button_r"
    DUAL_BUTTON_LEDS = "Leds"
    DUAL_BUTTON_LED_L = "led_l"
    DUAL_BUTTON_LED_R = "led_r"
    
    DUAL_RELAY = "Dual Relay"
    DUAL_RELAY_STATE = "State"
    DUAL_RELAY_1 = "relay1"
    DUAL_RELAY_2 = "relay2"
    
    HALL_EFFECT = "Hall Effect"
    HALL_EFFECT_VALUE = "Value"
    
    HUMIDITY = "Humidity"
    HUMIDITY_HUMIDITY = "Humidity"
    HUMIDITY_ANALOG_VALUE = "Analog Value"
    
    INDUSTRIAL_DUAL_0_20_MA = "Industrial Dual 0 20 mA"
    INDUSTRIAL_DUAL_0_20_MA_CURRENT = "Current"
    INDUSTRIAL_DUAL_0_20_MA_SENSOR_0 = "Sensor 0"
    INDUSTRIAL_DUAL_0_20_MA_SENSOR_1 = "Sensor 1"
    
    IO_16 = "IO-16"
    IO_16_PORTS = "Ports"
    IO_16_PORT_A = "Port A"
    IO_16_PORT_B = "Port B"
    
    IO_4 = "IO-4"
    IO_4_VALUE = "Value"
    
    JOYSTICK = "Joystick"
    JOYSTICK_POSITION = "Position"
    JOYSTICK_POSITION_X = "Position X"
    JOYSTICK_POSITION_Y = "Position Y"
    JOYSTICK_ANALOG_VALUE = "Analog Value"
    JOYSTICK_PRESSED = "Pressed"
    
    LED_STRIP = "LED Strip"
    LED_STRIP_SUPPLY_VOLTAGE = "Supply Voltage"
    
    LINE = "line"
    LINE_REFLECTIVITY = "Reflectivity"
    
    LINEAR_POTI = "Linear Poti"
    LINEAR_POTI_POSITION = "Position"
    LINEAR_POTI_ANALOG_VALUE = "Analog Value"
    
    MOISTURE = "Moisture"
    MOISTURE_MOISTURE_VALUE = "Moisture Value"
    
    MOTION_DETECTOR = "Motion Detector"
    MOTION_DETECTOR_MOTION_DETECTED = "Motion Detected"
    
    MULTI_TOUCH = "Multi Touch"
    MULTI_TOUCH_TOUCH_STATE = "Touch State"
    
    ROTARY_ENCODER = "Rotary Encoder"
    ROTARY_ENCODER_COUNT = "Count"
    ROTARY_ENCODER_PRESSED = "Pressed"
    
    ROTARY_POTI = "Rotary Poti"
    ROTARY_POTI_POSITION = "Position"
    ROTARY_POTI_ANALOG_VALUE = "Analog Value"
    
    SOLID_STATE_RELAY = "Solid State Relay"
    SOLID_STATE_RELAY_STATE = "State"
    
    SOUND_INTENSITY = "Sound Intensity"
    SOUND_INTENSITY_INTENSITY = "Intensity"
    
    TEMPERATURE = "Temperature"
    TEMPERATURE_TEMPERATURE = "Temperature"
    
    TEMPERATURE_IR = "Temperature IR"
    TEMPERATURE_IR_AMBIENT_TEMPERATURE = "Ambient Temperature"
    TEMPERATURE_IR_OBJECT_TEMPERATURE ="Object Temperature"
    
    TILT = "Tilt"
    TILT_STATE = "State"
    
    VOLTAGE = "Voltage"
    VOLTAGE_VOLTAGE = "Voltage"
    VOLTAGE_ANALOG_VALUE = "Analog Value"
    
    VOLTAGE_CURRENT = "Voltage Current"
    VOLTAGE_CURRENT_CURRENT = "Current"
    VOLTAGE_CURRENT_VOLTAGE = "Voltage"
    VOLTAGE_CURRENT_POWER = "Power"

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
    
    SEGMENT_DISPLAY_4x7 = "Segment Display 4x7"
    SEGMENT_DISPLAY_4x7_SEGMENTS = "Segments"
    SEGMENT_DISPLAY_4x7_SEGMENT_1 = "Segment 1"
    SEGMENT_DISPLAY_4x7_SEGMENT_2 = "Segment 2"
    SEGMENT_DISPLAY_4x7_SEGMENT_3 = "Segment 3"
    SEGMENT_DISPLAY_4x7_SEGMENT_4 = "Segment 4"
    SEGMENT_DISPLAY_4x7_BRIGTHNESS = "Brightness"
    SEGMENT_DISPLAY_4x7_COLON = "Colon"
    SEGMENT_DISPLAY_4x7_COUNTER_VALUE = "Counter Value"

class AbstractDevice(object):
    """DEBUG and Inheritance only class"""
    def __init__(self, data, datalogger):             
        self.datalogger = datalogger
        self.data = data
        self.uid = self.data[Identifier.DEVICE_UID] 
        self.identifier = None 
        self.device = None
        
        self.__name__ = "AbstractDevice"
        
        
    def start_timer(self):
        utils.EventLogger.debug(self.__str__())
                
        
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
        return "["+self.__name__+"=" + str(self.data[Identifier.DEVICE_CLASS]) + " | <UID="+ str(self.uid) +"> | <IDENTIEFIER=" + str(self.identifier) + "> | <data="+ str(self.data) + ">]"

class SimpleDevice(AbstractDevice):
    
    def __init__(self, data, datalogger):  
        AbstractDevice.__init__(self, data, datalogger)     
        self.device = self.data[Identifier.DEVICE_CLASS](self.uid, self.datalogger.ipcon)
        self.identifier = self.data[Identifier.DEVICE_CLASS].DEVICE_IDENTIFIER  

        self.__name__ = Identifier.SIMPLE_DEVICE

    def start_timer(self):  
        AbstractDevice.start_timer(self)
                      
        for value in self.data[Identifier.DEVICE_VALUES]:
            interval = self.data[Identifier.DEVICE_VALUES][value][Identifier.DEVICE_VALUES_INTERVAL]
            func_name = "_timer"
            var_name = value
            self.datalogger.timers.append(utils.LoggerTimer(interval, func_name, var_name, self)) 

    def _timer(self, var_name):        
        #CSVDATA=[uid->memeber, name/identety->member, var_name->parameter, raw_data->function]
        value = None
        try:
            getter_name = self.data[Identifier.DEVICE_VALUES][var_name][Identifier.DEVICE_VALUES_NAME]
            getter_args = self.data[Identifier.DEVICE_VALUES][var_name][Identifier.DEVICE_VALUES_ARGS]
        
            if getter_args:
                value = getattr(self.device, getter_name)(*getter_args)
            else:
                value = getattr(self.device, getter_name)()
        except tinkerforge.ip_connection.Error as e:
            value = self._exception_msg(e.value, e.description)
        except Exception as ex:
            value = self._exception_msg(str(self.identifier)+"-"+str(var_name), ex)    
        
        self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, var_name, value))

class ComplexDevice(AbstractDevice):
    
    def __init__(self, data, datalogger):
        AbstractDevice.__init__(self, data, datalogger)     
        self.device = self.data[Identifier.DEVICE_CLASS](self.uid, self.datalogger.ipcon)
        self.identifier = self.data[Identifier.DEVICE_CLASS].DEVICE_IDENTIFIER  
        
        self.__name__ = Identifier.COMPLEX_DEVICE

    def start_timer(self):  
        AbstractDevice.start_timer(self)
             
        #start for each variable a timer         
        for value in self.data[Identifier.DEVICE_VALUES]:
            interval = self.data[Identifier.DEVICE_VALUES][value][Identifier.DEVICE_VALUES_INTERVAL]
            func_name = "_timer"
            var_name = value
            self.datalogger.timers.append(utils.LoggerTimer(interval, func_name, var_name, self)) 

    def _timer(self, var_name):        
        values = None
        try:
            getter_name = self.data[Identifier.DEVICE_VALUES][var_name][Identifier.DEVICE_VALUES_NAME]
            getter_args = self.data[Identifier.DEVICE_VALUES][var_name][Identifier.DEVICE_VALUES_ARGS]
        
            #start functions to get values
            if getter_args:
                values = getattr(self.device, getter_name)(*getter_args)
            else:
                values = getattr(self.device, getter_name)()
             
            #check for tuples
            if type(values) is tuple:
                l = list(values)
            else:
                l = []
                l.append(values)

            #get bool and variable to check, which data should be logged
            bools = self.data[Identifier.DEVICE_VALUES][var_name][Identifier.COMPLEX_DEVICE_VALUES_BOOL]
            names = self.data[Identifier.DEVICE_VALUES][var_name][Identifier.COMPLEX_DEVICE_VALUES_NAME]
        
            #if variable bool is not True, dont log the data
            for i in range(0, len(l)):
                if bools[i]:
                    self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, names[i], l[i]))
            
        except tinkerforge.ip_connection.Error as e:
            values = self._exception_msg(e.value, e.description)
            self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, var_name, values))
        except Exception as ex:
            values = self._exception_msg(str(self.identifier)+"-"+str(var_name), ex)    
            self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, var_name, values))        

###Special Devices     
class GPSBricklet(AbstractDevice):
    
    def __init__(self, data, datalogger):
        AbstractDevice.__init__(self, data, datalogger)
      
        self.device = GPS(self.uid, datalogger.ipcon)
        self.identifier = GPS.DEVICE_IDENTIFIER 
        
        self.__name__ = Identifier.SPECIAL_DEVICE

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        
        value1 = self.data[Identifier.SPECIAL_DEVICE_VALUE][Identifier.GPS_COORDINATES]
        value2 = self.data[Identifier.SPECIAL_DEVICE_VALUE][Identifier.GPS_ALTITUDE]
        value3 = self.data[Identifier.SPECIAL_DEVICE_VALUE][Identifier.GPS_MOTION]
        value4 = self.data[Identifier.SPECIAL_DEVICE_VALUE][Identifier.GPS_DATE_TIME]
     
        self.datalogger.timers.append(utils.LoggerTimer(value1, self._timer_coordinates.__name__, Identifier.GPS_COORDINATES, self))  
        self.datalogger.timers.append(utils.LoggerTimer(value2, self._timer_altitude.__name__, Identifier.GPS_ALTITUDE, self)) 
        self.datalogger.timers.append(utils.LoggerTimer(value3, self._timer_motion.__name__, Identifier.GPS_MOTION, self)) 
        self.datalogger.timers.append(utils.LoggerTimer(value4, self._timer_date_time.__name__, Identifier.GPS_DATE_TIME, self)) 
    
    def _timer_coordinates(self, var_name):
        try:
            #check for the FIX Value of get_status()
            fix = self._get_fix_status()
                          
            if fix == GPS.FIX_NO_FIX:
                self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.GPS_COORDINATES, self._exception_msg("Fix-Status="+fix, "GPS Fix-Status was 1, but needs to be 2 or 3 for valid Coordinates.")))
                return

            latitude, ns, longitude, ew, pdop, hdop, vdop, epe = self.device.get_coordinates()     
            #latitude, ns, longitude, ew, pdop, hdop, vdop, epe = self.__TMP_get_coordinates()  #TODO: TMP ONLY       
            if self.data[Identifier.SPECIAL_DEVICE_BOOL][Identifier.GPS_LATITUDE]:
                self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.GPS_LATITUDE, latitude))
            if self.data[Identifier.SPECIAL_DEVICE_BOOL][Identifier.GPS_NS]:
                self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.GPS_NS, ns))
            if self.data[Identifier.SPECIAL_DEVICE_BOOL][Identifier.GPS_LONGITUDE]:
                self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.GPS_LONGITUDE, longitude))
            if self.data[Identifier.SPECIAL_DEVICE_BOOL][Identifier.GPS_EW]:
                self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.GPS_EW, ew))
            if self.data[Identifier.SPECIAL_DEVICE_BOOL][Identifier.GPS_PDOP]:
                self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.GPS_PDOP, pdop))
            if self.data[Identifier.SPECIAL_DEVICE_BOOL][Identifier.GPS_HDOP]:
                self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.GPS_HDOP, hdop))
            if self.data[Identifier.SPECIAL_DEVICE_BOOL][Identifier.GPS_VDOP]:
                self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.GPS_VDOP, vdop))
            if self.data[Identifier.SPECIAL_DEVICE_BOOL][Identifier.GPS_EPE]:
                self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.GPS_EPE, epe))
        except tinkerforge.ip_connection.Error as e:
            self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.GPS_COORDINATES, self._exception_msg(e.value, e.description)))
        except Exception as ex:
            self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.GPS_COORDINATES, self._exception_msg(str(self.identifier)+"-"+str(var_name), ex) ))

    def _timer_altitude(self, var_name):
        try:
            #check for the FIX Value of get_status()
            fix = self._get_fix_status()
               
            if fix != GPS.FIX_3D_FIX:
                self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.GPS_ALTITUDE, self._exception_msg("Fix-Status="+str(fix), "GPS Fix-Status was " + str(fix) + ", but needs to be 3 for valid Altitude Values.")))
                return
 
            altitude, geoidal_separation = self.device.get_altitude()            
            if self.data[Identifier.SPECIAL_DEVICE_BOOL][Identifier.GPS_ALTITUDE_VALUE]:
                self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.GPS_ALTITUDE_VALUE, altitude))
            if self.data[Identifier.SPECIAL_DEVICE_BOOL][Identifier.GPS_GEOIDAL_SEPERATION]:
                self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.GPS_GEOIDAL_SEPERATION, geoidal_separation))
        except tinkerforge.ip_connection.Error as e:
            self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.GPS_ALTITUDE, self._exception_msg(e.value, e.description)))
        except Exception as ex:
            self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.GPS_ALTITUDE, self._exception_msg(str(self.identifier)+"-"+str(var_name), ex) ))

    def _timer_motion(self, var_name):
        try:
            #check for the FIX Value of get_status()
            fix = self._get_fix_status()
               
            if fix == GPS.FIX_NO_FIX:
                self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.GPS_MOTION, self._exception_msg("Fix-Status="+fix, "GPS Fix-Status was " + fix + ", but needs to be 2 or 3 for valid Altitude Values.")))
                return
 
            course, speed = self.device.get_motion()
            if self.data[Identifier.SPECIAL_DEVICE_BOOL][Identifier.GPS_COURSE]:
                self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.GPS_COURSE, course))
            if self.data[Identifier.SPECIAL_DEVICE_BOOL][Identifier.GPS_SPEED]:
                self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.GPS_SPEED, speed))
        except tinkerforge.ip_connection.Error as e:
            self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.GPS_MOTION, self._exception_msg(e.value, e.description)))
        except Exception as ex:
            self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.GPS_MOTION, self._exception_msg(str(self.identifier)+"-"+str(var_name), ex) ))

    def _timer_date_time(self, var_name):
        try:
            date, time = self.device.get_date_time()
            if self.data[Identifier.SPECIAL_DEVICE_BOOL][Identifier.GPS_DATE]:
                self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.GPS_DATE, date))
            if self.data[Identifier.SPECIAL_DEVICE_BOOL][Identifier.GPS_TIME]:
                self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.GPS_TIME, time))
        except Exception as e:
            self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.GPS_DATE_TIME, self._exception_msg(e.value, e.description)))

    def _get_fix_status(self):
        fix, satellites_view, satellites_used = self.device.get_status()
        #fix, satellites_view, satellites_used = self.__TMP_get_status()#TODO: TMP ONLY
         
        if self.data[Identifier.SPECIAL_DEVICE_BOOL][Identifier.GPS_FIX_STATUS]:
            self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.GPS_FIX_STATUS, fix))
        if self.data[Identifier.SPECIAL_DEVICE_BOOL][Identifier.GPS_SATELLITES_VIEW]:
            self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.GPS_SATELLITES_VIEW, satellites_view))
        if self.data[Identifier.SPECIAL_DEVICE_BOOL][Identifier.GPS_SATELLITES_USED]:
            self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.GPS_SATELLITES_USED, satellites_used))
        return fix
    
    #TODO: delete Dummys
    def __TMP_get_status(self):
        #fix, satellites_view, satellites_used
        return (2, 10, 8)

    def __TMP_get_coordinates(self):
        #latitude, ns, longitude, ew, pdop, hdop, vdop, epe
        #int, chr, int, chr, int, int, int, int)
        return (57123468, 'N', 46012357, 'E', 1, 2, 3, 42)

class SegmentDisplay4x7Bricklet(AbstractDevice):
    
    def __init__(self, data, datalogger):
        AbstractDevice.__init__(self, data, datalogger)
    
        self.device = BrickletSegmentDisplay4x7(self.uid, datalogger.ipcon)
        self.identifier = BrickletSegmentDisplay4x7.DEVICE_IDENTIFIER 
        
        self.__name__ = Identifier.SPECIAL_DEVICE
        

    def start_timer(self):
        AbstractDevice.start_timer(self) 
        
        value1 = self.data[Identifier.SPECIAL_DEVICE_VALUE][Identifier.SEGMENT_DISPLAY_4x7_SEGMENTS]
        value2 = self.data[Identifier.SPECIAL_DEVICE_VALUE][Identifier.SEGMENT_DISPLAY_4x7_COUNTER_VALUE]
        
        self.datalogger.timers.append(utils.LoggerTimer(value1, self._timer_segments.__name__, Identifier.SEGMENT_DISPLAY_4x7_SEGMENTS, self)) 
        self.datalogger.timers.append(utils.LoggerTimer(value2, self._timer_counter_value.__name__, Identifier.SEGMENT_DISPLAY_4x7_COUNTER_VALUE, self)) 

    def _timer_segments(self, var_name):
        try:
            segment, brightness, colon = self.device.get_segments()
            #segment, brightness, colon = self.__TMP_GET_SEGMENTS()#TODO: debug only
            if self.data[Identifier.SPECIAL_DEVICE_BOOL][Identifier.SEGMENT_DISPLAY_4x7_Identifier.SEGMENT_1]:
                self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.SEGMENT_DISPLAY_4x7_Identifier.SEGMENT_1, segment[0]))
            if self.data[Identifier.SPECIAL_DEVICE_BOOL][Identifier.SEGMENT_DISPLAY_4x7_Identifier.SEGMENT_2]:
                self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.SEGMENT_DISPLAY_4x7_Identifier.SEGMENT_2, segment[1]))
            if self.data[Identifier.SPECIAL_DEVICE_BOOL][Identifier.SEGMENT_DISPLAY_4x7_Identifier.SEGMENT_3]:
                self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.SEGMENT_DISPLAY_4x7_Identifier.SEGMENT_3, segment[2]))
            if self.data[Identifier.SPECIAL_DEVICE_BOOL][Identifier.SEGMENT_DISPLAY_4x7_Identifier.SEGMENT_4]:
                self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.SEGMENT_DISPLAY_4x7_Identifier.SEGMENT_4, segment[3]))
            if self.data[Identifier.SPECIAL_DEVICE_BOOL][Identifier.SEGMENT_DISPLAY_4x7_BRIGTHNESS]:
                self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.SEGMENT_DISPLAY_4x7_BRIGTHNESS, brightness))
            if self.data[Identifier.SPECIAL_DEVICE_BOOL][Identifier.SEGMENT_DISPLAY_4x7_COLON]:
                self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.SEGMENT_DISPLAY_4x7_COLON, colon))        
        except tinkerforge.ip_connection.Error as e:
            self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.SEGMENT_DISPLAY_4x7_SEGMENTS, self._exception_msg(e.value, e.description)))
        except Exception as ex:
            self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.SEGMENT_DISPLAY_4x7_SEGMENTS, self._exception_msg(str(self.identifier)+"-"+str(var_name), ex) ))

    def _timer_counter_value(self, var_name):
        value = self._try_catch(self.device.get_counter_value)
        self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.SEGMENT_DISPLAY_4x7_COUNTER_VALUE, value))

    def __TMP_GET_SEGMENTS(self):
        #([int, int, int, int], int, bool)
        #segments, brightness und colon.
        return ([1,2,3,4], 50, False)
              
############################################################################################
###NOT SUPPORTED
# from tinkerforge.bricklet_industrial_digital_in_4 import IndustrialDigitalIn4    
# INDUSTRIAL_DIGITAL_IN_4 = "Industrial Digital In 4"
# from tinkerforge.bricklet_industrial_digital_out_4 import IndustrialDigitalOut4    
# INDUSTRIAL_DIGITAL_OUT_4 = "Industrial Digital Out 4"
# from tinkerforge.bricklet_industrial_quad_relay import IndustrialQuadRelay
# INDUSTRIAL_QUAD_RELAY = "Industrial Quad Relay"
# from tinkerforge.bricklet_lcd_16x2 import LCD16x2
# LCD_16x2 = "LCD 16x2"
# from tinkerforge.bricklet_lcd_20x4 import LCD20x4
# LCD_20x4 = "LCD 20x4"
# from tinkerforge.bricklet_nfc_rfid import BrickletNFCRFID
# NFC_RFID = "NFC RFID"
# from tinkerforge.bricklet_piezo_buzzer import BrickletPiezoBuzzer
# PIEZO_BUZZER = "Pirezo Buzzer"
# from tinkerforge.bricklet_piezo_speaker import PiezoSpeaker
# PIEZO_SPEAKER = "Piezo Speaker"
# from tinkerforge.bricklet_remote_switch import RemoteSwitch
# REMOTE_SWITCH = "Remote Switch"
