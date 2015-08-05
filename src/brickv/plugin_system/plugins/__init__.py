from brickv.plugin_system.plugins.ac_current import device_class as ac_current
from brickv.plugin_system.plugins.accelerometer import device_class as accelerometer
from brickv.plugin_system.plugins.ambient_light import device_class as ambient_light
from brickv.plugin_system.plugins.ambient_light_v2 import device_class as ambient_light_v2
from brickv.plugin_system.plugins.analog_in import device_class as analog_in
from brickv.plugin_system.plugins.analog_in_v2 import device_class as analog_in_v2
from brickv.plugin_system.plugins.analog_out import device_class as analog_out
from brickv.plugin_system.plugins.analog_out_v2 import device_class as analog_out_v2
from brickv.plugin_system.plugins.barometer import device_class as barometer
from brickv.plugin_system.plugins.co2 import device_class as co2
from brickv.plugin_system.plugins.color import device_class as color
from brickv.plugin_system.plugins.current12 import device_class as current12
from brickv.plugin_system.plugins.current25 import device_class as current25
from brickv.plugin_system.plugins.dc import device_class as dc
from brickv.plugin_system.plugins.distance_ir import device_class as distance_ir
from brickv.plugin_system.plugins.distance_us import device_class as distance_us
from brickv.plugin_system.plugins.dual_button import device_class as dual_button
from brickv.plugin_system.plugins.dual_relay import device_class as dual_relay
from brickv.plugin_system.plugins.dust_detector import device_class as dust_detector
from brickv.plugin_system.plugins.gas_detector import device_class as gas_detector
from brickv.plugin_system.plugins.gps import device_class as gps
from brickv.plugin_system.plugins.hall_effect import device_class as hall_effect
from brickv.plugin_system.plugins.heart_rate import device_class as heart_rate
from brickv.plugin_system.plugins.humidity import device_class as humidity
from brickv.plugin_system.plugins.imu import device_class as imu
from brickv.plugin_system.plugins.imu_v2 import device_class as imu_v2
from brickv.plugin_system.plugins.industrial_analog_out import device_class as industrial_analog_out
from brickv.plugin_system.plugins.industrial_digital_in_4 import device_class as industrial_digital_in_4
from brickv.plugin_system.plugins.industrial_digital_out_4 import device_class as industrial_digital_out_4
from brickv.plugin_system.plugins.industrial_dual_0_20ma import device_class as industrial_dual_0_20ma
from brickv.plugin_system.plugins.industrial_dual_analog_in import device_class as industrial_dual_analog_in
from brickv.plugin_system.plugins.industrial_quad_relay import device_class as industrial_quad_relay
from brickv.plugin_system.plugins.io16 import device_class as io16
from brickv.plugin_system.plugins.io4 import device_class as io4
from brickv.plugin_system.plugins.joystick import device_class as joystick
from brickv.plugin_system.plugins.laser_range_finder import device_class as laser_range_finder
from brickv.plugin_system.plugins.lcd_16x2 import device_class as lcd_16x2
from brickv.plugin_system.plugins.lcd_20x4 import device_class as lcd_20x4
from brickv.plugin_system.plugins.led_strip import device_class as led_strip
from brickv.plugin_system.plugins.line import device_class as line
from brickv.plugin_system.plugins.linear_poti import device_class as linear_poti
from brickv.plugin_system.plugins.load_cell import device_class as load_cell
from brickv.plugin_system.plugins.master import device_class as master
from brickv.plugin_system.plugins.moisture import device_class as moisture
from brickv.plugin_system.plugins.motion_detector import device_class as motion_detector
from brickv.plugin_system.plugins.multi_touch import device_class as multi_touch
from brickv.plugin_system.plugins.nfc_rfid import device_class as nfc_rfid
from brickv.plugin_system.plugins.oled_128x64 import device_class as oled_128x64
from brickv.plugin_system.plugins.oled_64x48 import device_class as oled_64x48
from brickv.plugin_system.plugins.ozone import device_class as ozone
from brickv.plugin_system.plugins.piezo_buzzer import device_class as piezo_buzzer
from brickv.plugin_system.plugins.piezo_speaker import device_class as piezo_speaker
from brickv.plugin_system.plugins.ptc import device_class as ptc
from brickv.plugin_system.plugins.red import device_class as red
from brickv.plugin_system.plugins.remote_switch import device_class as remote_switch
from brickv.plugin_system.plugins.rotary_encoder import device_class as rotary_encoder
from brickv.plugin_system.plugins.rotary_poti import device_class as rotary_poti
from brickv.plugin_system.plugins.rs232 import device_class as rs232
from brickv.plugin_system.plugins.segment_display_4x7 import device_class as segment_display_4x7
from brickv.plugin_system.plugins.servo import device_class as servo
from brickv.plugin_system.plugins.solid_state_relay import device_class as solid_state_relay
from brickv.plugin_system.plugins.sound_intensity import device_class as sound_intensity
from brickv.plugin_system.plugins.stepper import device_class as stepper
from brickv.plugin_system.plugins.temperature import device_class as temperature
from brickv.plugin_system.plugins.temperature_ir import device_class as temperature_ir
from brickv.plugin_system.plugins.tilt import device_class as tilt
from brickv.plugin_system.plugins.voltage import device_class as voltage
from brickv.plugin_system.plugins.voltage_current import device_class as voltage_current

device_classes = [
    ac_current,
    accelerometer,
    ambient_light,
    ambient_light_v2,
    analog_in,
    analog_in_v2,
    analog_out,
    analog_out_v2,
    barometer,
    co2,
    color,
    current12,
    current25,
    dc,
    distance_ir,
    distance_us,
    dual_button,
    dual_relay,
    dust_detector,
    gas_detector,
    gps,
    hall_effect,
    heart_rate,
    humidity,
    imu,
    imu_v2,
    industrial_analog_out,
    industrial_digital_in_4,
    industrial_digital_out_4,
    industrial_dual_0_20ma,
    industrial_dual_analog_in,
    industrial_quad_relay,
    io16,
    io4,
    joystick,
    laser_range_finder,
    lcd_16x2,
    lcd_20x4,
    led_strip,
    line,
    linear_poti,
    load_cell,
    master,
    moisture,
    motion_detector,
    multi_touch,
    nfc_rfid,
    oled_128x64,
    oled_64x48,
    ozone,
    piezo_buzzer,
    piezo_speaker,
    ptc,
    red,
    remote_switch,
    rotary_encoder,
    rotary_poti,
    rs232,
    segment_display_4x7,
    servo,
    solid_state_relay,
    sound_intensity,
    stepper,
    temperature,
    temperature_ir,
    tilt,
    voltage,
    voltage_current,
]
