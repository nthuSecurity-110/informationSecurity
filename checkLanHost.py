import nmap
from datetime import datetime
from netaddr import IPAddress
from trace import *

class CheckLanHost:
    def __init__(self, os):
        self.os = os

    def callback_result(self, host, scan_result):
        if self.os == "win":
            print('------------------')
            print("scan_res:", scan_result)
            if scan_result['scan'] != {}:
                print(scan_result['scan'])
            else:
                print(host)
        elif self.os == "linux":
            print('------------------')
            print("scan_res:", scan_result)
            if scan_result != None and scan_result['scan'] != None and scan_result['scan'] != {}:
                print(scan_result['scan'])
            else:
                print(host)
        else:
            print("err")

    def AllLanHost(self, config):
        trace = Trace(self.os)
        wireless_lan_gateway = config.getGateway11()
        wireless_lan_subnet = config.getSubnet11()
        if self.os == 'win':
            mask_num = IPAddress(wireless_lan_subnet).netmask_bits()
        elif self.os == 'linux':
            mask_num = wireless_lan_subnet
        else:
            mask_num=-1

        # cmd = input("Choose an option: '-sS'/'-sP'/'-sL'/'-PS'/'-PU': ")
        cmd = '-sS -F -O -T4' 
        cmd+=" --min-hostgroup 20"
        # the fastest parameters I find so far
        # cmd+=" --min-rate 10"

        start_time = datetime.now()
        nma = nmap.PortScannerAsync()
        
        for i in range(len(trace.IPlist)):
            if i != 0 and trace.IPlist[i-1] == trace.root_IP: # stop at root IP
                break

            ip=trace.IPlist[i]
            mask_num = 24 if ip != wireless_lan_gateway else mask_num
            ip = ip + '/' + str(30)

            print(f"scanning LAN under {ip}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            nma.scan(hosts=ip, arguments=cmd, callback=self.callback_result)
            while nma.still_scanning():
                nma.wait(2)
        end_time = datetime.now()
        print("Duration: {}".format(end_time - start_time))
