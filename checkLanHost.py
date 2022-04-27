import nmap
from datetime import datetime
from netaddr import IPAddress
from sqlalchemy import null
from tracert import *

trace = Trace()

def callback_result(host, scan_result):
    print('------------------')
    if scan_result['scan'] != {}:
        print(host, scan_result['scan'])
    

def LanHost(config, os):
    wireless_lan_gateway = config.getGateway11()
    wireless_lan_subnet = config.getSubnet11()
    if os == 'win':
        mask_num = IPAddress(wireless_lan_subnet).netmask_bits()
    elif os == 'linux':
        mask_num = wireless_lan_subnet
    else:
        mask_num=-1




    # cmd = input("Choose an option: '-sS'/'-sP'/'-sL'/'-PS'/'-PU': ")
    cmd = '-sS -F -O'
    cmd+=" --min-hostgroup 20"
    cmd+=" --min-rate 10"

    start_time = datetime.now()
    nma = nmap.PortScannerAsync()
    privateIP_list = trace.IPdict['private']
    for ip in privateIP_list:
        mask_num = 16 if ip != wireless_lan_gateway else mask_num
        ip = ip + '/' + str(mask_num)

        print(f"scanning LAN under {ip}")
        nma.scan(hosts=ip, arguments=cmd, callback=callback_result)
        while nma.still_scanning():
            nma.wait(2)
    end_time = datetime.now()
    print("Duration: {}".format(end_time - start_time))