#!/usr/bin/env python2

from sys import argv
import subprocess

if len(argv) < 13:
    exit (0)

enct = argv[6]
key = argv[7]
ip = argv[2]
mask = argv[3]
gw = argv[4]
dns = argv[5]
search_domain = argv[8]
dns_domain =argv[9]
dns2 = argv[10]
dns3 = argv[11]
automatic = argv[12]

prepend_cmd = "/usr/bin/wicd-cli --wireless "+"-n"+argv[1]
cmd_wireless_connect1 = prepend_cmd+" -p enctype -s "+enct
cmd_wireless_connect2 = prepend_cmd+" -p key -s "+key
cmd_wireless_connect3 = prepend_cmd+" -p ip -s "+ip
cmd_wireless_connect4 = prepend_cmd+" -p netmask -s "+mask
cmd_wireless_connect5 = prepend_cmd+" -p gateway -s "+gw
cmd_wireless_connect6 = prepend_cmd+" -p dns1 -s "+dns
cmd_wireless_connect7 = prepend_cmd+" -p search_domain -s "+search_domain
cmd_wireless_connect8 = prepend_cmd+" -p dns_domain -s "+dns_domain
cmd_wireless_connect9 = prepend_cmd+" -p dns2 -s "+dns2
cmd_wireless_connect10 = prepend_cmd+" -p dns3 -s "+dns3
cmd_wireless_connect11 = prepend_cmd+" -p automatic -s "+automatic
cmd_wireless_disconnect_connect = "/usr/bin/wicd-cli --wireless -x; "+prepend_cmd+" -c"

ps = subprocess.Popen(cmd_wireless_connect1, shell=True)
comm = ps.communicate()
ps = subprocess.Popen(cmd_wireless_connect2, shell=True)
comm = ps.communicate()
ps = subprocess.Popen(cmd_wireless_connect3, shell=True)
comm = ps.communicate()
ps = subprocess.Popen(cmd_wireless_connect4, shell=True)
comm = ps.communicate()
p = subprocess.Popen(cmd_wireless_connect5, shell=True)
comm = ps.communicate()
ps = subprocess.Popen(cmd_wireless_connect4, shell=True)
comm = ps.communicate()
ps = subprocess.Popen(cmd_wireless_connect7, shell=True)
comm = ps.communicate()
ps = subprocess.Popen(cmd_wireless_connect8, shell=True)
comm = ps.communicate()
ps = subprocess.Popen(cmd_wireless_connect9, shell=True)
comm = ps.communicate()
ps = subprocess.Popen(cmd_wireless_connect10, shell=True)
comm = ps.communicate()
ps = subprocess.Popen(cmd_wireless_connect11, shell=True)
comm = ps.communicate()
ps = subprocess.Popen(cmd_wireless_disconnect_connect, shell=True)
comm = ps.communicate()
