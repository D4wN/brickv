from brickv.data_logger.loggable_devices import Identifier
from brickv.data_logger.event_logger import EventLogger

class GuiConfigHandler(object):

    device_blueprint = {}
    
    def load_devices(device_json):
        GuiConfigHandler.clear_blueprint()
        GuiConfigHandler.simple_device_blueprints(device_json[Identifier.SIMPLE_DEVICE])
        GuiConfigHandler.complex_device_blueprints(device_json[Identifier.COMPLEX_DEVICE])
        GuiConfigHandler.special_device_blueprints(device_json[Identifier.SPECIAL_DEVICE])
        
        return GuiConfigHandler.device_blueprint
    
    def clear_blueprint():
        GuiConfigHandler.device_blueprint = None
        GuiConfigHandler.device_blueprint = {}
    
    def complex_device_blueprints(complex_devices):
        #CLASS_NAME=dev[Identifier.DEVICE_NAME]   
        for dev in complex_devices:
            tmp = {} #empty list
            dev_name = dev[Identifier.DEVICE_NAME]   
            #t1
            tmp = {}
            
            for var in dev[Identifier.DEVICE_VALUES]:
                interval = dev[Identifier.DEVICE_VALUES][var][Identifier.DEVICE_VALUES_INTERVAL]
                vars = dev[Identifier.DEVICE_VALUES][var][Identifier.COMPLEX_DEVICE_VALUES_NAME]
                bools = dev[Identifier.DEVICE_VALUES][var][Identifier.COMPLEX_DEVICE_VALUES_BOOL] 
                                
                tmp[var] = {}
                tmp[var]["_"+Identifier.DEVICE_VALUES_INTERVAL] = interval      
                 
                for v in range(0,len(vars)):
                    tmp[var][vars[v]] = bools[v]
                
            #add UID
            tmp[Identifier.DEVICE_UID] = dev[Identifier.DEVICE_UID]

            GuiConfigHandler.device_blueprint[dev_name] = tmp  
    
    def simple_device_blueprints(simple_devices):
        for dev in simple_devices:
            dev_name = dev[Identifier.DEVICE_NAME]   
            #t1
            tmp = {}
            
            for var in dev[Identifier.DEVICE_VALUES]:
                interval = dev[Identifier.DEVICE_VALUES][var][Identifier.DEVICE_VALUES_INTERVAL]
                
                tmp[var] = {}
                tmp[var]["_"+Identifier.DEVICE_VALUES_INTERVAL] = interval  
                
            #add UID
            tmp[Identifier.DEVICE_UID] = dev[Identifier.DEVICE_UID]
            GuiConfigHandler.device_blueprint[dev_name] = tmp

    def special_device_blueprints(special_devices):
        for dev in special_devices:
            dev_name = dev[Identifier.DEVICE_NAME]   
            #t1
            tmp = {}
            tmp[Identifier.SPECIAL_DEVICE_BOOL] = {}
            tmp[Identifier.SPECIAL_DEVICE_VALUE] = {}
            
            for var in dev[Identifier.SPECIAL_DEVICE_BOOL]:
                tmp[Identifier.SPECIAL_DEVICE_BOOL][var] = dev[Identifier.SPECIAL_DEVICE_BOOL][var]
             
            for var in dev[Identifier.SPECIAL_DEVICE_VALUE]:
                tmp[Identifier.SPECIAL_DEVICE_VALUE][var] = dev[Identifier.SPECIAL_DEVICE_VALUE][var]
              
            #add UID
            tmp[Identifier.DEVICE_UID] = dev[Identifier.DEVICE_UID]
            
            GuiConfigHandler.device_blueprint[dev_name] = tmp

    def create_config_file(tree_widget):
        config_root = {}
        #TODO: add general section
        general_section = {}
        #TODO: add xively
        
        #add simple devices
        simple_dev = []
        #add complex devices
        complex_dev = []
        #add special devices
        special_dev = []
        
                
        r0_max =  tree_widget.topLevelItemCount()    
        
        for r0 in range(0, r0_max):
            device_type = 0
            tw_root = tree_widget.topLevelItem(r0)
            #create object structure
            dev = {}
            dev[Identifier.DEVICE_NAME] = str(tw_root.text(0))
            dev[Identifier.DEVICE_CLASS] = Identifier.create_class_name(dev[Identifier.DEVICE_NAME])
            tmp_uid = str(tw_root.text(1))
            if tmp_uid == "" or tmp_uid == None:
                dev[Identifier.DEVICE_UID] = "TODO"
            else:
                dev[Identifier.DEVICE_UID] = tmp_uid            
            
            r1_max = tw_root.childCount()
            
            #check for special device type
            tmp_sepcial = str(tw_root.child(0).text(0))
                
            if (tmp_sepcial == Identifier.SPECIAL_DEVICE_BOOL or tmp_sepcial == Identifier.SPECIAL_DEVICE_VALUE):
                #is special device!

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
                        
                        #speicla_bool or special_value
                        if var_name == Identifier.SPECIAL_DEVICE_BOOL:
                            check_state_num = tw_r2.checkState(1)                        
                            if check_state_num == 0:
                                dev[Identifier.SPECIAL_DEVICE_BOOL][var_key] = False
                            else:
                                dev[Identifier.SPECIAL_DEVICE_BOOL][var_key] = True
    
                        else:
                            dev[Identifier.SPECIAL_DEVICE_VALUE][var_key] = int(str(tw_r2.text(1)))
    
            else:
                #is complex or Simple
                dev[Identifier.DEVICE_VALUES] = {}
                
                for r1 in range(0, r1_max):
                    tw_r1 = tw_root.child(r1)       
                    var_name = str(tw_r1.text(0))            
                    
                    dev[Identifier.DEVICE_VALUES][var_name] = {}
                    dev[Identifier.DEVICE_VALUES][var_name][Identifier.DEVICE_VALUES_ARGS] = Identifier.create_args(dev[Identifier.DEVICE_NAME], var_name)
                    dev[Identifier.DEVICE_VALUES][var_name][Identifier.DEVICE_VALUES_NAME] = Identifier.create_function_name(dev[Identifier.DEVICE_NAME], var_name)
                    
                    r2_max = tw_r1.childCount()
                    if r2_max != 1:
                        #complex device
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
            
            
            #save dev in the right device!
            if device_type == 0:
                simple_dev.append(dev)
            elif device_type == 1:    
                complex_dev.append(dev)         
            elif device_type == 2:
                special_dev.append(dev)
            else:
                EventLogger.debug("gui_config_handler: Unknown device?!: "+str(device_type))
        
        
        config_root["GENERAL TODO"] = general_section
        config_root[Identifier.SIMPLE_DEVICE] = simple_dev
        config_root[Identifier.COMPLEX_DEVICE] = complex_dev
        config_root[Identifier.SPECIAL_DEVICE] = special_dev
        
        return config_root
    

    load_devices = staticmethod(load_devices)
    clear_blueprint = staticmethod(clear_blueprint)
    complex_device_blueprints = staticmethod(complex_device_blueprints)
    simple_device_blueprints = staticmethod(simple_device_blueprints)
    special_device_blueprints = staticmethod(special_device_blueprints)
    create_config_file = staticmethod(create_config_file)
    