import unittest

from ApiTests.Util import Helper
from brickv.bindings.brick_red import RED
from brickv.bindings.ip_connection import IPConnection

##### TestModule Functions
def setUpModule():
    print "Setting up the Tests..."
    Helper.ipcon = IPConnection()
    Helper.ipcon.connect(Helper.HOST, Helper.PORT)
    Helper.red = RED(Helper.UID, Helper.ipcon)

def tearDownModule():
    print "Tearing down..."
    Helper.ipcon.disconnect()

# FIXME no solution! just a workaround!
setUpModule()
from ApiTests.modules.Colormatch import Colormatch
from ApiTests.modules.Downscale import Downscale
from ApiTests.modules.Functions import Functions
from ApiTests.modules.Grayfilter import Grayfilter
from ApiTests.modules.Module import Module
from ApiTests.modules.Motiondetect import Motiondetect
from ApiTests.modules.Snapshot import Snapshot
from ApiTests.modules.Stream import Stream

# tearDownModule() # TODO how to export test classes?!

##### MAIN
if __name__ == '__main__':
    unittest.main()
