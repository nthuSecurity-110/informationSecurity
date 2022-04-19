import sys
from infoIP import *
from PortScanAsync import *
import nmap

info = IPConfig()

def callback_result(host, scan_result):
    print('------------------')
    print(host, scan_result)

wireless_lan_gateway = info.get_gateway_11()
wireless_lan_subnet = info.get_subnetmask_11()
mask_num = info.calculate_mask(wireless_lan_subnet)

ipAddr = wireless_lan_gateway + '/' + str(mask_num)
print(ipAddr)

if __name__ == '__main__':
    nma = nmap.PortScannerAsync()
    nma.scan(hosts=ipAddr, arguments='-sS', callback=callback_result)
    while nma.still_scanning():
        nma.wait(2)