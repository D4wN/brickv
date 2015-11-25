from brickv.bindings.brick_red import RED
from brickv.bindings.ip_connection import IPConnection
from brickv.plugin_system.plugins.red.api import REDSession
from brickv.plugin_system.plugins.red.program_utils import ChunkedDownloaderBase

HOST = 'localhost'
PORT = 4223
UID = '37GmTY' # Change to your UID

def increase_error_count():
    print "ErrorCount ++"

if __name__ == "__main__":
    print "GoGo"

    ipcon = IPConnection() # Create IP connection
    red = RED(UID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd

    red_path = "/home/tf/test.txt"
    my_path = "C:\\Programmierung\\Repos\\Python\\TinkervisionBrickv\\"

    session = REDSession(red, increase_error_count).create()
    downloader = ChunkedDownloaderBase(session)
    print "Prepeared = " + str(downloader.prepare(red_path))
    downloader.start(my_path)

    print "Done?"

    raw_input('--------\nPress key to exit\n--------\n') # Use input() in Python 3

    ipcon.disconnect()