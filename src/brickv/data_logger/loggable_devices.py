import sys

from brickv.bindings.brick_dc import DC
from brickv.bindings.brick_stepper import Stepper
from brickv.bindings.bricklet_ambient_light import AmbientLight
from brickv.bindings.bricklet_analog_in import AnalogIn
from brickv.bindings.bricklet_analog_out import AnalogOut
from brickv.bindings.bricklet_barometer import Barometer
from brickv.bindings.bricklet_color import Color
from brickv.bindings.bricklet_current12 import Current12
from brickv.bindings.bricklet_current25 import Current25
from brickv.bindings.bricklet_distance_ir import DistanceIR
from brickv.bindings.bricklet_distance_us import DistanceUS
from brickv.bindings.bricklet_dual_button import DualButton
from brickv.bindings.bricklet_dual_relay import DualRelay
from brickv.bindings.bricklet_gps import GPS
from brickv.bindings.bricklet_hall_effect import HallEffect
from brickv.bindings.bricklet_humidity import Humidity
from brickv.bindings.bricklet_industrial_dual_0_20ma import IndustrialDual020mA
from brickv.bindings.bricklet_io16 import IO16
from brickv.bindings.bricklet_io4 import IO4
from brickv.bindings.bricklet_joystick import Joystick
from brickv.bindings.bricklet_led_strip import LEDStrip
from brickv.bindings.bricklet_line import BrickletLine
from brickv.bindings.bricklet_linear_poti import BrickletLinearPoti
from brickv.bindings.bricklet_moisture import Moisture
from brickv.bindings.bricklet_motion_detector import MotionDetector
from brickv.bindings.bricklet_multi_touch import MultiTouch
from brickv.bindings.bricklet_ptc import PTC
from brickv.bindings.bricklet_rotary_encoder import RotaryEncoder
from brickv.bindings.bricklet_rotary_poti import RotaryPoti
from brickv.bindings.bricklet_segment_display_4x7 import BrickletSegmentDisplay4x7
from brickv.bindings.bricklet_solid_state_relay import BrickletSolidStateRelay
from brickv.bindings.bricklet_sound_intensity import BrickletSoundIntensity
from brickv.bindings.bricklet_temperature import BrickletTemperature
from brickv.bindings.bricklet_temperature_ir import BrickletTemperatureIR
from brickv.bindings.bricklet_tilt import BrickletTilt
from brickv.bindings.bricklet_voltage import BrickletVoltage
from brickv.bindings.bricklet_voltage_current import BrickletVoltageCurrent
import brickv.bindings.ip_connection as ip_connection
from brickv.data_logger.event_logger import EventLogger
import brickv.data_logger.utils as utils
from collections import namedtuple


# import ALL supported bricklets and bricks
def string_to_class(string):
    """
    Parses the correct class from a String.
    """
    return reduce(getattr, string.split("."), sys.modules[__name__])

'''
/*---------------------------------------------------------------------------
                                Identifier
 ---------------------------------------------------------------------------*/
 '''
class Identifier(object):
    """
        This class is for all identification strings of the bricklets and bricks.
        It also has function for creating a correct class and function name for
        the correct device.
    """
    
    # creates a function name from device_name and var_name
    def create_function_name(device_name, var_name):
        """
        Creates a correct function name(var_name) as String for the appropriate device_name.
        """
        if Identifier.FUNCTION_NAME.has_key(device_name + var_name):
            return Identifier.FUNCTION_NAME[device_name + var_name]
        return ("get_" + var_name).replace(" ", "_").lower()
    
    def create_class_name(device_name):
        """
        Creates the correct class name as String for the appropriate device_name.
        """
        if Identifier.CLASS_NAME.has_key(device_name):
            return Identifier.CLASS_NAME[device_name]
        return (device_name).replace(" ", "")
    
    def create_args(device_name, var_name):
        """
        Creates the correct arguments for the appropriate device_name and var_name.
        """
        if Identifier.VAR_ARGS.has_key(device_name + var_name):
            return Identifier.VAR_ARGS[device_name + var_name]
        return None
    
    create_function_name = staticmethod(create_function_name)
    create_class_name = staticmethod(create_class_name)
    create_args = staticmethod(create_args)
    
    # ##Devices
    # functions got one return value
    SIMPLE_DEVICE = "SimpleDevice"
    # function can have tuple return value
    COMPLEX_DEVICE = "ComplexDevice"
    # array/multiple return values in tuple (e.g. return ([1,2,3],"a","b","c"))
    # or special rules, e.g. GPS which needs a special FIX value for some functions
    SPECIAL_DEVICE = "SpecialDevice"
    # core 2.0 new identifier
    DEVICES = "Devices"
    
    # config list access strings
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

    # ##Special Identifiers
    FUNCTION_NAME = {}
    CLASS_NAME = {}
    VAR_ARGS = {}

    # ##Bricks
    DC_BRICK = "DC Brick"
    CLASS_NAME[DC_BRICK] = "DC"
    DC_BRICK_VELOCITY = "Velocity"
    DC_BRICK_CURRENT_VELOCITY = "Current Velocity"
    DC_BRICK_ACCELERATION = "Acceleration"
    DC_BRICK_STACK_INPUT_VOLTAGE = "Stack Input Voltage"
    DC_BRICK_EXTERNAL_INTPU_VOLTAGE = "External Input Voltage"
    DC_BRICK_CURRENT_CONSUMPTION = "Current Consumption"
    DC_BRICK_CHIP_TEMPERATURE = "Chip Temperature"
    
    #needs refactoring for namedtuples and api changes!
#     IMU_BRICK = "IMU Brick"
#     CLASS_NAME[IMU_BRICK] = "IMU"
#     IMU_BRICK_ORIENTATION = "Orientation"
#     IMU_BRICK_ORIENTATION_ROLL = "Roll"
#     IMU_BRICK_ORIENTATION_YAW = "Yaw"
#     IMU_BRICK_ORIENTATION_PITCH = "Pitch"
#     IMU_BRICK_QUATERNION = "Quaternion"
#     IMU_BRICK_QUATERNION_X = "X"
#     IMU_BRICK_QUATERNION_Y = "Y"
#     IMU_BRICK_QUATERNION_Z = "Z"
#     IMU_BRICK_QUATERNION_W = "W"
#     IMU_BRICK_ACCELERATION = "Acceleration"
#     IMU_BRICK_ACCELERATION_X = "X"
#     IMU_BRICK_ACCELERATION_Y = "Y"
#     IMU_BRICK_ACCELERATION_Z = "Z"
#     IMU_BRICK_MAGNETIC_FIELD = "Magnetic Field"
#     IMU_BRICK_MAGNETIC_FIELD_X = "X"
#     IMU_BRICK_MAGNETIC_FIELD_Y = "Y"
#     IMU_BRICK_MAGNETIC_FIELD_Z = "Z"
#     IMU_BRICK_ANGULAR_VELOCITY = "Angular Velocity"
#     IMU_BRICK_ANGULAR_VELOCITY_X = "X"
#     IMU_BRICK_ANGULAR_VELOCITY_Y = "Y"
#     IMU_BRICK_ANGULAR_VELOCITY_Z = "Z"
#     IMU_BRICK_IMU_TEMPERATURE = "IMU Temperature"
#     IMU_BRICK_LEDS = "Leds"
#     FUNCTION_NAME[IMU_BRICK + IMU_BRICK_LEDS] = "are_leds_on"
#     IMU_BRICK_CHIP_TEMPERATURE = "Chip Temperature"
    
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
    FUNCTION_NAME[STEPPER_BRICK + STEPPER_BRICK_SNYC_RECT] = "is_sync_rect"

    # ##Bricklets
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
    COLOR_RED = "r"
    COLOR_GREEN = "g"
    COLOR_BLUE = "b"
    COLOR_CLEAR = "c"
    COLOR_COLOR = "Rgbc"
    FUNCTION_NAME[COLOR + COLOR_COLOR] = "get_color"
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
    FUNCTION_NAME[DISTANCE_US + DISTANCE_US_DISTANCE] = "get_distance_value"
    
    DUAL_BUTTON = "Dual Button"
    DUAL_BUTTON_BUTTONS = "Buttons"
    FUNCTION_NAME[DUAL_BUTTON + DUAL_BUTTON_BUTTONS] = "get_button_state"
    DUAL_BUTTON_BUTTON_L = "button_l"
    DUAL_BUTTON_BUTTON_R = "button_r"
    DUAL_BUTTON_LEDS = "Leds"
    FUNCTION_NAME[DUAL_BUTTON + DUAL_BUTTON_LEDS] = "get_led_state"
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
    FUNCTION_NAME[INDUSTRIAL_DUAL_0_20_MA + INDUSTRIAL_DUAL_0_20_MA_SENSOR_0] = "get_current"
    VAR_ARGS[INDUSTRIAL_DUAL_0_20_MA + INDUSTRIAL_DUAL_0_20_MA_SENSOR_0] = [0]
    INDUSTRIAL_DUAL_0_20_MA_SENSOR_1 = "Sensor 1"
    FUNCTION_NAME[INDUSTRIAL_DUAL_0_20_MA + INDUSTRIAL_DUAL_0_20_MA_SENSOR_1] = "get_current"
    VAR_ARGS[INDUSTRIAL_DUAL_0_20_MA + INDUSTRIAL_DUAL_0_20_MA_SENSOR_1] = [1]
    
    IO_16 = "IO-16"
    CLASS_NAME[IO_16] = "IO16"
    IO_16_PORTS = "Ports"
    IO_16_PORT_A = "Port A"
    FUNCTION_NAME[IO_16 + IO_16_PORT_A] = "get_port"
    VAR_ARGS[IO_16 + IO_16_PORT_A] = ["a"]
    IO_16_PORT_B = "Port B"
    FUNCTION_NAME[IO_16 + IO_16_PORT_B] = "get_port"
    VAR_ARGS[IO_16 + IO_16_PORT_B] = ["b"]
    
    IO_4 = "IO-4"
    CLASS_NAME[IO_4] = "IO4"
    IO_4_VALUE = "Value"
    
    JOYSTICK = "Joystick"
    JOYSTICK_POSITION = "Position"
    JOYSTICK_POSITION_X = "x"
    JOYSTICK_POSITION_Y = "y"
    JOYSTICK_ANALOG_VALUE = "Analog Value"
    JOYSTICK_PRESSED = "Pressed"
    FUNCTION_NAME[JOYSTICK + JOYSTICK_PRESSED] = "is_pressed"
    
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
    FUNCTION_NAME[ROTARY_ENCODER + ROTARY_ENCODER_PRESSED] = "is_pressed"
    
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
    TEMPERATURE_IR_OBJECT_TEMPERATURE = "Object Temperature"
    
    TILT = "Tilt"
    CLASS_NAME[TILT] = "BrickletTilt"
    TILT_STATE = "State"
    FUNCTION_NAME[TILT + TILT_STATE] = "get_tilt_state"
    
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
    GPS_DATE = "Date"
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

'''
/*---------------------------------------------------------------------------
                                AbstractDevice
 ---------------------------------------------------------------------------*/
 '''
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
        """
        Starts all timer for all loggable variables of the devices.
        """
        EventLogger.debug(self.__str__())
                
    def _try_catch(self, func):
        """
        Creates a simple try-catch for a specific funtion.
        """
        value = "[NYI-FAIL-TIMER]"
        # err = 0
        try:
            value = func()
        except Exception as e:
            value = self._exception_msg(e.value, e.description)
            # err = 1
        return value
    
    def _exception_msg(self, value, msg):
        """
        For a uniform creation of Exception messages.
        """
        return "ERROR[" + str(value) + "]: " + str(msg)
    
    def __str__(self):
        """
        Representation String of the class. For simple overwiev.
        """
        return "[" + self.__name__ + "=" + str(self.data[Identifier.DEVICE_CLASS]) + " | <UID=" + str(self.uid) + "> | <IDENTIEFIER=" + str(self.identifier) + "> | <data=" + str(self.data) + ">]"

'''
/*---------------------------------------------------------------------------
                                SimpleDevice
 ---------------------------------------------------------------------------*/
 '''
class SimpleDevice(AbstractDevice):
    """
    A SimpleDevice is every device, which only has funtion with one return value.
    """
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
        """
        This function is used by the LoggerTimer to get the variable values from the brickd.
        In SimpleDevices the get-functions only return one value.
        """
        # CSVDATA=[uid->memeber, name/identety->member, var_name->parameter, raw_data->function]
        value = None
        try:
            getter_name = self.data[Identifier.DEVICE_VALUES][var_name][Identifier.DEVICE_VALUES_NAME]
            getter_args = self.data[Identifier.DEVICE_VALUES][var_name][Identifier.DEVICE_VALUES_ARGS]
        
            if getter_args:
                # FIXME: find better solution for the unicode problem!
                for i in range(len(getter_args)):
                    if type(getter_args[i]) == unicode:
                        getter_args[i] = str(getter_args[i])
                
                value = getattr(self.device, getter_name)(*getter_args)
            else:
                value = getattr(self.device, getter_name)()
        except ip_connection.Error as e:
            value = self._exception_msg(e.value, e.description)
        except Exception as ex:
            value = self._exception_msg(str(self.identifier) + "-" + str(var_name), ex)
        
        self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, var_name, value))

'''
/*---------------------------------------------------------------------------
                                SimpleDevice
 ---------------------------------------------------------------------------*/
 '''
class ComplexDevice(AbstractDevice):
    
    def __init__(self, data, datalogger):
        AbstractDevice.__init__(self, data, datalogger)
        self.device = self.data[Identifier.DEVICE_CLASS](self.uid, self.datalogger.ipcon)
        self.identifier = self.data[Identifier.DEVICE_CLASS].DEVICE_IDENTIFIER
        
        self.__name__ = Identifier.COMPLEX_DEVICE

    def start_timer(self):
        AbstractDevice.start_timer(self)
             
        # start for each variable a timer
        for value in self.data[Identifier.DEVICE_VALUES]:
            interval = self.data[Identifier.DEVICE_VALUES][value][Identifier.DEVICE_VALUES_INTERVAL]
            func_name = "_timer"
            var_name = value
            self.datalogger.timers.append(utils.LoggerTimer(interval, func_name, var_name, self))

    def _timer(self, var_name):
        """
        This function is used by the LoggerTimer to get the variable values from the brickd.
        In ComplexDevice the get-functions return one or multiple(as tupel) values.
        """
        values = None
        try:
            getter_name = self.data[Identifier.DEVICE_VALUES][var_name][Identifier.DEVICE_VALUES_NAME]
            getter_args = self.data[Identifier.DEVICE_VALUES][var_name][Identifier.DEVICE_VALUES_ARGS]
        
            # start functions to get values
            if getter_args:
                # FIXME: find better solution for the unicode problem!
                for i in range(len(getter_args)):
                    if type(getter_args[i]) == unicode:
                        getter_args[i] = str(getter_args[i])
                
                values = getattr(self.device, getter_name)(*getter_args)
            else:
                values = getattr(self.device, getter_name)()
            
            # get bool and variable to check, which data should be logged
            bools = self.data[Identifier.DEVICE_VALUES][var_name][Identifier.COMPLEX_DEVICE_VALUES_BOOL]
            names = self.data[Identifier.DEVICE_VALUES][var_name][Identifier.COMPLEX_DEVICE_VALUES_NAME]
            
            l = [] #values
            n = [] #identifeir of the namedtuple
            if type(values) is not int and type(values) is not bool and type(values) is not float and type(values) is not long:
                for v_name in values._fields:
                    l.append(getattr(values, v_name))
                    n.append(v_name)
            else:                
                l.append(values)
                n.append(names[0])

            #check, which variable should be logged
            for j in range(0, len(n)):
                for i in range(0, len(names)):
                    if n[j] == names[i]:
                        if bools[i]:
                            self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, names[i], l[j]))
            
        except ip_connection.Error as e:
            values = self._exception_msg(e.value, e.description)
            self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, var_name, values))
        except Exception as ex:
            values = self._exception_msg(str(self.identifier) + "-" + str(var_name), ex)
            self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, var_name, values))

# ##Special Devices
'''
/*---------------------------------------------------------------------------
                                GPSBricklet
 ---------------------------------------------------------------------------*/
 '''
class GPSBricklet(AbstractDevice):
    """
    The GPSBricklet is a special device. Because of the special behavior, that
    some values should only be logged if others are at a certain point, the
    GPSBricklet needs a own class.
    """
    def __init__(self, data, datalogger):
        AbstractDevice.__init__(self, data, datalogger)
      
        self.device = GPS(self.uid, datalogger.ipcon)
        self.identifier = GPS.DEVICE_IDENTIFIER
        
        self.__name__ = Identifier.SPECIAL_DEVICE

    def start_timer(self):
        """
        Starts all timer for all loggable variables of the devices.
        """
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
        """
        LoggerTimer function to get the GPS coordinates. Should only log the coordiantes when the GPS.FIX is greater or equal 2.
        """
        try:
            # check for the FIX Value of get_status()
            fix = self._get_fix_status()
                          
            if fix == GPS.FIX_NO_FIX:
                self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.GPS_COORDINATES, self._exception_msg("Fix-Status=" + str(fix), "GPS Fix-Status was 1, but needs to be 2 or 3 for valid Coordinates.")))
                return

            latitude, ns, longitude, ew, pdop, hdop, vdop, epe = self.device.get_coordinates()
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
        except ip_connection.Error as e:
            self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.GPS_COORDINATES, self._exception_msg(e.value, e.description)))
        except Exception as ex:
            self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.GPS_COORDINATES, self._exception_msg(str(self.identifier) + "-" + str(var_name), ex)))

    def _timer_altitude(self, var_name):
        """
        LoggerTimer function to get the GPS altitude. Should only log the altitude when the GPS.FIX is equal 3.
        """
        try:
            # check for the FIX Value of get_status()
            fix = self._get_fix_status()
               
            if fix != GPS.FIX_3D_FIX:
                self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.GPS_ALTITUDE, self._exception_msg("Fix-Status=" + str(fix), "GPS Fix-Status was " + str(fix) + ", but needs to be 3 for valid Altitude Values.")))
                return
 
            altitude, geoidal_separation = self.device.get_altitude()
            if self.data[Identifier.SPECIAL_DEVICE_BOOL][Identifier.GPS_ALTITUDE_VALUE]:
                self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.GPS_ALTITUDE_VALUE, altitude))
            if self.data[Identifier.SPECIAL_DEVICE_BOOL][Identifier.GPS_GEOIDAL_SEPERATION]:
                self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.GPS_GEOIDAL_SEPERATION, geoidal_separation))
        except ip_connection.Error as e:
            self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.GPS_ALTITUDE, self._exception_msg(e.value, e.description)))
        except Exception as ex:
            self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.GPS_ALTITUDE, self._exception_msg(str(self.identifier) + "-" + str(var_name), ex)))

    def _timer_motion(self, var_name):
        """
        LoggerTimer function to get the GPS motion. Should only log the motion when the GPS.FIX is greater or equal 2.
        """
        try:
            # check for the FIX Value of get_status()
            fix = self._get_fix_status()
               
            if fix == GPS.FIX_NO_FIX:
                self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.GPS_MOTION, self._exception_msg("Fix-Status=" + str(fix), "GPS Fix-Status was " + str(fix) + ", but needs to be 2 or 3 for valid Altitude Values.")))
                return
 
            course, speed = self.device.get_motion()
            if self.data[Identifier.SPECIAL_DEVICE_BOOL][Identifier.GPS_COURSE]:
                self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.GPS_COURSE, course))
            if self.data[Identifier.SPECIAL_DEVICE_BOOL][Identifier.GPS_SPEED]:
                self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.GPS_SPEED, speed))
        except ip_connection.Error as e:
            self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.GPS_MOTION, self._exception_msg(e.value, e.description)))
        except Exception as ex:
            self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.GPS_MOTION, self._exception_msg(str(self.identifier) + "-" + str(var_name), ex)))

    def _timer_date_time(self, var_name):
        """
        LoggerTimer function to get the GPS date.
        """
        try:
            date, time = self.device.get_date_time()
            if self.data[Identifier.SPECIAL_DEVICE_BOOL][Identifier.GPS_DATE]:
                self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.GPS_DATE, date))
            if self.data[Identifier.SPECIAL_DEVICE_BOOL][Identifier.GPS_TIME]:
                self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.GPS_TIME, time))
        except Exception as e:
            self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.GPS_DATE_TIME, self._exception_msg(e.value, e.description)))

    def _get_fix_status(self):
        """
        Fix-Status function. Returns the current Fix-Status for other functions
        """
        fix, satellites_view, satellites_used = self.device.get_status()
         
        if self.data[Identifier.SPECIAL_DEVICE_BOOL][Identifier.GPS_FIX_STATUS]:
            self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.GPS_FIX_STATUS, fix))
        if self.data[Identifier.SPECIAL_DEVICE_BOOL][Identifier.GPS_SATELLITES_VIEW]:
            self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.GPS_SATELLITES_VIEW, satellites_view))
        if self.data[Identifier.SPECIAL_DEVICE_BOOL][Identifier.GPS_SATELLITES_USED]:
            self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.GPS_SATELLITES_USED, satellites_used))
        return fix

'''
/*---------------------------------------------------------------------------
                                SegmentDisplay4x7Bricklet
 ---------------------------------------------------------------------------*/
 '''
class SegmentDisplay4x7Bricklet(AbstractDevice):
    """
    The SegmentDisplay4x7Bricklet is a special device. It's function returns a combination of
    multiple values and a list. Because of this, the device needs special attention and it's
    own class.
    """
    def __init__(self, data, datalogger):
        AbstractDevice.__init__(self, data, datalogger)
    
        self.device = BrickletSegmentDisplay4x7(self.uid, datalogger.ipcon)
        self.identifier = BrickletSegmentDisplay4x7.DEVICE_IDENTIFIER
        
        self.__name__ = Identifier.SPECIAL_DEVICE
        

    def start_timer(self):
        """
        Starts all timer for all loggable variables of the devices.
        """
        AbstractDevice.start_timer(self)
        
        value1 = self.data[Identifier.SPECIAL_DEVICE_VALUE][Identifier.SEGMENT_DISPLAY_4x7_SEGMENTS]
        value2 = self.data[Identifier.SPECIAL_DEVICE_VALUE][Identifier.SEGMENT_DISPLAY_4x7_COUNTER_VALUE]
        
        self.datalogger.timers.append(utils.LoggerTimer(value1, self._timer_segments.__name__, Identifier.SEGMENT_DISPLAY_4x7_SEGMENTS, self))
        self.datalogger.timers.append(utils.LoggerTimer(value2, self._timer_counter_value.__name__, Identifier.SEGMENT_DISPLAY_4x7_COUNTER_VALUE, self))

    def _timer_segments(self, var_name):
        """
        LoggerTimer function to log some variables of SegmentDisplay4x7Bricklet.
        """
        try:
            segment, brightness, colon = self.device.get_segments()

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
        except ip_connection.Error as e:
            self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.SEGMENT_DISPLAY_4x7_SEGMENTS, self._exception_msg(e.value, e.description)))
        except Exception as ex:
            self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.SEGMENT_DISPLAY_4x7_SEGMENTS, self._exception_msg(str(self.identifier) + "-" + str(var_name), ex)))

    def _timer_counter_value(self, var_name):
        """
        LoggerTimer function to log the counter value of SegmentDisplay4x7Bricklet.
        """
        value = self._try_catch(self.device.get_counter_value)
        self.datalogger.add_to_queue(utils.CSVData(self.uid, self.identifier, Identifier.SEGMENT_DISPLAY_4x7_COUNTER_VALUE, value))
              
############################################################################################
# ##NOT SUPPORTED
# INDUSTRIAL_DIGITAL_IN_4 = "Industrial Digital In 4"
# INDUSTRIAL_DIGITAL_OUT_4 = "Industrial Digital Out 4"
# INDUSTRIAL_QUAD_RELAY = "Industrial Quad Relay"
# LCD_16x2 = "LCD 16x2"
# LCD_20x4 = "LCD 20x4"
# NFC_RFID = "NFC RFID"
# PIEZO_BUZZER = "Pirezo Buzzer"
# PIEZO_SPEAKER = "Piezo Speaker"
# REMOTE_SWITCH = "Remote Switch"
# from brickv.bindings.brick_imu import IMU #API changes not supported at the moment!
