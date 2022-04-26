import sys
from utilities import *
from netData import *
import nmap
from datetime import datetime

util = Helper()
config = NetworkData()

def callback_result(host, scan_result):
    print('------------------')
    print(host, scan_result)

def LanHost():
    wireless_lan_gateway = config.getGateway11()
    wireless_lan_subnet = config.getSubnet11()
    mask_num = util.calculateMask(wireless_lan_subnet)

    ipAddr = wireless_lan_gateway + '/' + str(mask_num)
    print(ipAddr)


    cmd = input("Choose an option: '-sS'/'-sP'/'-sL'/'-PS'/'-PU': ")
    start_time = datetime.now()
    nma = nmap.PortScannerAsync()
    nma.scan(hosts=ipAddr, arguments=cmd, callback=callback_result)
    while nma.still_scanning():
        nma.wait(2)
    end_time = datetime.now()
    print("Duration: {}".format(end_time - start_time))