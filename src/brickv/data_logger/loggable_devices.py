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

class SpecialDevices(object):

    #GPS
    def get_gps_coordinates(device):
        if device.get_status()[0] == GPS.FIX_NO_FIX:
            raise Exception('No fix')
        else:
            return device.get_coordinates()
    get_gps_coordinates = staticmethod(get_gps_coordinates)

    def get_gps_altitude(device):
        if device.get_status()[0] != GPS.FIX_3D_FIX:
            raise Exception('No 3D fix')
        else:
            return device.get_altitude()
    get_gps_altitude = staticmethod(get_gps_altitude)

    def get_gps_motion(device):
        if device.get_status()[0] == GPS.FIX_NO_FIX:
            raise Exception('No fix')
        else:
            return device.get_motion()
    get_gps_motion = staticmethod(get_gps_motion)

    #PTC
    def get_ptc_temperature(device):
        if not device.is_sensor_connected():
            raise Exception('No sensor')
        else:
            return device.get_temperature()
    get_ptc_temperature = staticmethod(get_ptc_temperature)

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
    # core 2.0 new identifier
    DEVICES = "DEVICES"
    
    # config list access strings
    DEVICE_NAME = "name"
    DEVICE_CLASS = "class"
    DEVICE_UID = "uid"
    DEVICE_VALUES = "values"
    DEVICE_VALUES_INTERVAL = "interval"
    #Device Definitions Keys
    DEVICE_DEFINITIONS_GETTER = "getter"
    DEVICE_DEFINITIONS_SUBVALUES = "subvalues"

    #Device Definitons
    DEVICE_DEFINITIONS = {
        AmbientLight.DEVICE_DISPLAY_NAME: {
            'class': AmbientLight,
            'values': {
                'Analog Value': {
                    'getter': lambda device: device.get_analog_value(),
                    'subvalues': None
                },
                'Illuminance': {
                    'getter': lambda device: device.get_illuminance(),
                    'subvalues': None
                }
            }
        },
        AnalogIn.DEVICE_DISPLAY_NAME: {
            'class': AnalogIn,
            'values': {
                'Analog Value': {
                    'getter': lambda device: device.get_analog_value(),
                    'subvalues': None
                },
                'Voltage': {
                    'getter': lambda device: device.get_voltage(),
                    'subvalues': None
                }
            }
        },
        AnalogOut.DEVICE_DISPLAY_NAME: {
            'class': AnalogOut,
            'values': {
                'Voltage': {
                    'getter': lambda device: device.get_voltage(),
                    'subvalues': None
                }
            }
        },
        Barometer.DEVICE_DISPLAY_NAME: {
            'class': Barometer,
            'values': {
                'Air Pressure': {
                    'getter': lambda device: device.get_air_pressure(),
                    'subvalues': None
                },
                'Altitude': {
                    'getter': lambda device: device.get_altitude(),
                    'subvalues': None
                },
                'Chip Temperature': {
                    'getter': lambda device: device.get_chip_temperature(),
                    'subvalues': None
                }
            }
        },
        Color.DEVICE_DISPLAY_NAME: {
            'class': Color,
            'values': {
                'Color': {
                    'getter': lambda device: device.get_color(),
                    'subvalues': ['Red', 'Green', 'Blue', 'Clear']
                },
                'Illuminance': {
                    'getter': lambda device: device.get_illuminance(),
                    'subvalues': None
                },
                'Color Temperature': {
                    'getter': lambda device: device.get_color_temperature(),
                    'subvalues': None
                }
            }
        },
        Current12.DEVICE_DISPLAY_NAME: {
            'class': Current12,
            'values': {
                'Analog Value': {
                    'getter': lambda device: device.get_analog_value(),
                    'subvalues': None
                },
                'Current': {
                    'getter': lambda device: device.get_current(),
                    'subvalues': None
                }
            }
        },
        Current25.DEVICE_DISPLAY_NAME: {
            'class': Current25,
            'values': {
                'Analog Value': {
                    'getter': lambda device: device.get_analog_value(),
                    'subvalues': None
                },
                'Current': {
                    'getter': lambda device: device.get_current(),
                    'subvalues': None
                }
            }
        },
        DistanceIR.DEVICE_DISPLAY_NAME: {
            'class': DistanceIR,
            'values': {
                'Analog Value': {
                    'getter': lambda device: device.get_analog_value(),
                    'subvalues': None
                },
                'Distance': {
                    'getter': lambda device: device.get_distance(),
                    'subvalues': None
                }
            }
        },
        DistanceUS.DEVICE_DISPLAY_NAME: {
            'class': DistanceUS,
            'values': {
                'Distance': {
                    'getter': lambda device: device.get_distance_value(),
                    'subvalues': None
                }
            }
        },
        DualButton.DEVICE_DISPLAY_NAME: {
            'class': DualButton,
            'values': {
                'Button State': {
                    'getter': lambda device: device.get_button_state(),
                    'subvalues': ['Left', 'Right']
                },
                'Led State': {
                    'getter': lambda device: device.get_led_state(),
                    'subvalues': ['Left', 'Right']
                }
            }
        },
        GPS.DEVICE_DISPLAY_NAME: {
            'class': GPS,
            'values': {
                'Altitude': {
                    'getter': SpecialDevices.get_gps_altitude,
                    'subvalues': ['Altitude', 'Geoidal Separation']
                },
                'Coordinates': {
                    'getter': SpecialDevices.get_gps_coordinates,
                    'subvalues': ['Latitude', 'NS', 'Longitude', 'EW', 'PDOP', 'HDOP', 'VDOP', 'EPE']
                },
                'Date Time': {
                    'getter': lambda device: device.get_date_time(),
                    'subvalues': ['Date', 'Time']
                },
                'Motion': {
                    'getter': SpecialDevices.get_gps_motion,
                    'subvalues': ['Course', 'Speed']
                },
                'Status': {
                    'getter': lambda device: device.get_status(),
                    'subvalues': ['Fix', 'Satellites View', 'Satellites Used']
                }
            }
        },

        BrickletSegmentDisplay4x7.DEVICE_DISPLAY_NAME: {
            'class': BrickletSegmentDisplay4x7,
            'values': {
                'Counter Value': {
                    'getter': lambda device: device.get_counter_value(),
                    'subvalues': None
                },
                'Segments': {
                    'getter': lambda device: device.get_segments(),
                    'subvalues': [['Segm1','Segm2','Segm3','Segm4'],'Brightness','Colon']
                }
            }
        }
    }
    # ##Special Identifiers
    FUNCTION_NAME = {}
    CLASS_NAME = {}
    VAR_ARGS = {}
    # ##Bricklets
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

    #TODO needs attention -> check device definition
    DUAL_BUTTON = "Dual Button"
    DUAL_BUTTON_BUTTONS = "Buttons"
    FUNCTION_NAME[DUAL_BUTTON + DUAL_BUTTON_BUTTONS] = "get_button_state"
    DUAL_BUTTON_BUTTON_L = "button_l"
    DUAL_BUTTON_BUTTON_R = "button_r"
    DUAL_BUTTON_LEDS = "Leds"
    FUNCTION_NAME[DUAL_BUTTON + DUAL_BUTTON_LEDS] = "get_led_state"
    DUAL_BUTTON_LED_L = "led_l"
    DUAL_BUTTON_LED_R = "led_r"

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
        self.identifier = None
        
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
        return "["+str(self.__name__)+"TODO NEW DEBUG STRING]"

'''
/*---------------------------------------------------------------------------
                                DeviceImpl
 ---------------------------------------------------------------------------*/
 '''
class DeviceImpl(AbstractDevice):
    """
    A SimpleDevice is every device, which only has funtion with one return value.
    """
    def __init__(self, data, datalogger):
        AbstractDevice.__init__(self, data, datalogger)

        self.device_name = self.data[Identifier.DEVICE_NAME]
        self.device_uid = self.data[Identifier.DEVICE_UID]
        self.device_definition = Identifier.DEVICE_DEFINITIONS[self.device_name]
        device_class = self.device_definition[Identifier.DEVICE_CLASS]
        self.device = device_class(self.device_uid, self.datalogger.ipcon)
        self.identifier = self.device_name #TODO change to number?

        self.__name__ = Identifier.DEVICES+":"+str(self.device_name)

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

        getter = self.device_definition[Identifier.DEVICE_VALUES][var_name][Identifier.DEVICE_DEFINITIONS_GETTER]
        subvalue_names = self.device_definition[Identifier.DEVICE_VALUES][var_name][Identifier.DEVICE_DEFINITIONS_SUBVALUES]
        timestamp = utils.CSVData._get_timestamp()

        try:
            value = getter(self.device)
        except Exception as e:
            value = self._exception_msg(str(self.identifier) + "-" + str(var_name), e)
            self.datalogger.add_to_queue(utils.CSVData(self.device_uid, self.identifier, var_name, value, timestamp))
            #log_exception(timestamp, value_name, e)
            return

        try:
            if subvalue_names == None:
                #log_value(value_name, value)
                self.datalogger.add_to_queue(utils.CSVData(self.device_uid, self.identifier, var_name, value, timestamp))
            else:
                subvalue_bool = self.data[Identifier.DEVICE_VALUES][var_name][Identifier.DEVICE_DEFINITIONS_SUBVALUES]
                for i in range(len(subvalue_names)):
                    if not isinstance(subvalue_names[i], list):
                        try:
                            if subvalue_bool[subvalue_names[i]]:
                                self.datalogger.add_to_queue(utils.CSVData(self.device_uid, self.identifier, str(var_name)+"-"+str(subvalue_names[i]), value[i], timestamp))
                        except Exception as e:
                            value = self._exception_msg(str(self.identifier) + "-" + str(var_name), e)
                            self.datalogger.add_to_queue(utils.CSVData(self.device_uid, self.identifier, str(var_name)+"-"+str(subvalue_names[i][k]), value[i][k], timestamp))
                            return
                    else:
                        for k in range(len(subvalue_names[i])):
                            try:
                                if subvalue_bool[subvalue_names[i][k]]:
                                    self.datalogger.add_to_queue(utils.CSVData(self.device_uid, self.identifier, str(var_name)+"-"+str(subvalue_names[i][k]), value[i][k], timestamp))
                            except Exception as e:
                                value = self._exception_msg(str(self.identifier) + "-" + str(var_name), e)
                                self.datalogger.add_to_queue(utils.CSVData(self.device_uid, self.identifier, str(var_name)+"-"+str(subvalue_names[i][k]), value[i][k], timestamp))
                                return
        except Exception as e:
            value = self._exception_msg(str(self.identifier) + "-" + str(var_name), e)
            self.datalogger.add_to_queue(utils.CSVData(self.device_uid, self.identifier, var_name, value, timestamp))


# ##Special Devices


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
