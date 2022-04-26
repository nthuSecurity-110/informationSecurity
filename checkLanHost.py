from asyncio.windows_events import NULL
import imp
import nmap
from datetime import datetime
from netaddr import IPAddress

def callback_result(host, scan_result):
    print('------------------')
    print(host, scan_result)

def LanHost(config, os):
    wireless_lan_gateway = config.getGateway11()
    wireless_lan_subnet = config.getSubnet11()
    if os == 'win':
        mask_num = IPAddress(wireless_lan_subnet).netmask_bits()
    elif os == 'linux':
        mask_num = wireless_lan_subnet
    else:
        mask_num=-1

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