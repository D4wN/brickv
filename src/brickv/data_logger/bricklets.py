from brickv.data_logger.utils import LoggerTimer   #Timer for getVariable
from brickv.data_logger.utils import DataLogger    #gloabl thread/job queue -> brickelts callbacks/timer
from brickv.data_logger.utils import CSVData       #bricklets

###Sections##############################################################
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

#ALL BRICKLETS + FUNCTIONS##################################################################
############################################################################################
#TODO: TEST Ambient Light
from tinkerforge.bricklet_ambient_light import AmbientLight
AMBIENT_LIGHT = "Ambient Light"
AMBIENT_LIGHT_ILLUMINANCE = "Illuminance"
AMBIENT_LIGHT_ANALOG_VALUE = "Analog Value"
class AmbientLightBricklet():
    """
    TODO:
        - exception handling value1,2 in timer_XXXXX
        - data[XXXXX] parse to int + excep handling
    """
    
    def __init__(self, uid):
        self.uid = uid        
        self._device = AmbientLight(self.uid, DataLogger.ipcon)


    def start_timer(self, data):
        print data
                
        value1 = DataLogger.parse_to_int(data[AMBIENT_LIGHT_ANALOG_VALUE])
        value2 = DataLogger.parse_to_int(data[AMBIENT_LIGHT_ILLUMINANCE])
        
        if value1 != 0:
            DataLogger.CB_COUNT += 1
            DataLogger.CB_SUM += value1            
        if value2 != 0:
            DataLogger.CB_COUNT += 1
            DataLogger.CB_SUM += value2        
        
        t = LoggerTimer(value1, self._timer_analog_value)
        LoggerTimer.Timers.append(t)         
        t = LoggerTimer(value2, self._timer_illuminance)
        LoggerTimer.Timers.append(t)

    def _timer_analog_value(self):
        value = "TMP-Error"
        try:
            value = self._device.get_analog_value()
        except:
            value = "Hallo Welt"
        
        csv = CSVData(self.uid, AMBIENT_LIGHT, AMBIENT_LIGHT_ANALOG_VALUE, value)
        DataLogger.Q.put(csv)
        
    def _timer_illuminance(self):
#         value = self._device.get_illuminance()
#         csv = CSVData(self.uid, AMBIENT_LIGHT, AMBIENT_LIGHT_ILLUMINANCE, value)
#         DataLogger.Q.put(csv)  
        pass

############################################################################################
#TODO: TEST Analog In                                
from tinkerforge.bricklet_analog_in import AnalogIn
ANALOG_IN = "Analog In"
ANALOG_IN_VOLTAGE = "Voltage"
ANALOG_IN_ANALOG_VALUE = "Analog Value"
class AnalogInBricklet():
    
    def __init__(self, uid):
        self.uid = uid        
        self._device = AnalogIn(self.uid, DataLogger.ipcon)


    def start_timer(self, data):        
        value1 = DataLogger.parse_to_int(data[ANALOG_IN_ANALOG_VALUE])
        value2 = DataLogger.parse_to_int(data[ANALOG_IN_VOLTAGE])
        
        if value1 != 0:
            DataLogger.CB_COUNT += 1
            DataLogger.CB_SUM += value1            
        if value2 != 0:
            DataLogger.CB_COUNT += 1
            DataLogger.CB_SUM += value2        
        
        t = LoggerTimer(value1, self._timer_analog_value)
        LoggerTimer.Timers.append(t)         
        t = LoggerTimer(value2, self._timer_voltage)
        LoggerTimer.Timers.append(t)

    def _timer_analog_value(self):
        value = self._device.get_analog_value()
        csv = CSVData(self.uid, ANALOG_IN, ANALOG_IN_ANALOG_VALUE, value)
        DataLogger.Q.put(csv)
        
    def _timer_voltage(self):
        value = self._device.get_voltage()
        csv = CSVData(self.uid, ANALOG_IN, ANALOG_IN_VOLTAGE, value)
        DataLogger.Q.put(csv)  

############################################################################################
#TODO: TEST Analog Out
from tinkerforge.bricklet_analog_out import AnalogOut
ANALOG_OUT = "Analog Out"
ANALOG_OUT_VOLTAGE = "Voltage"
class AnalogOutBricklet():
    
    def __init__(self, uid):
        self.uid = uid        
        self._device = AnalogOut(self.uid, DataLogger.ipcon)


    def start_timer(self, data):        
        value1 = DataLogger.parse_to_int(data[ANALOG_OUT_VOLTAGE])
        
        if value1 != 0:
            DataLogger.CB_COUNT += 1
            DataLogger.CB_SUM += value1         
        
        t = LoggerTimer(value1, self._timer_voltage()())
        LoggerTimer.Timers.append(t)         

    def _timer_voltage(self):
        value = self._device.get_voltage()
        csv = CSVData(self.uid, ANALOG_OUT, ANALOG_OUT_VOLTAGE, value)
        DataLogger.Q.put(csv)

############################################################################################
#Barometer
from tinkerforge.bricklet_barometer import Barometer
BAROMETER = "Barometer"
BAROMETER_AIR_PRESSURE = "Air Pressure"
BAROMETER_ALTITUDE = "Altitude"
class BarometerBricklet():
    
    def __init__(self, uid):
        self.uid = uid        
        self._device = Barometer(self.uid, DataLogger.ipcon)


    def start_timer(self, data):        
        value1 = DataLogger.parse_to_int(data[BAROMETER_AIR_PRESSURE])
        value2 = DataLogger.parse_to_int(data[BAROMETER_ALTITUDE])
        
        if value1 != 0:
            DataLogger.CB_COUNT += 1
            DataLogger.CB_SUM += value1            
        if value2 != 0:
            DataLogger.CB_COUNT += 1
            DataLogger.CB_SUM += value2        
        
        t = LoggerTimer(value1, self._timer_air_pressure)
        LoggerTimer.Timers.append(t)         
        t = LoggerTimer(value2, self._timer_altitude)
        LoggerTimer.Timers.append(t)

    def _timer_air_pressure(self):
        value = self._device.get_air_pressure()
        csv = CSVData(self.uid, BAROMETER, BAROMETER_AIR_PRESSURE, value)
        DataLogger.Q.put(csv)
        
    def _timer_altitude(self):
        value = self._device.get_altitude()
        csv = CSVData(self.uid, BAROMETER, BAROMETER_ALTITUDE, value)
        DataLogger.Q.put(csv)   

############################################################################################
#TODO: TEST Color
#TODO: Needs testing!!
from tinkerforge.bricklet_color import Color
COLOR = "Color"
COLOR_COLOR = "RGBC"
COLOR_RED = "Red"
COLOR_BLUE = "Blue"
COLOR_GREEN = "Green"
COLOR_CLEAR = "Clear"
COLOR_ILLUMINANCE = "ILLUMINANCE"
COLOR_TEMPERATUR = "Temperatur"
class ColorBricklet():
    
    def __init__(self, uid):
        self.uid = uid        
        self._device = Color(self.uid, DataLogger.ipcon)


    def start_timer(self, data):        
        value1 = DataLogger.parse_to_int(data[COLOR_COLOR])
        value2 = DataLogger.parse_to_int(data[COLOR_ILLUMINANCE])
        value3 = DataLogger.parse_to_int(data[COLOR_TEMPERATUR])
        
        if value1 != 0:
            DataLogger.CB_COUNT += 1
            DataLogger.CB_SUM += value1            
        if value2 != 0:
            DataLogger.CB_COUNT += 1
            DataLogger.CB_SUM += value2   
        if value3 != 0:
            DataLogger.CB_COUNT += 1
            DataLogger.CB_SUM += value3      
        
        t = LoggerTimer(value1, self._timer_color)
        LoggerTimer.Timers.append(t)         
        t = LoggerTimer(value2, self._timer_illuminance)
        LoggerTimer.Timers.append(t)
        t = LoggerTimer(value3, self._timer_color_temperature)
        LoggerTimer.Timers.append(t)

    def _timer_color(self):
        #TODO: TEST NEEDED !!!!!
        value = self._device.get_color()
        print "COLOR: TEST -> " +str(value)
#         csv = CSVData(self.uid, COLOR, COLOR, value)
#         DataLogger.Q.put(csv)
        
    def _timer_illuminance(self):
        value = self._device.get_illuminance()
        csv = CSVData(self.uid, COLOR, COLOR_ILLUMINANCE, value)
        DataLogger.Q.put(csv) 
        
    def _timer_color_temperature(self):
        value = self._device.get_color_temperature()
        csv = CSVData(self.uid, COLOR, COLOR_TEMPERATUR, value)
        DataLogger.Q.put(csv) 

############################################################################################
#TODO: TEST Current12
from tinkerforge.bricklet_current12 import Current12
CURRENT_12 = "Current 12"

class Current12Bricklet():
    
    def __init__(self, uid):
        self.uid = uid        
        self._device = Current12(self.uid, DataLogger.ipcon)


    def start_timer(self, data):
        print "UID(" + self.uid + ").start_timer"        

############################################################################################
#TODO: TEST Current25
from tinkerforge.bricklet_current25 import Current25
CURRENT_25 = "Current 25"

class Current25Bricklet():
    
    def __init__(self, uid):
        self.uid = uid        
        self._device = Current25(self.uid, DataLogger.ipcon)


    def start_timer(self, data):
        print "UID(" + self.uid + ").start_timer"   

############################################################################################
#TODO: TEST Distance IR
from tinkerforge.bricklet_distance_ir import DistanceIR
DISTANCE_IR = "Distance IR"

class DistanceIRBricklet():
    
    def __init__(self, uid):
        self.uid = uid        
        self._device = DistanceIR(self.uid, DataLogger.ipcon)


    def start_timer(self, data):
        print "UID(" + self.uid + ").start_timer"   

############################################################################################
#TODO: TEST Distance US
from tinkerforge.bricklet_distance_us import DistanceUS
DISTANCE_US = "Distance US"

class DistanceUSBricklet():
    
    def __init__(self, uid):
        self.uid = uid        
        self._device = DistanceUS(self.uid, DataLogger.ipcon)


    def start_timer(self, data):
        print "UID(" + self.uid + ").start_timer"   

############################################################################################
#TODO: TEST Dual Button
from tinkerforge.bricklet_dual_button import DualButton
DUAL_BUTTON = "Dual Button"
class DualButtonBricklet():
    
    def __init__(self, uid):
        self.uid = uid        
        self._device = DualButton(self.uid, DataLogger.ipcon)


    def start_timer(self, data):
        print "UID(" + self.uid + ").start_timer" 

############################################################################################
#TODO: TEST Dual Relay
from tinkerforge.bricklet_dual_relay import DualRelay
DUAL_RELAY = "Dual Relay"
class DualRelayBricklet():
    
    def __init__(self, uid):
        self.uid = uid        
        self._device = DualRelay(self.uid, DataLogger.ipcon)


    def start_timer(self, data):
        print "UID(" + self.uid + ").start_timer" 

############################################################################################
#TODO: TEST GPS
from tinkerforge.bricklet_gps import GPS
GPS_BRICKLET = "GPS"
class GPSBricklet():
    
    def __init__(self, uid):
        self.uid = uid        
        self._device = GPS(self.uid, DataLogger.ipcon)


    def start_timer(self, data):
        print "UID(" + self.uid + ").start_timer" 

############################################################################################
#TODO: TEST Hall Effect
from tinkerforge.bricklet_hall_effect import HallEffect
HALL_EFFECT = "Hall Effect"
class HallEffectBricklet():
    
    def __init__(self, uid):
        self.uid = uid        
        self._device = HallEffect(self.uid, DataLogger.ipcon)


    def start_timer(self, data):
        print "UID(" + self.uid + ").start_timer" 

############################################################################################
#TODO: TEST Humidity
from tinkerforge.bricklet_humidity import Humidity
HUMIDITY = "Humidity"
HUMIDITY_HUMIDITY = "Humidity"
HUMIDITY_ANALOG_VALUE = "Analog Value"
class HumidityBricklet():
    
    def __init__(self, uid):
        self.uid = uid        
        self._device = Humidity(self.uid, DataLogger.ipcon)


    def start_timer(self, data):        
        value1 = DataLogger.parse_to_int(data[HUMIDITY_ANALOG_VALUE])
        value2 = DataLogger.parse_to_int(data[HUMIDITY_HUMIDITY])
        
        if value1 != 0:
            DataLogger.CB_COUNT += 1
            DataLogger.CB_SUM += value1            
        if value2 != 0:
            DataLogger.CB_COUNT += 1
            DataLogger.CB_SUM += value2        
        
        t = LoggerTimer(value1, self._timer_analog_value)
        LoggerTimer.Timers.append(t)         
        t = LoggerTimer(value2, self._timer_humidity)
        LoggerTimer.Timers.append(t)

    def _timer_analog_value(self):
        value = self._device.get_analog_value()
        csv = CSVData(self.uid, HUMIDITY, HUMIDITY_ANALOG_VALUE, value)
        DataLogger.Q.put(csv)
        
    def _timer_humidity(self):
        value = self._device.get_humidity()
        csv = CSVData(self.uid, HUMIDITY, HUMIDITY_HUMIDITY, value)
        DataLogger.Q.put(csv)   

############################################################################################
#TODO: TEST Industrial Digital In 4
from tinkerforge.bricklet_industrial_digital_in_4 import IndustrialDigitalIn4
INDUSTRIAL_DIGITAL_IN_4 = "Industrial Digital In 4"
class IndustrialDigitalIn4Bricklet():
    
    def __init__(self, uid):
        self.uid = uid        
        self._device = IndustrialDigitalIn4(self.uid, DataLogger.ipcon)


    def start_timer(self, data):
        print "UID(" + self.uid + ").start_timer" 

############################################################################################
#TODO: TEST Industrial Digital Out 4
from tinkerforge.bricklet_industrial_digital_out_4 import IndustrialDigitalOut4
INDUSTRIAL_DIGITAL_OUT_4 = "Industrial Digital Out 4"
class IndustrialDigitalOut4Bricklet():
    
    def __init__(self, uid):
        self.uid = uid        
        self._device = IndustrialDigitalOut4(self.uid, DataLogger.ipcon)


    def start_timer(self, data):
        print "UID(" + self.uid + ").start_timer" 

############################################################################################
#TODO: TEST Industrial Dual 0-20mA
from tinkerforge.bricklet_industrial_dual_0_20ma import IndustrialDual020mA
INDUSTRIAL_DUAL_0_20_MA = "Industrial Dual 0 20 mA"
class IndustrialDual020mABricklet():
    
    def __init__(self, uid):
        self.uid = uid        
        self._device = IndustrialDual020mA(self.uid, DataLogger.ipcon)


    def start_timer(self, data):
        print "UID(" + self.uid + ").start_timer" 

############################################################################################
#TODO: TEST Industrial Quad Relay
from tinkerforge.bricklet_industrial_quad_relay import IndustrialQuadRelay
INDUSTRIAL_QUAD_RELAY = "Industrial Quad Relay"
class IndustrialQuadRelayBricklet():
    
    def __init__(self, uid):
        self.uid = uid        
        self._device = IndustrialQuadRelay(self.uid, DataLogger.ipcon)


    def start_timer(self, data):
        print "UID(" + self.uid + ").start_timer" 

############################################################################################
#TODO: TEST IO-16
from tinkerforge.bricklet_io16 import IO16
IO_16 = "IO-16"
class IO16Bricklet():
    
    def __init__(self, uid):
        self.uid = uid        
        self._device = IO16(self.uid, DataLogger.ipcon)


    def start_timer(self, data):
        print "UID(" + self.uid + ").start_timer" 

############################################################################################
#TODO: TEST IO-4
from tinkerforge.bricklet_io4 import IO4
IO_4 = "IO-4"
class IO4Bricklet():
    
    def __init__(self, uid):
        self.uid = uid        
        self._device = IO4(self.uid, DataLogger.ipcon)


    def start_timer(self, data):
        print "UID(" + self.uid + ").start_timer" 

############################################################################################
#TODO: TEST Joystick
from tinkerforge.bricklet_joystick import Joystick
JOYSTICK = "Joystick"
class JoystickBricklet():
    
    def __init__(self, uid):
        self.uid = uid        
        self._device = Joystick(self.uid, DataLogger.ipcon)


    def start_timer(self, data):
        print "UID(" + self.uid + ").start_timer" 

############################################################################################
#TODO: TEST LCD 16x2
from tinkerforge.bricklet_lcd_16x2 import LCD16x2
LCD_16x2 = "LCD 16x2"
class LCD16x2Bricklet():
    
    def __init__(self, uid):
        self.uid = uid        
        self._device = LCD16x2(self.uid, DataLogger.ipcon)


    def start_timer(self, data):
        print "UID(" + self.uid + ").start_timer" 

############################################################################################
#TODO: TEST LCD 20x4
from tinkerforge.bricklet_lcd_20x4 import LCD20x4
LCD_20x4 = "LCD 20x4"
class LCD20x4Bricklet():
    
    def __init__(self, uid):
        self.uid = uid        
        self._device = LCD20x4(self.uid, DataLogger.ipcon)


    def start_timer(self, data):
        print "UID(" + self.uid + ").start_timer" 

############################################################################################
#TODO: TEST LED Strip
from tinkerforge.bricklet_led_strip import LEDStrip
LED_STRIP = "LED Strip"
class LEDStripBricklet():
    
    def __init__(self, uid):
        self.uid = uid        
        self._device = LEDStrip(self.uid, DataLogger.ipcon)


    def start_timer(self, data):
        print "UID(" + self.uid + ").start_timer" 

############################################################################################
#TODO: TEST Line
from tinkerforge.bricklet_line import BrickletLine
LINE = "line"
class LineBricklet():
    
    def __init__(self, uid):
        self.uid = uid        
        self._device = BrickletLine(self.uid, DataLogger.ipcon)


    def start_timer(self, data):
        print "UID(" + self.uid + ").start_timer" 

############################################################################################
#TODO: TEST Linear Poti
from tinkerforge.bricklet_linear_poti import BrickletLinearPoti
LINEAR_POTI = "Linear Poti"
class LinearPotiBricklet():
    
    def __init__(self, uid):
        self.uid = uid        
        self._device = BrickletLinearPoti(self.uid, DataLogger.ipcon)


    def start_timer(self, data):
        print "UID(" + self.uid + ").start_timer" 

############################################################################################
#TODO: TEST Moisture
from tinkerforge.bricklet_moisture import Moisture
MOISTURE = "Moisture"
class MoistureBricklet():
    
    def __init__(self, uid):
        self.uid = uid        
        self._device = Moisture(self.uid, DataLogger.ipcon)


    def start_timer(self, data):
        print "UID(" + self.uid + ").start_timer" 

############################################################################################
#TODO: TEST Motion Detector
from tinkerforge.bricklet_motion_detector import MotionDetector
MOTION_DETECTOR = "Motion Detector"
class MotionDetectorBricklet():
    
    def __init__(self, uid):
        self.uid = uid        
        self._device = MotionDetector(self.uid, DataLogger.ipcon)


    def start_timer(self, data):
        print "UID(" + self.uid + ").start_timer" 

############################################################################################
#TODO: TEST Multi Touch
from tinkerforge.bricklet_multi_touch import MultiTouch
MULTI_TOUCH = "Multi Touch"
class MultiTouchBricklet():
    
    def __init__(self, uid):
        self.uid = uid        
        self._device = MultiTouch(self.uid, DataLogger.ipcon)


    def start_timer(self, data):
        print "UID(" + self.uid + ").start_timer" 

############################################################################################
#TODO: TEST NFC/RFID
from tinkerforge.bricklet_nfc_rfid import BrickletNFCRFID
NFC_RFID = "NFC RFID"
class NFCRFIDBricklet():
    
    def __init__(self, uid):
        self.uid = uid        
        self._device = BrickletNFCRFID(self.uid, DataLogger.ipcon)


    def start_timer(self, data):
        print "UID(" + self.uid + ").start_timer" 

############################################################################################
#TODO: TEST Piezo Buzzer
from tinkerforge.bricklet_piezo_buzzer import BrickletPiezoBuzzer
PIEZO_BUZZER = "Pirezo Buzzer"
class PiezoBuzzerBricklet():
    
    def __init__(self, uid):
        self.uid = uid        
        self._device = BrickletPiezoBuzzer(self.uid, DataLogger.ipcon)


    def start_timer(self, data):
        print "UID(" + self.uid + ").start_timer" 

############################################################################################
#TODO: TEST Piezo Speaker
from tinkerforge.bricklet_piezo_speaker import PiezoSpeaker
PIEZO_SPEAKER = "Piezo Speaker"
class PiezoSpeakerBricklet():
    
    def __init__(self, uid):
        self.uid = uid        
        self._device = PiezoSpeaker(self.uid, DataLogger.ipcon)


    def start_timer(self, data):
        print "UID(" + self.uid + ").start_timer" 

############################################################################################
#TODO: TEST PTC
from tinkerforge.bricklet_ptc import PTC
PTC_BRICKLET = "PTC"
class PTCBricklet():
    
    def __init__(self, uid):
        self.uid = uid        
        self._device = PTC(self.uid, DataLogger.ipcon)


    def start_timer(self, data):
        print "UID(" + self.uid + ").start_timer" 

############################################################################################
#TODO: TEST Remote Switch
from tinkerforge.bricklet_remote_switch import RemoteSwitch
REMOTE_SWITCH = "Remote Switch"
class RemoteSwitchBricklet():
    
    def __init__(self, uid):
        self.uid = uid        
        self._device = RemoteSwitch(self.uid, DataLogger.ipcon)


    def start_timer(self, data):
        print "UID(" + self.uid + ").start_timer" 

############################################################################################
#TODO: TEST Rotary Encoder
from tinkerforge.bricklet_rotary_encoder import RotaryEncoder
ROTARY_ENCODER = "Rotary Encoder"
class RotaryEncoderBricklet():
    
    def __init__(self, uid):
        self.uid = uid        
        self._device = RotaryEncoder(self.uid, DataLogger.ipcon)


    def start_timer(self, data):
        print "UID(" + self.uid + ").start_timer" 

############################################################################################
#TODO: TEST Rotary Poti
from tinkerforge.bricklet_rotary_poti import RotaryPoti
ROTARY_POTI = "Rotary Poti"
class RotaryPotiBricklet():
    
    def __init__(self, uid):
        self.uid = uid        
        self._device = RotaryPoti(self.uid, DataLogger.ipcon)


    def start_timer(self, data):
        print "UID(" + self.uid + ").start_timer" 

############################################################################################
#TODO: TEST Segment Display 4x7
from tinkerforge.bricklet_segment_display_4x7 import BrickletSegmentDisplay4x7 
SEGMENT_DISPLAY_4x7 = "Segment Display 4x7"
class SegmentDisplay4x7Bricklet():
    
    def __init__(self, uid):
        self.uid = uid        
        self._device = BrickletSegmentDisplay4x7(self.uid, DataLogger.ipcon)


    def start_timer(self, data):
        print "UID(" + self.uid + ").start_timer" 

############################################################################################
#TODO: TEST Solid State Relay
from tinkerforge.bricklet_solid_state_relay import BrickletSolidStateRelay
SOLID_STATE_RELAY = "Solid State Relay"
class SolidStateRelayBricklet():
    
    def __init__(self, uid):
        self.uid = uid        
        self._device = BrickletSolidStateRelay(self.uid, DataLogger.ipcon)


    def start_timer(self, data):
        print "UID(" + self.uid + ").start_timer" 

############################################################################################
#TODO: TEST Sound Intensity
from tinkerforge.bricklet_sound_intensity import BrickletSoundIntensity
SOUND_INTENSITY = "Sound Intensity"
class SoundIntensityBricklet():
    
    def __init__(self, uid):
        self.uid = uid        
        self._device = BrickletSoundIntensity(self.uid, DataLogger.ipcon)


    def start_timer(self, data):
        print "UID(" + self.uid + ").start_timer" 

############################################################################################
#TODO: TEST Temperature
from tinkerforge.bricklet_temperature import BrickletTemperature
TEMPERATURE = "Temperature"
class TemperatureBricklet():
    
    def __init__(self, uid):
        self.uid = uid        
        self._device = BrickletTemperature(self.uid, DataLogger.ipcon)


    def start_timer(self, data):
        print "UID(" + self.uid + ").start_timer" 

############################################################################################
#TODO: Temperature IR
from tinkerforge.bricklet_temperature_ir import BrickletTemperatureIR
TEMPERATURE_IR = "Temperature IR"
class TemperatureIRBricklet():
    
    def __init__(self, uid):
        self.uid = uid        
        self._device = BrickletTemperatureIR(self.uid, DataLogger.ipcon)


    def start_timer(self, data):
        print "UID(" + self.uid + ").start_timer" 

############################################################################################
#TODO: TEST Tilt
from tinkerforge.bricklet_tilt import BrickletTilt
TILT = "Tilt"
class TiltBricklet():
    
    def __init__(self, uid):
        self.uid = uid        
        self._device = BrickletTilt(self.uid, DataLogger.ipcon)


    def start_timer(self, data):
        print "UID(" + self.uid + ").start_timer" 

############################################################################################
#TODO: TEST Voltage
from tinkerforge.bricklet_voltage import BrickletVoltage
VOLTAGE = "Voltage"
class VoltageBricklet():
    
    def __init__(self, uid):
        self.uid = uid        
        self._device = BrickletVoltage(self.uid, DataLogger.ipcon)


    def start_timer(self, data):
        print "UID(" + self.uid + ").start_timer" 

############################################################################################
#TODO: TEST Voltage/Current
from tinkerforge.bricklet_voltage_current import BrickletVoltageCurrent
VOLTAGE_CURRENT = "Voltage Current"
class VoltageCurrentBricklet():
    
    def __init__(self, uid):
        self.uid = uid        
        self._device = BrickletVoltageCurrent(self.uid, DataLogger.ipcon)


    def start_timer(self, data):
        print "UID(" + self.uid + ").start_timer" 
