from time import sleep
from brickv.bindings.brick_red import RED
from brickv.bindings.ip_connection import IPConnection

HOST = "localhost"
PORT = 4223
UID = "37GmTY"

def doStuff(red):
    test_no_param_functions(red)

    show_running_modules(red)
    start_stream(red)
    show_running_modules(red)
    start_module(red,"motiondetect")
    show_running_modules(red)
    start_module(red,"motiondetect")
    kill_all_modules(red)
    sleep(2) # wait module removal
    show_running_modules(red)

def start_stream(red):
    result = red.vision_module_start("stream")
    print "START_MODULE = " + str(result)
    if result.result == 0:
        sleep(1)
        result_url = red.vision_string_parameter_get(result.id, 'url')
        print str(result_url)
        stream_path = None
        if result_url.value != "<inactive>":
            stream_path = result_url.value
        else:
            stream_path = 'rtsp://192.168.0.66:8554/tinkervision'
        from subprocess import call
        print "STREAM_PATH = " + str(stream_path)
        #print call(['C://Tools//VLC//vlc', '-vvv', stream_path])

def start_module(red, md_name):
    result = red.vision_module_start(md_name)
    print "START_MODULE(" + str(md_name) + ") = " + str(result)

def kill_all_modules(red):
    print "KILL_ALL_MODULES = " + str(red.vision_remove_all_modules())

def show_running_modules(red):
    ids = ""
    c = red.vision_libs_loaded_count()
    if c.result != 0:
        print "_show_module_params::vision_libs_loaded_count"
        return
    for i in range(0, c.count):
        md_id = red.vision_module_get_id(i)
        if md_id.result != 0:
            #print "_button_debug_print_running_modules::vision_module_get_id"
            continue
        ids += str(md_id.id)+","

    print "SHOW_RUNNING_MODULES = " + str(ids)

def test_no_param_functions(red):
    print "vision_is_valid                 = " + str(red.vision_is_valid())
    print "vision_camera_available         = " + str(red.vision_camera_available())
    print "vision_get_frameperiod         = " + str(red.vision_get_frameperiod()) # struct.error: unpack requires a string argument of length 4
    print "vision_libs_count              = " + str(red.vision_libs_count()) # brickv.bindings.ip_connection.Error: Got invalid parameter for function 89 (-9)
    print "vision_libs_loaded_count       = " + str(red.vision_libs_loaded_count()) # brickv.bindings.ip_connection.Error: Got invalid parameter for function 90 (-9)
    print "vision_lib_get_user_prefix      = " + str(red.vision_lib_get_user_prefix())
    print "vision_lib_get_system_load_path = " + str(red.vision_lib_get_system_load_path())
    print "vision_remove_all_modules       = " + str(red.vision_remove_all_modules()) # brickv.bindings.ip_connection.Error: Got invalid parameter for function 97 (-9)
    # print "" + str(red.)
    # print "" + str(red.)
    # print "" + str(red.)

if __name__ == "__main__":
    ipcon = IPConnection()
    ipcon.connect(HOST, PORT)
    red = RED(UID, ipcon)
    doStuff(red);
    #raw_input("Press key to exit\n") # Use input() in Python 3
    ipcon.disconnect()