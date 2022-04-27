import nmap
from datetime import datetime
from netaddr import IPAddress
from tracert import *

# trace = Trace()

def callback_result(host, scan_result):
    print('------------------')
    if scan_result['scan'] != {}:
        print(host, scan_result['scan'])

# def LanHost(config, os):
def LanHost(os):
    # wireless_lan_gateway = config.getGateway11()
    # wireless_lan_subnet = config.getSubnet11()
    wireless_lan_gateway = "172.16.15.254"
    wireless_lan_subnet = "255.255.240.0"
    if os == 'win':
        mask_num = IPAddress(wireless_lan_subnet).netmask_bits()
    elif os == 'linux':
        mask_num = wireless_lan_subnet
    else:
        mask_num=-1




    # cmd = input("Choose an option: '-sS'/'-sP'/'-sL'/'-PS'/'-PU': ")
    cmd = '-sS -F -O'
    # cmd+=" --min-paralleism 10"
    cmd+=" --min-hostgroup 20"
    cmd+=" --min-rate 10"
    # cmd+=" --max-scan-delay 500ms" 
    # cmd+=" --host-timeout 100ms" # 100ms is too short, some msg lost
    start_time = datetime.now()
    nma = nmap.PortScannerAsync()
    # privateIP_list = trace.IPdict['private']
    privateIP_list = ["172.16.15.254"]
    for ip in privateIP_list:
        mask_num = 16 if ip != wireless_lan_gateway else mask_num
        ip = ip + '/' + str(mask_num)

        print(f"scanning LAN under {ip}")
        nma.scan(hosts="192.168.50.1-100", arguments=cmd, callback=callback_result)
        # nma.scan(hosts="172.16.0.179", arguments=cmd, callback=callback_result)
        while nma.still_scanning():
            nma.wait(2)
    end_time = datetime.now()
    print("Duration: {}".format(end_time - start_time))