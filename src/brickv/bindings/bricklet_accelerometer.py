# -*- coding: utf-8 -*-
#############################################################
# This file was automatically generated on 2015-03-06.      #
#                                                           #
# Bindings Version 2.1.4                                    #
#                                                           #
# If you have a bugfix for this file and want to commit it, #
# please fix the bug in the generator. You can find a link  #
# to the generator git on tinkerforge.com                   #
#############################################################

#### __DEVICE_IS_NOT_RELEASED__ ####

try:
    from collections import namedtuple
except ImportError:
    try:
        from .ip_connection import namedtuple
    except ValueError:
        from ip_connection import namedtuple

try:
    from .ip_connection import Device, IPConnection, Error
except ValueError:
    from ip_connection import Device, IPConnection, Error

GetAcceleration = namedtuple('Acceleration', ['x', 'y', 'z'])
GetAccelerationCallbackThreshold = namedtuple('AccelerationCallbackThreshold', ['option', 'min_x', 'max_x', 'min_y', 'max_y', 'min_z', 'max_z'])
GetIdentity = namedtuple('Identity', ['uid', 'connected_uid', 'position', 'hardware_version', 'firmware_version', 'device_identifier'])

class BrickletAccelerometer(Device):
    """
    Device for sensing acceleration in three axis
    """

    DEVICE_IDENTIFIER = 250
    DEVICE_DISPLAY_NAME = 'Accelerometer Bricklet'

    CALLBACK_ACCELERATION = 9
    CALLBACK_ACCELERATION_REACHED = 10

    FUNCTION_GET_ACCELERATION = 1
    FUNCTION_SET_ACCELERATION_CALLBACK_PERIOD = 2
    FUNCTION_GET_ACCELERATION_CALLBACK_PERIOD = 3
    FUNCTION_SET_ACCELERATION_CALLBACK_THRESHOLD = 4
    FUNCTION_GET_ACCELERATION_CALLBACK_THRESHOLD = 5
    FUNCTION_SET_DEBOUNCE_PERIOD = 6
    FUNCTION_GET_DEBOUNCE_PERIOD = 7
    FUNCTION_GET_TEMPERATURE = 8
    FUNCTION_GET_IDENTITY = 255

    THRESHOLD_OPTION_OFF = 'x'
    THRESHOLD_OPTION_OUTSIDE = 'o'
    THRESHOLD_OPTION_INSIDE = 'i'
    THRESHOLD_OPTION_SMALLER = '<'
    THRESHOLD_OPTION_GREATER = '>'

    def __init__(self, uid, ipcon):
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        Device.__init__(self, uid, ipcon)

        self.api_version = (2, 0, 0)

        self.response_expected[BrickletAccelerometer.FUNCTION_GET_ACCELERATION] = BrickletAccelerometer.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletAccelerometer.FUNCTION_SET_ACCELERATION_CALLBACK_PERIOD] = BrickletAccelerometer.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletAccelerometer.FUNCTION_GET_ACCELERATION_CALLBACK_PERIOD] = BrickletAccelerometer.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletAccelerometer.FUNCTION_SET_ACCELERATION_CALLBACK_THRESHOLD] = BrickletAccelerometer.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletAccelerometer.FUNCTION_GET_ACCELERATION_CALLBACK_THRESHOLD] = BrickletAccelerometer.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletAccelerometer.FUNCTION_SET_DEBOUNCE_PERIOD] = BrickletAccelerometer.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletAccelerometer.FUNCTION_GET_DEBOUNCE_PERIOD] = BrickletAccelerometer.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletAccelerometer.FUNCTION_GET_TEMPERATURE] = BrickletAccelerometer.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletAccelerometer.CALLBACK_ACCELERATION] = BrickletAccelerometer.RESPONSE_EXPECTED_ALWAYS_FALSE
        self.response_expected[BrickletAccelerometer.CALLBACK_ACCELERATION_REACHED] = BrickletAccelerometer.RESPONSE_EXPECTED_ALWAYS_FALSE
        self.response_expected[BrickletAccelerometer.FUNCTION_GET_IDENTITY] = BrickletAccelerometer.RESPONSE_EXPECTED_ALWAYS_TRUE

        self.callback_formats[BrickletAccelerometer.CALLBACK_ACCELERATION] = 'h h h'
        self.callback_formats[BrickletAccelerometer.CALLBACK_ACCELERATION_REACHED] = 'h h h'

    def get_acceleration(self):
        """
        TODO
        
        If you want to get the acceleration periodically, it is recommended 
        to use the callback :func:`Acceleration` and set the period with 
        :func:`SetAccelerationCallbackPeriod`.
        """
        return GetAcceleration(*self.ipcon.send_request(self, BrickletAccelerometer.FUNCTION_GET_ACCELERATION, (), '', 'h h h'))

    def set_acceleration_callback_period(self, period):
        """
        Sets the period in ms with which the :func:`Acceleration` callback is triggered
        periodically. A value of 0 turns the callback off.
        
        :func:`Acceleration` is only triggered if the acceleration has changed since the
        last triggering.
        
        The default value is 0.
        """
        self.ipcon.send_request(self, BrickletAccelerometer.FUNCTION_SET_ACCELERATION_CALLBACK_PERIOD, (period,), 'I', '')

    def get_acceleration_callback_period(self):
        """
        Returns the period as set by :func:`SetAccelerationCallbackPeriod`.
        """
        return self.ipcon.send_request(self, BrickletAccelerometer.FUNCTION_GET_ACCELERATION_CALLBACK_PERIOD, (), '', 'I')

    def set_acceleration_callback_threshold(self, option, min_x, max_x, min_y, max_y, min_z, max_z):
        """
        Sets the thresholds for the :func:`AccelerationReached` callback. 
        
        The following options are possible:
        
        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100
        
         "'x'",    "Callback is turned off"
         "'o'",    "Callback is triggered when the temperature is *outside* the min and max values"
         "'i'",    "Callback is triggered when the temperature is *inside* the min and max values"
         "'<'",    "Callback is triggered when the temperature is smaller than the min value (max is ignored)"
         "'>'",    "Callback is triggered when the temperature is greater than the min value (max is ignored)"
        
        The default value is ('x', 0, 0, 0, 0, 0, 0).
        """
        self.ipcon.send_request(self, BrickletAccelerometer.FUNCTION_SET_ACCELERATION_CALLBACK_THRESHOLD, (option, min_x, max_x, min_y, max_y, min_z, max_z), 'c h h h h h h', '')

    def get_acceleration_callback_threshold(self):
        """
        Returns the threshold as set by :func:`SetAccelerationCallbackThreshold`.
        """
        return GetAccelerationCallbackThreshold(*self.ipcon.send_request(self, BrickletAccelerometer.FUNCTION_GET_ACCELERATION_CALLBACK_THRESHOLD, (), '', 'c h h h h h h'))

    def set_debounce_period(self, debounce):
        """
        Sets the period in ms with which the threshold callback
        
        * :func:`AccelerationReached`
        
        is triggered, if the threshold
        
        * :func:`SetAccelerationCallbackThreshold`
        
        keeps being reached.
        
        The default value is 100.
        """
        self.ipcon.send_request(self, BrickletAccelerometer.FUNCTION_SET_DEBOUNCE_PERIOD, (debounce,), 'I', '')

    def get_debounce_period(self):
        """
        Returns the debounce period as set by :func:`SetDebouncePeriod`.
        """
        return self.ipcon.send_request(self, BrickletAccelerometer.FUNCTION_GET_DEBOUNCE_PERIOD, (), '', 'I')

    def get_temperature(self):
        """
        Returns the temperature of the accelerometer in °C.
        """
        return self.ipcon.send_request(self, BrickletAccelerometer.FUNCTION_GET_TEMPERATURE, (), '', 'b')

    def get_identity(self):
        """
        Returns the UID, the UID where the Bricklet is connected to, 
        the position, the hardware and firmware version as well as the
        device identifier.
        
        The position can be 'a', 'b', 'c' or 'd'.
        
        The device identifier numbers can be found :ref:`here <device_identifier>`.
        |device_identifier_constant|
        """
        return GetIdentity(*self.ipcon.send_request(self, BrickletAccelerometer.FUNCTION_GET_IDENTITY, (), '', '8s 8s c 3B 3B H'))

    def register_callback(self, id, callback):
        """
        Registers a callback with ID *id* to the function *callback*.
        """
        self.registered_callbacks[id] = callback

Accelerometer = BrickletAccelerometer # for backward compatibility
