import nmap
from datetime import datetime
from netaddr import IPAddress
from trace import *

# trace = Trace()
class Test:
    def __init__(self, os):
        self.user_os = os

    def callback_result(self, host, scan_result):
        if self.user_os == "win":
            print('------------------')
            print("scan_res:", scan_result)
            if scan_result['scan'] != {}:
                print(scan_result['scan'])
            else:
                print(host)
        elif self.user_os == "linux":
            print('------------------')
            print("scan_res:", scan_result)
            if scan_result != None and scan_result['scan'] != None:
                print(scan_result['scan'])
            else:
                print(host)
        else:
            print("err")

    def AllLanHostTest(self, os):
        wireless_lan_gateway = "140.114.71.253"
        wireless_lan_subnet = "255.255.255.0"
        if os == 'win':
            mask_num = IPAddress(wireless_lan_subnet).netmask_bits()
        elif os == 'linux':
            mask_num = wireless_lan_subnet
        else:
            mask_num=-1

        # cmd = input("Choose an option: '-sS'/'-sP'/'-sL'/'-PS'/'-PU': ")
        cmd = '-sS -F -O -T4'
        # cmd+=" --min-paralleism 10"
        cmd+=" --min-hostgroup 20"
        # cmd+=" --min-rate 10"
        # cmd+=" --max-scan-delay 500ms" 
        # cmd+=" --host-timeout 100ms" # 100ms is too short, some msg lost
        start_time = datetime.now()
        nma = nmap.PortScannerAsync()
        # privateIP_list = trace.IPdict['private']
        privateIP_list = [wireless_lan_gateway]
        for ip in privateIP_list:
            mask_num = 16 if ip != wireless_lan_gateway else mask_num
            ip = ip + '/' + str(mask_num)

            print(f"scanning LAN under {ip}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            nma.scan(hosts=ip, arguments=cmd, callback=self.callback_result)
            while nma.still_scanning():
                nma.wait(2)
        end_time = datetime.now()
        print("Duration: {}".format(end_time - start_time))