import collections
import json

from brickv.data_logger.event_logger import EventLogger, GUILogger
from brickv.data_logger.loggable_devices import Identifier

'''
/*---------------------------------------------------------------------------
                                GuiConfigHandler
 ---------------------------------------------------------------------------*/
 '''
class GuiConfigHandler(object):
    """
        This static class is used to convert a config into a blueprint for the gui and vice versa.
        It also holds a blueprint with all supported diveces. If a new device should be supported,
        this string should be updatetd, too.
    """

    device_blueprint = []
    #blueprint for all supported devices
    all_devices_blueprint = "[{\"Ambient Light\": {\"Analog Value\": {\"_interval\": 0}, \"Illuminance\": {\"_interval\": 0}}, \"Analog In\": {\"Analog Value\": {\"_interval\": 0}, \"Voltage\": {\"_interval\": 0}}, \"Analog Out\": {\"Voltage\": {\"_interval\": 0}}, \"Barometer\": {\"Air Pressure\": {\"_interval\": 0}, \"Altitude\": {\"_interval\": 0}, \"Chip Temperature\": {\"_interval\": 0}}, \"Color\": {\"Color Temperature\": {\"Color Temperature\": true, \"_interval\": 0}, \"Illuminance\": {\"Illuminance\": true, \"_interval\": 0}, \"Rgbc\": {\"b\": true, \"c\": true, \"g\": true, \"r\": true, \"_interval\": 0}}, \"Current 12\": {\"Analog Value\": {\"_interval\": 0}, \"Current\": {\"_interval\": 0}}, \"Current 25\": {\"Analog Value\": {\"_interval\": 0}, \"Current\": {\"_interval\": 0}}, \"DC Brick\": {\"Acceleration\": {\"_interval\": 0}, \"Chip Temperature\": {\"_interval\": 0}, \"Current Consumption\": {\"_interval\": 0}, \"Current Velocity\": {\"_interval\": 0}, \"External Input Voltage\": {\"_interval\": 0}, \"Stack Input Voltage\": {\"_interval\": 0}, \"Velocity\": {\"_interval\": 0}}, \"Distance IR\": {\"Analog Value\": {\"_interval\": 0}, \"Distance\": {\"_interval\": 0}}, \"Distance US\": {\"Distance\": {\"_interval\": 0}}, \"Dual Button\": {\"Buttons\": {\"button_l\": true, \"button_r\": true, \"_interval\": 0}, \"Leds\": {\"led_l\": true, \"led_r\": true, \"_interval\": 0}}, \"Dual Relay\": {\"State\": {\"relay1\": true, \"relay2\": true, \"_interval\": 0}}, \"GPS\": {\"special_bool\": {\"Altitude Value\": true, \"Course\": true, \"Date\": true, \"Epe\": true, \"Ew\": true, \"Fix Status\": true, \"Geoidal Seperation\": true, \"Hdop\": true, \"Latitude\": true, \"Longitude\": true, \"Ns\": true, \"Pdop\": true, \"Satellites Used\": true, \"Satellites View\": true, \"Speed\": true, \"Time\": true, \"Vdop\": true}, \"special_values\": {\"Altitude\": 0, \"Coordinates\": 0, \"Date Time\": 0, \"Motion\": 0}}, \"Hall Effect\": {\"Value\": {\"_interval\": 0}}, \"Humidity\": {\"Analog Value\": {\"_interval\": 0}, \"Humidity\": {\"_interval\": 0}}, \"IO-16\": {\"Port A\": {\"_interval\": 0}, \"Port B\": {\"_interval\": 0}}, \"IO-4\": {\"Value\": {\"_interval\": 0}}, \"Industrial Dual 0 20 mA\": {\"Sensor 0\": {\"_interval\": 0}, \"Sensor 1\": {\"_interval\": 0}}, \"Joystick\": {\"Analog Value\": {\"x\": true, \"y\": true, \"_interval\": 0}, \"Position\": {\"x\": true, \"y\": true, \"_interval\": 0}, \"Pressed\": {\"Pressed\": true, \"_interval\": 0}}, \"LED Strip\": {\"Supply Voltage\": {\"_interval\": 0}}, \"Line\": {\"Reflectivity\": {\"_interval\": 0}}, \"Linear Poti\": {\"Analog Value\": {\"_interval\": 0}, \"Position\": {\"_interval\": 0}}, \"Moisture\": {\"Moisture Value\": {\"_interval\": 0}}, \"Motion Detector\": {\"Motion Detected\": {\"_interval\": 0}}, \"Multi Touch\": {\"Touch State\": {\"_interval\": 0}}, \"PTC\": {\"Resistance\": {\"_interval\": 0}, \"Temperature\": {\"_interval\": 0}}, \"Rotary Encoder\": {\"Count\": {\"_interval\": 0}, \"Pressed\": {\"_interval\": 0}}, \"Rotary Poti\": {\"Analog Value\": {\"_interval\": 0}, \"Position\": {\"_interval\": 0}}, \"Segment Display 4x7\": {\"special_bool\": {\"Brightness\": true, \"Colon\": true, \"Segment 1\": true, \"Segment 2\": true, \"Segment 3\": true, \"Segment 4\": true}, \"special_values\": {\"Counter Value\": 0, \"Segments\": 0}}, \"Solid State Relay\": {\"State\": {\"_interval\": 0}}, \"Sound Intensity\": {\"Intensity\": {\"_interval\": 0}}, \"Stepper Brick\": {\"Current Consumption\": {\"_interval\": 0}, \"Current Position\": {\"_interval\": 0}, \"Current Velocity\": {\"_interval\": 0}, \"External Input Voltage\": {\"_interval\": 0}, \"Remaining Steps\": {\"_interval\": 0}, \"Stack Input Voltage\": {\"_interval\": 0}, \"Steps\": {\"_interval\": 0}, \"Sync Rect\": {\"_interval\": 0}}, \"Temperature\": {\"Temperature\": {\"_interval\": 0}}, \"Temperature IR\": {\"Ambient Temperature\": {\"_interval\": 0}, \"Object Temperature\": {\"_interval\": 0}}, \"Tilt\": {\"State\": {\"_interval\": 0}}, \"Voltage\": {\"Analog Value\": {\"_interval\": 0}, \"Voltage\": {\"_interval\": 0}}, \"Voltage Current\": {\"Current\": {\"_interval\": 0}, \"Power\": {\"_interval\": 0}, \"Voltage\": {\"_interval\": 0}}}]"


    def load_devices(device_json):
        """
        Loads the config as json and converts all devices into the blueprint part.
        Returns the blueprint of the devices.
        """



        try:
            GuiConfigHandler.clear_blueprint()
            #TODO new blueprints from DEVICE


            GuiConfigHandler.create_device_blueprint(device_json[Identifier.DEVICES])
            #GuiConfigHandler.device_blueprint.append(tmp)


            #GuiConfigHandler.simple_device_blueprints(device_json[Identifier.SIMPLE_DEVICE])
            #GuiConfigHandler.complex_device_blueprints(device_json[Identifier.COMPLEX_DEVICE])
            #GuiConfigHandler.special_device_blueprints(device_json[Identifier.SPECIAL_DEVICE])
            
        except Exception as e:
            EventLogger.warning("Devices could not be fully loaded! -> " + str(e))
        
        return GuiConfigHandler.device_blueprint

    def clear_blueprint(fixme=None): #FIXME error without parameter?!
        """
        Resets the current blueprints save in device_blueprint.
        """
        GuiConfigHandler.device_blueprint = None
        GuiConfigHandler.device_blueprint = []

    def create_device_blueprint(devices):
        import copy
        EventLogger.debug("DEVICES:\n" + str(devices))



        for dev in devices:
            bp_dev = None #Blueprint Device

            #check for blueprint KEY(DEVICE_DEFINITIONS)
            if Identifier.DEVICE_DEFINITIONS.has_key(dev[Identifier.DEVICE_NAME]):
                bp_dev = copy.deepcopy(Identifier.DEVICE_DEFINITIONS[dev[Identifier.DEVICE_NAME]])
                #remove unused entries(class)
                del bp_dev[Identifier.DEVICE_CLASS]

                #add new entries(name, uid)
                bp_dev[Identifier.DEVICE_NAME] = dev[Identifier.DEVICE_NAME]
                bp_dev[Identifier.DEVICE_UID] = dev[Identifier.DEVICE_UID]

                #add/remove entries for values
                for val in bp_dev[Identifier.DEVICE_VALUES]:

                    #remove getter
                    del bp_dev[Identifier.DEVICE_VALUES][val][Identifier.DEVICE_DEFINITIONS_GETTER]

                    #add interval, check if exists
                    if val in bp_dev[Identifier.DEVICE_VALUES]:
                        #check for NO device values
                        if not val in dev[Identifier.DEVICE_VALUES]:
                            #create necessary structures for the checks
                            dev[Identifier.DEVICE_VALUES][val] = {}
                            dev[Identifier.DEVICE_VALUES][val][Identifier.DEVICE_DEFINITIONS_SUBVALUES] = {}

                        if Identifier.DEVICE_VALUES_INTERVAL in dev[Identifier.DEVICE_VALUES][val]:
                            bp_dev[Identifier.DEVICE_VALUES][val][Identifier.DEVICE_VALUES_INTERVAL] = dev[Identifier.DEVICE_VALUES][val][Identifier.DEVICE_VALUES_INTERVAL]
                        else:
                            bp_dev[Identifier.DEVICE_VALUES][val][Identifier.DEVICE_VALUES_INTERVAL] = 0

                        #subvalues

                        if bp_dev[Identifier.DEVICE_VALUES][val][Identifier.DEVICE_DEFINITIONS_SUBVALUES] is not None:
                            bp_sub_values = bp_dev[Identifier.DEVICE_VALUES][val][Identifier.DEVICE_DEFINITIONS_SUBVALUES]

                            #delete subvalues old entries
                            bp_dev[Identifier.DEVICE_VALUES][val][Identifier.DEVICE_DEFINITIONS_SUBVALUES] = {}

                            for i in range(0, len(bp_sub_values)):
                                #check sub_val for bool
                                sub_val = bp_sub_values[i]

                                #check if list in list #FIXME multi layer? sub_sub_sub_....
                                if type(sub_val) == list:
                                    for j in range(0, len(sub_val)):
                                        sub_sub_val = sub_val[j]

                                        if sub_sub_val in dev[Identifier.DEVICE_VALUES][val][Identifier.DEVICE_DEFINITIONS_SUBVALUES]:
                                            bp_dev[Identifier.DEVICE_VALUES][val][Identifier.DEVICE_DEFINITIONS_SUBVALUES][sub_sub_val] = dev[Identifier.DEVICE_VALUES][val][Identifier.DEVICE_DEFINITIONS_SUBVALUES][sub_sub_val]
                                        else:
                                            bp_dev[Identifier.DEVICE_VALUES][val][Identifier.DEVICE_DEFINITIONS_SUBVALUES][sub_sub_val] = False
                                    continue

                                if sub_val in dev[Identifier.DEVICE_VALUES][val][Identifier.DEVICE_DEFINITIONS_SUBVALUES]:
                                    bp_dev[Identifier.DEVICE_VALUES][val][Identifier.DEVICE_DEFINITIONS_SUBVALUES][sub_val] = dev[Identifier.DEVICE_VALUES][val][Identifier.DEVICE_DEFINITIONS_SUBVALUES][sub_val]
                                else:
                                    bp_dev[Identifier.DEVICE_VALUES][val][Identifier.DEVICE_DEFINITIONS_SUBVALUES][sub_val] = False

                        else:
                            del bp_dev[Identifier.DEVICE_VALUES][val][Identifier.DEVICE_DEFINITIONS_SUBVALUES]

                    else:
                        bp_dev[Identifier.DEVICE_VALUES][val][Identifier.DEVICE_VALUES_INTERVAL] = 0 # Default Value for Interval




                    #else: #ignore subvals



                EventLogger.debug(str(bp_dev))
                print str(bp_dev)

            else:
                EventLogger.warning("No Device Definition found in Config for Device Name: " +str(dev[Identifier.DEVICE_NAME]) + "! Device will be ignored!")




        #GuiConfigHandler.device_blueprint.append(tmp)

    def create_config_file(Ui_Logger):
        """
        Creates a config file. Converst all devices from the tree_widget and
        fetches the GENERAL_SECTION information.
        Returns the config as dictonary.
        """
        config_root = {}
        # add general section
        general_section = GuiConfigHandler.create_general_section(Ui_Logger)
        # TODO: add xively
        xively_section = {}
        
        # add simple devices
        simple_dev = []
        # add complex devices
        complex_dev = []
        # add special devices
        special_dev = []
        
                
        tree_widget = Ui_Logger.tree_devices
            
        r0_max = tree_widget.topLevelItemCount()
        
        for r0 in range(0, r0_max):
            device_type = 0
            tw_root = tree_widget.topLevelItem(r0)
            # create object structure
            dev = {}
            dev[Identifier.DEVICE_NAME] = str(tw_root.text(0))
            dev[Identifier.DEVICE_CLASS] = Identifier.create_class_name(dev[Identifier.DEVICE_NAME])
            tmp_uid = str(tw_root.text(1))
            if tmp_uid == "" or tmp_uid is None:
                dev[Identifier.DEVICE_UID] = "TODO"
            else:
                dev[Identifier.DEVICE_UID] = tmp_uid
            
            r1_max = tw_root.childCount()
            
            # check for special device type
            tmp_sepcial = str(tw_root.child(0).text(0))
                
            if (tmp_sepcial == Identifier.SPECIAL_DEVICE_BOOL or tmp_sepcial == Identifier.SPECIAL_DEVICE_VALUE):
                # is special device!

                device_type = 2
                dev[Identifier.SPECIAL_DEVICE_BOOL] = {}
                dev[Identifier.SPECIAL_DEVICE_VALUE] = {}
                
                for r1 in range(0, r1_max):
                    tw_r1 = tw_root.child(r1)
                    var_name = str(tw_r1.text(0))
                    
                    r2_max = tw_r1.childCount()
                    for r2 in range(0, r2_max):
                        tw_r2 = tw_r1.child(r2)
                        var_key = str(tw_r2.text(0))
                        
                        # speicla_bool or special_value
                        if var_name == Identifier.SPECIAL_DEVICE_BOOL:
                            check_state_num = tw_r2.checkState(1)
                            if check_state_num == 0:
                                dev[Identifier.SPECIAL_DEVICE_BOOL][var_key] = False
                            else:
                                dev[Identifier.SPECIAL_DEVICE_BOOL][var_key] = True
    
                        else:
                            dev[Identifier.SPECIAL_DEVICE_VALUE][var_key] = int(str(tw_r2.text(1)))
    
            else:
                # is complex or Simple
                dev[Identifier.DEVICE_VALUES] = {}
                
                for r1 in range(0, r1_max):
                    tw_r1 = tw_root.child(r1)
                    var_name = str(tw_r1.text(0))
                    
                    dev[Identifier.DEVICE_VALUES][var_name] = {}
                    dev[Identifier.DEVICE_VALUES][var_name][Identifier.DEVICE_VALUES_ARGS] = Identifier.create_args(dev[Identifier.DEVICE_NAME], var_name)
                    dev[Identifier.DEVICE_VALUES][var_name][Identifier.DEVICE_VALUES_NAME] = Identifier.create_function_name(dev[Identifier.DEVICE_NAME], var_name)
                    
                    r2_max = tw_r1.childCount()
                    if r2_max != 1:
                        # complex device
                        device_type = 1
                        dev[Identifier.DEVICE_VALUES][var_name][Identifier.COMPLEX_DEVICE_VALUES_BOOL] = []
                        dev[Identifier.DEVICE_VALUES][var_name][Identifier.COMPLEX_DEVICE_VALUES_NAME] = []
                    
                    for r2 in range(0, r2_max):
                        tw_r2 = tw_r1.child(r2)
                        var_key = str(tw_r2.text(0))
                        if var_key == Identifier.DEVICE_VALUES_INTERVAL:
                            dev[Identifier.DEVICE_VALUES][var_name][var_key] = int(str(tw_r2.text(1)))
                        
                        else:
                            dev[Identifier.DEVICE_VALUES][var_name][Identifier.COMPLEX_DEVICE_VALUES_NAME].append(var_key)
                            check_state_num = tw_r2.checkState(1)
                        
                            if check_state_num == 0:
                                dev[Identifier.DEVICE_VALUES][var_name][Identifier.COMPLEX_DEVICE_VALUES_BOOL].append(False)
                            else:
                                dev[Identifier.DEVICE_VALUES][var_name][Identifier.COMPLEX_DEVICE_VALUES_BOOL].append(True)
            
            
            # save dev in the right device!
            if device_type == 0:
                simple_dev.append(dev)
            elif device_type == 1:
                complex_dev.append(dev)
            elif device_type == 2:
                special_dev.append(dev)
            else:
                EventLogger.debug("gui_config_handler: Unknown device?!: " + str(device_type))
        
        from brickv.data_logger.configuration_validator import ConfigurationReader
        
        config_root[ConfigurationReader.GENERAL_SECTION] = general_section
        config_root[ConfigurationReader.XIVELY_SECTION] = xively_section
        config_root[Identifier.SIMPLE_DEVICE] = simple_dev
        config_root[Identifier.COMPLEX_DEVICE] = complex_dev
        config_root[Identifier.SPECIAL_DEVICE] = special_dev
        
        return config_root

    def create_general_section(Ui_Logger):
        """
        Creates the GENERAL_SECTION part of the config file 
        and returns it as a dictonary.
        """
        from brickv.data_logger.configuration_validator import ConfigurationReader
        
        general_section = {}
        
        # host            combo_host              currentText()   : QString
        general_section[ConfigurationReader.GENERAL_HOST] = str(Ui_Logger.combo_host.currentText())
        # port            spinbox_port            value()         : int
        general_section[ConfigurationReader.GENERAL_PORT] = Ui_Logger.spinbox_port.value()
        # file_count      spin_file_count         value()         : int
        general_section[ConfigurationReader.GENERAL_LOG_COUNT] = Ui_Logger.spin_file_count.value()
        # file_size       spin_file_size          value()         : int * 1024 * 1024! (MB -> Byte)
        general_section[ConfigurationReader.GENERAL_LOG_FILE_SIZE] = (Ui_Logger.spin_file_size.value() * 1024 * 1024)
        # path_to_file    line_path_to_file       text()          : QString
        path_to_file = str(Ui_Logger.line_path_to_file.text())
        log_to_file = True
        if path_to_file is None or path_to_file == "":
            log_to_file = False
        # log_to_file     (if path_to_file != None || "")
        general_section[ConfigurationReader.GENERAL_PATH_TO_FILE] = path_to_file
        general_section[ConfigurationReader.GENERAL_LOG_TO_FILE] = log_to_file

        #logfile path
        general_section[ConfigurationReader.GENERAL_EVENTLOG_PATH] = str(Ui_Logger.line_path_to_eventfile.text())
        #loglevel
        ll = Ui_Logger.combo_loglevel.currentText()
        log_level_num = 0
        od = collections.OrderedDict(sorted(GUILogger._convert_level.items()))
        for k in od.keys():
            if ll == od[k]:
                log_level_num = k
                break;
        general_section[ConfigurationReader.GENERAL_EVENTLOG_LEVEL] = log_level_num
        #log_to_console
        general_section[ConfigurationReader.GENERAL_EVENTLOG_TO_FILE] = Ui_Logger.checkbox_to_file.isChecked()
        #log_to_file
        general_section[ConfigurationReader.GENERAL_EVENTLOG_TO_CONSOLE] = Ui_Logger.checkbox_to_console.isChecked()

        return general_section

    def get_simple_blueprint(Ui_Logger):
        """
        Returns a very simple bluepirnt version of the current 
        devices in the tree_widget. Is used for the DeviceDialog.
        This blueprint only contains the name and uid of a device.
        """
        simple_blueprint = []
        
        tree_widget = Ui_Logger.tree_devices
            
        r0_max = tree_widget.topLevelItemCount()
        
        for r0 in range(0, r0_max):
            item = {}
            
            tw_root = tree_widget.topLevelItem(r0)
            item[str(tw_root.text(0))] = str(tw_root.text(1))
            
            simple_blueprint.append(item)
        
        return simple_blueprint

    def get_single_device_bluprint(device_name):
        """
        Returns a singel blueprint for a given device_name.
        Used to add a device from the DeviceDialog.
        """
        dev = None
        
        blueprint = json.loads(GuiConfigHandler.all_devices_blueprint)
        
        found = False
        for device_item in blueprint:
            for i in device_item:
                if device_name == i:
                    dev = {}
                    dev[i] = device_item[i]
                    found = True
                    break
                
            if found:
                break
        
        return dev

    load_devices = staticmethod(load_devices)
    clear_blueprint = staticmethod(clear_blueprint)
    create_device_blueprint = staticmethod(create_device_blueprint)
    create_config_file = staticmethod(create_config_file)
    create_general_section = staticmethod(create_general_section)
    get_simple_blueprint = staticmethod(get_simple_blueprint)
    get_single_device_bluprint = staticmethod(get_single_device_bluprint)

    
