import sys, tinkerforge, utils, data_logger

#import ALL supported bricklets and bricks
from tinkerforge.brick_dc import DC
from tinkerforge.brick_imu import IMU
from tinkerforge.brick_stepper import Stepper

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
    
    #creates a function name from device_name and var_name
    def create_function_name(device_name, var_name):
        if Identifier.FUNCTION_NAME.has_key(device_name+var_name):
            return Identifier.FUNCTION_NAME[device_name+var_name]
        return ("get_"+var_name).replace(" ", "_").lower()
    
    def create_class_name(device_name):
        if Identifier.CLASS_NAME.has_key(device_name):
            return Identifier.CLASS_NAME[device_name]
        return (device_name).replace(" ", "")
    
    create_function_name = staticmethod(create_function_name)
    create_class_name = staticmethod(create_class_name)
    
    ###Devices
    #one return value
    SIMPLE_DEVICE = "SimpleDevice"
    #tuple return value
    COMPLEX_DEVICE = "ComplexDevice"
    #array/multiple return values in tuple (e.g. return ([1,2,3],"a","b","c"))
    #or special rules, e.g. GPS which needs a special FIX value for some functions
    SPECIAL_DEVICE = "SpecialDevice"
    
    DEVICE_NAME = "name"
    DEVICE_CLASS = "class"
    DEVICE_UID = "uid"
    DEVICE_VALUES = "values"
    DEVICE_VALUES_NAME = "func_name"
    DEVICE_VALUES_ARGS = "args"
    DEVICE_VALUES_INTERVAL = "interval"
    
    COMPLEX_DEVICE_VALUES_NAME = "var_name"
    COMPLEX_DEVICE_VALUES_BOOL = "var_bool"
    
    SPECIAL_DEVICE_VALUE = "special_values"
    SPECIAL_DEVICE_BOOL = "special_bool"

    ###Special Identifiers
    FUNCTION_NAME = {}
    CLASS_NAME = {}

    ###Bricks
    DC_BRICK = "DC Brick"
    CLASS_NAME[DC_BRICK] = "DC"
    DC_BRICK_VELOCITY = "Velocity"
    DC_BRICK_CURRENT_VELOCITY = "Current Velocity"
    DC_BRICK_ACCELERATION = "Acceleration"
    DC_BRICK_STACK_INPUT_VOLTAGE = "Stack Input Voltage"
    DC_BRICK_EXTERNAL_INTPU_VOLTAGE = "External Input Voltage"
    DC_BRICK_CURRENT_CONSUMPTION = "Current Consumption"
    DC_BRICK_CHIP_TEMPERATURE = "Chip Temperature"
    
    IMU_BRICK = "IMU Brick"
    CLASS_NAME[IMU_BRICK] = "IMU"
    IMU_BRICK_ORIENTATION = "Orientation"
    IMU_BRICK_ORIENTATION_ROLL = "Roll"
    IMU_BRICK_ORIENTATION_YAW = "Yaw"
    IMU_BRICK_ORIENTATION_PITCH = "Pitch"
    IMU_BRICK_QUATERNION = "Quaternion"
    IMU_BRICK_QUATERNION_X = "X"
    IMU_BRICK_QUATERNION_Y = "Y"
    IMU_BRICK_QUATERNION_Z = "Z"
    IMU_BRICK_QUATERNION_W = "W"   
    IMU_BRICK_ACCELERATION = "Acceleration"
    IMU_BRICK_ACCELERATION_X = "X"
    IMU_BRICK_ACCELERATION_Y = "Y"
    IMU_BRICK_ACCELERATION_Z = "Z"
    IMU_BRICK_MAGNETIC_FIELD = "Magnetic Field"
    IMU_BRICK_MAGNETIC_FIELD_X = "X"
    IMU_BRICK_MAGNETIC_FIELD_Y = "Y"
    IMU_BRICK_MAGNETIC_FIELD_Z = "Z"
    IMU_BRICK_ANGULAR_VELOCITY = "Angular Velocity"
    IMU_BRICK_ANGULAR_VELOCITY_X = "X"
    IMU_BRICK_ANGULAR_VELOCITY_Y = "Y"
    IMU_BRICK_ANGULAR_VELOCITY_Z = "Z"
    IMU_BRICK_IMU_TEMPERATURE = "IMU Temperature"
    IMU_BRICK_LEDS = "Leds"
    FUNCTION_NAME[IMU_BRICK+IMU_BRICK_LEDS] = "are_leds_on"
    IMU_BRICK_CHIP_TEMPERATURE = "Chip Temperature"
    
    STEPPER_BRICK = "Stepper Brick"
    CLASS_NAME[STEPPER_BRICK] = "Stepper"
    STEPPER_BRICK_CURRENT_VELOCITY = "Current Velocity"
    STEPPER_BRICK_STEPS = "Steps"
    STEPPER_BRICK_REMAINING_STEPS = "Remaining Steps"
    STEPPER_BRICK_CURRENT_POSITION = "Current Position"
    STEPPER_BRICK_STACK_INPUT_VOLTAGE = "Stack Input Voltage"
    STEPPER_BRICK_EXTERNAL_INPUT_VOLTAGE = "External Input Voltage"
    STEPPER_BRICK_CURRENT_CONSUMPTION = "Current Consumption"
    STEPPER_BRICK_SNYC_RECT = "Sync Rect"
    FUNCTION_NAME[STEPPER_BRICK+STEPPER_BRICK_SNYC_RECT] = "is_sync_rect"

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
    FUNCTION_NAME[COLOR+COLOR_COLOR] = "get_color"
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
    FUNCTION_NAME[DISTANCE_US+DISTANCE_US_DISTANCE] = "get_distance_value"
    
    DUAL_BUTTON = "Dual Button"
    DUAL_BUTTON_BUTTONS = "Buttons"
    FUNCTION_NAME[DUAL_BUTTON+DUAL_BUTTON_BUTTONS] = "get_button_state"
    DUAL_BUTTON_BUTTON_L = "button_l"
    DUAL_BUTTON_BUTTON_R = "button_r"
    DUAL_BUTTON_LEDS = "Leds"
    FUNCTION_NAME[DUAL_BUTTON+DUAL_BUTTON_LEDS] = "get_led_state"
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
    FUNCTION_NAME[INDUSTRIAL_DUAL_0_20_MA+INDUSTRIAL_DUAL_0_20_MA_SENSOR_0] = "get_current"
    INDUSTRIAL_DUAL_0_20_MA_SENSOR_1 = "Sensor 1"
    FUNCTION_NAME[INDUSTRIAL_DUAL_0_20_MA+INDUSTRIAL_DUAL_0_20_MA_SENSOR_1] = "get_current"
    
    IO_16 = "IO-16"
    CLASS_NAME[IO_16] = "IO16"
    IO_16_PORTS = "Ports"
    IO_16_PORT_A = "Port A"
    FUNCTION_NAME[IO_16+IO_16_PORT_A] = "get_port"
    IO_16_PORT_B = "Port B"
    FUNCTION_NAME[IO_16+IO_16_PORT_B] = "get_port"
    
    IO_4 = "IO-4"
    CLASS_NAME[IO_4] = "IO4"
    IO_4_VALUE = "Value"
    
    JOYSTICK = "Joystick"
    JOYSTICK_POSITION = "Position"
    JOYSTICK_POSITION_X = "Position X"
    JOYSTICK_POSITION_Y = "Position Y"
    JOYSTICK_ANALOG_VALUE = "Analog Value"
    JOYSTICK_PRESSED = "Pressed"
    FUNCTION_NAME[JOYSTICK+JOYSTICK_PRESSED] = "is_pressed"
    
    LED_STRIP = "LED Strip"
    LED_STRIP_SUPPLY_VOLTAGE = "Supply Voltage"
    
    LINE = "Line"
    CLASS_NAME[LINE] = "BrickletLine"
    LINE_REFLECTIVITY = "Reflectivity"
    
    LINEAR_POTI = "Linear Poti"
    CLASS_NAME[LINEAR_POTI] = "BrickletLinearPoti"
    LINEAR_POTI_POSITION = "Position"
    LINEAR_POTI_ANALOG_VALUE = "Analog Value"
    
    MOISTURE = "Moisture"
    MOISTURE_MOISTURE_VALUE = "Moisture Value"
    
    MOTION_DETECTOR = "Motion Detector"
    MOTION_DETECTOR_MOTION_DETECTED = "Motion Detected"
    
    MULTI_TOUCH = "Multi Touch"
    MULTI_TOUCH_TOUCH_STATE = "Touch State"
    
    PTC_BRICKLET = "PTC"
    PTC_BRICKLET_RESISTANCE = "Resistance"
    PTC_BRICKLET_TEMPERATURE = "Temperature"
    
    ROTARY_ENCODER = "Rotary Encoder"
    ROTARY_ENCODER_COUNT = "Count"
    ROTARY_ENCODER_PRESSED = "Pressed"
    FUNCTION_NAME[ROTARY_ENCODER+ROTARY_ENCODER_PRESSED] = "is_pressed"
    
    ROTARY_POTI = "Rotary Poti"
    ROTARY_POTI_POSITION = "Position"
    ROTARY_POTI_ANALOG_VALUE = "Analog Value"
    
    SOLID_STATE_RELAY = "Solid State Relay"
    CLASS_NAME[SOLID_STATE_RELAY] = "BrickletSolidStateRelay"
    SOLID_STATE_RELAY_STATE = "State"
    
    SOUND_INTENSITY = "Sound Intensity"
    CLASS_NAME[SOUND_INTENSITY] = "BrickletSoundIntensity"
    SOUND_INTENSITY_INTENSITY = "Intensity"
    
    TEMPERATURE = "Temperature"
    CLASS_NAME[TEMPERATURE] = "BrickletTemperature"
    TEMPERATURE_TEMPERATURE = "Temperature"
    
    TEMPERATURE_IR = "Temperature IR"
    CLASS_NAME[TEMPERATURE_IR] = "BrickletTemperatureIR"
    TEMPERATURE_IR_AMBIENT_TEMPERATURE = "Ambient Temperature"
    TEMPERATURE_IR_OBJECT_TEMPERATURE ="Object Temperature"
    
    TILT = "Tilt"
    CLASS_NAME[TILT] = "BrickletTilt"
    TILT_STATE = "State"
    FUNCTION_NAME[TILT+TILT_STATE] = "get_tilt_state"
    
    VOLTAGE = "Voltage"
    CLASS_NAME[VOLTAGE] = "BrickletVoltage"
    VOLTAGE_VOLTAGE = "Voltage"
    VOLTAGE_ANALOG_VALUE = "Analog Value"
    
    VOLTAGE_CURRENT = "Voltage Current"
    CLASS_NAME[VOLTAGE_CURRENT] = "BrickletVoltageCurrent"
    VOLTAGE_CURRENT_CURRENT = "Current"
    VOLTAGE_CURRENT_VOLTAGE = "Voltage"
    VOLTAGE_CURRENT_POWER = "Power"

    GPS_BRICKLET = "GPS"
    CLASS_NAME[GPS_BRICKLET] = "GPSBricklet"
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
    CLASS_NAME[SEGMENT_DISPLAY_4x7] = "SegmentDisplay4x7Bricklet"
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
                #FIXME: find better solution for the unicode problem!
                for i in range(len(getter_args)):
                    if type(getter_args[i]) == unicode:
                        getter_args[i] = str(getter_args[i])
                
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
                #FIXME: find better solution for the unicode problem!
                for i in range(len(getter_args)):
                    if type(getter_args[i]) == unicode:
                        getter_args[i] = str(getter_args[i])
                
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
