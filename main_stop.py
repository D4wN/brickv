#!/usr/bin/python
import sys

# RedBrick resource wrapper
from rb_setup import RedBrick
# available testfiles

def usage_exit(prog):
    print "Usage 1 (on RedBrick):", prog, "rb-uid testfilename", \
          "[host = localhost [port = 4223]]"
    print "Usage 0 (local):", prog, "- testfilename"

if __name__ == '__main__':
    host = "localhost"
    port = 4223
    prog = None
    if len(sys.argv) < 3:
        usage_exit(sys.argv[0])

    module_id = sys.argv[2]

    if sys.argv[1] != '-':
        uid = sys.argv[1]

        try:
            host =  sys.argv[3] if len(sys.argv) > 3 else host
            port = int(sys.argv[4]) if len(sys.argv) > 4 else port

        except KeyError, e:
            print "No such file", filename + ".py or not registered"
            exit(-1)

        with RedBrick(uid, host, port) as rb:
            print "Try to remove " + str(module_id) + " from modules!"
            print "Removed(0 is good) = " + str(rb.vision_module_remove(int(module_id)))
            #prog.run(rb)

    else:
        try:
            print "YOU SHOULD NOT BE HERE!"
            #prog = testfiles[filename]
        except KeyError, e:
            print "No such file", filename + ".py or not registered"
            exit(-1)

        with Lib() as lib:
            prog.run(lib)
