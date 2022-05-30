def prRed(skk): print("\033[91m {}\033[00m" .format(skk)) 
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk)) 
def prYellow(skk): print("\033[93m {}\033[00m" .format(skk)) 

import nmap
from datetime import datetime
from netaddr import IPAddress
from trace import *
from explore import *
from multiprocess import Process
from nodeData import *
# from subprocess import Popen, PIPE
# import os

block = "||"
stars = '*'*205
_host = "HOST ipv4"
_mac = "MAC Address"
_hostnames = "HOST NAMES"
_addresses = "ADDRESSES"
_vendor = "Vendor"
_status = "STATUS"
_state = "State"
_reason = "Reason"
_name = "Name"
_type = "Type"
_tcp = "TCP"
_port = "Port"
_conf = "Conf"
_portused = "PORT USED"
_portid = "Port ID"
_portstate = "State"
_portproto = "Protocol"
_osmatch = "OS Match"
_osaccuracy = "Accuracy"
_osline = "Line"
_osvendor = "Vendor"
_osfamily = "OS Family"
_osgen = "OS Gen"
_oscpe = "OS CPE"

class CheckLanHost:
    def __init__(self):
        self.ip_list = []
        self.contents = []

    def format_output(self, string):
        print(205*'=')
        print(f"{block}{_addresses:^201s}{block}")
        print(205*'-')
        host = list(string.keys())[0]
        mac = string[host]['addresses']['mac'] if 'mac' in string[host]['addresses'].keys() else '-'
        print(f"{block}{_host:^100s}|{host:^100s}{block}")
        print(f"{block}{_mac:^100s}|{mac:^100s}{block}")
        vendor = string[host]['vendor'][mac] if mac in string[host]['vendor'].keys() else '-'
        print(f"{block}{_vendor:^100s}|{vendor:^100s}{block}")

        print(205*'=')
        print(f"{block}{_hostnames:^201s}{block}")
        print(205*'-')
        hosts = string[host]['hostnames']
        hosts_num = len(string[host]['hostnames'])
        for nums in range(0, hosts_num):
            print(f"{'Host Num ' + str(nums+1):^205s}")
            h_name = string[host]['hostnames'][nums]['name'] if string[host]['hostnames'][nums]['name'] != None else '-'
            h_type = string[host]['hostnames'][nums]['type'] if string[host]['hostnames'][nums]['type'] != None else '-'
            print(f"{block}{_name:^100s}|{h_name:^100s}{block}")
            print(f"{block}{_type:^100s}|{h_type:^100s}{block}")

        if "status" in string[host].keys():
            print(205*'=')
            print(f"{block}{_status:^201s}{block}")
            print(205*'-')
            h_state = string[host]['status']['state'] if string[host]['status']['state'] != None else '-'
            h_reason = string[host]['status']['reason'] if string[host]['status']['reason'] != None else '-'
            print(f"{block}{_state:^100s}|{h_state:^100s}{block}")
            print(f"{block}{_reason:^100s}|{h_reason:^100s}{block}")

        if "tcp" in string[host].keys():
            print(205*'=')
            print(f"{block}{_tcp:^201s}{block}")
            print(205*'-')
            tcp_status = list(string[host]['tcp'])
            tcp_num = len(tcp_status) #number of tcp
            tcp_cnt = 0
            for it in tcp_status:
                tcp_cnt += 1
                if tcp_cnt == tcp_num:
                    port_name = string[host]['tcp'][it]['name'] if string[host]['tcp'][it]['name'] != None else '-'
                    port_state = string[host]['tcp'][it]['state'] if string[host]['tcp'][it]['state'] != None else '-'
                    port_reason = string[host]['tcp'][it]['reason'] if string[host]['tcp'][it]['reason'] != None else '-'
                    port_conf = string[host]['tcp'][it]['conf'] if string[host]['tcp'][it]['conf'] != None else '-'
                    print(f"{block}{_port:^100s}|{port_name:^100s}{block}")
                    print(f"{block}{_state:^100s}|{port_state:^100s}{block}")
                    print(f"{block}{_reason:^100s}|{port_reason:^100s}{block}")
                    print(f"{block}{_conf:^100s}|{port_conf:^100s}{block}")
                else:
                    port_name = string[host]['tcp'][it]['name'] if string[host]['tcp'][it]['name'] != None else '-'
                    port_state = string[host]['tcp'][it]['state'] if string[host]['tcp'][it]['state'] != None else '-'
                    port_reason = string[host]['tcp'][it]['reason'] if string[host]['tcp'][it]['reason'] != None else '-'
                    port_conf = string[host]['tcp'][it]['conf'] if string[host]['tcp'][it]['conf'] != None else '-'
                    print(f"{block}{_port:^100s}|{port_name:^100s}{block}")
                    print(f"{block}{_state:^100s}|{port_state:^100s}{block}")
                    print(f"{block}{_reason:^100s}|{port_reason:^100s}{block}")
                    print(f"{block}{_conf:^100s}|{port_conf:^100s}{block}")
                    print(205*'~')

        if "portused" in string[host].keys():
            print(205*'=')
            print(f"{block}{_portused:^201s}{block}")
            print(205*'-')
            port_used = list(string[host]['portused'])
            port_used_num = len(port_used)
            port_cnt = 0
            for it in port_used:
                port_cnt += 1
                if port_cnt == port_used_num:
                    port_id = it['portid'] if it['portid'] != None else '-'
                    port_state = it['state'] if it['state'] != None else '-'
                    port_proto = it['proto'] if it['proto'] != None else '-'
                    print(f"{block}{_portid:^100s}|{port_id:^100s}{block}")
                    print(f"{block}{_portstate:^100s}|{port_state:^100s}{block}")
                    print(f"{block}{_portproto:^100s}|{port_proto:^100s}{block}")
                else:
                    port_id = it['portid'] if it['portid'] != None else '-'
                    port_state = it['state'] if it['state'] != None else '-'
                    port_proto = it['proto'] if it['proto'] != None else '-'
                    print(f"{block}{_portid:^100s}|{port_id:^100s}{block}")
                    print(f"{block}{_portstate:^100s}|{port_state:^100s}{block}")
                    print(f"{block}{_portproto:^100s}|{port_proto:^100s}{block}")
                    print(205*'~')

        if "osmatch" in string[host].keys():
            print(205*'=')
            print(f"{block}{_osmatch:^201s}{block}")
            print(205*'-')
            os_match = list(string[host]['osmatch'])
            os_match_num = len(os_match)
            os_cnt = 0
            for it in os_match:
                os_cnt += 1
                if os_cnt == os_match_num:
                    os_name = it['name'] if it['name'] != None else '-'
                    os_accuracy = it['accuracy'] if it['accuracy'] != None else '-'
                    os_line = it['line'] if it['line'] != None else '-'

                    os_class = it['osclass']
                    os_class_num = len(os_class)
                    for n in range(0, os_class_num):
                        print(f"{block}{'OS Class ' + str(n+1) + ' (' + os_name + ')':^201s}{block}")
                        os_type = it['osclass'][n]['type'] if it['osclass'][n]['type'] != None else '-'
                        os_vendor = it['osclass'][n]['vendor'] if it['osclass'][n]['vendor'] != None else '-'
                        os_family = it['osclass'][n]['osfamily'] if it['osclass'][n]['osfamily'] != None else '-'
                        os_gen = it['osclass'][n]['osgen'] if it['osclass'][n]['osgen'] != None else '-'
                        print(f"{block}{_name:^100s}|{os_name:^100s}{block}")
                        print(f"{block}{_osaccuracy:^100s}|{os_accuracy:^100s}{block}")
                        print(f"{block}{_osline:^100s}|{os_line:^100s}{block}")
                        print(f"{block}{_type:^100s}|{os_type:^100s}{block}")
                        print(f"{block}{_osvendor:^100s}|{os_vendor:^100s}{block}")
                        print(f"{block}{_osfamily:^100s}|{os_family:^100s}{block}")
                        print(f"{block}{_osgen:^100s}|{os_gen:^100s}{block}")
                        os_cpe = it['osclass'][n]['cpe'] if it['osclass'][n]['cpe'] != None else '-'
                        os_cpe_num = len(os_cpe)
                        for num in range(0, os_cpe_num):
                            print(f"{block}{_oscpe+' '+str(num+1):^100s}|{os_cpe[num]:^100s}{block}")
                else:
                    os_name = it['name'] if it['name'] != None else '-'
                    os_accuracy = it['accuracy'] if it['accuracy'] != None else '-'
                    os_line = it['line'] if it['line'] != None else '-'
                    os_class = it['osclass']
                    os_class_num = len(os_class)
                    for n in range(0, os_class_num):
                        print(f"{block}{'OS Class ' + str(n+1) + ' (' + os_name + ')':^201s}{block}")
                        os_type = it['osclass'][n]['type'] if it['osclass'][n]['type'] != None else '-'
                        os_vendor = it['osclass'][n]['vendor'] if it['osclass'][n]['vendor'] != None else '-'
                        os_family = it['osclass'][n]['osfamily'] if it['osclass'][n]['osfamily'] != None else '-'
                        os_gen = it['osclass'][n]['osgen'] if it['osclass'][n]['osgen'] != None else '-'
                        print(f"{block}{_name:^100s}|{os_name:^100s}{block}")
                        print(f"{block}{_osaccuracy:^100s}|{os_accuracy:^100s}{block}")
                        print(f"{block}{_osline:^100s}|{os_line:^100s}{block}")
                        print(f"{block}{_type:^100s}|{os_type:^100s}{block}")
                        print(f"{block}{_osvendor:^100s}|{os_vendor:^100s}{block}")
                        print(f"{block}{_osfamily:^100s}|{os_family:^100s}{block}")
                        print(f"{block}{_osgen:^100s}|{os_gen:^100s}{block}")
                        os_cpe = it['osclass'][n]['cpe'] if it['osclass'][n]['cpe'] != None else '-'
                        os_cpe_num = len(os_cpe)
                        for num in range(0, os_cpe_num):
                            print(f"{block}{_oscpe+' '+str(num+1):^100s}|{os_cpe[num]:^100s}{block}")
                    print(205*'~')
            print(205*'=')

    def callback_result(self, host, scan_result):
        print('\n'+stars+'\n')
        if scan_result != None and scan_result['scan'] != None and scan_result['scan'] != {}:
            # print(scan_result['scan'])
            prGreen(f"{'Data found for host ' + host}")
            self.format_output(scan_result['scan'])
            explore = Explore()
            explore.start()
        else:
            prRed(f"{'No available data for host ' + host}")
    # def test_callback(self, host, scan_result):
    #     print(scan_result)

    def getIP(self):
        return self.ip_list

    def AllLanHost(self, config):
        trace = Trace()
        wireless_lan_gateway = config.getGateway11()
        wireless_lan_subnet = config.getSubnet11()
        mask_num = wireless_lan_subnet

        # cmd = input("Choose an option: '-sS'/'-sP'/'-sL'/'-PS'/'-PU': ")
        cmd = '-sS -F -O -T4' 
        cmd+=" --min-hostgroup 20"
        # cmd = "-sn"
        # the fastest parameters I find so far
        # cmd+=" --min-rate 10"

        start_time = datetime.now()
        AsyncScan = nmap.PortScannerAsync()
        Scan = nmap.PortScanner()
        
        for i in range(len(trace.IPlist)):
            if i != 0 and trace.IPlist[i-1] == trace.root_IP: # stop at root IP
                break

            LAN_ip=trace.IPlist[i]
            mask_num = 24 if LAN_ip != wireless_lan_gateway else mask_num
            LAN_ip = LAN_ip + '/' + str(mask_num)
            # LAN_ip = LAN_ip + '/' + str(30)
            
            # p = Popen(['nmap -sn '+ ip], stdout=PIPE)
            # p = Popen(['nmap', '-sn ', ip], stdout=PIPE)
            # outputText = str(p.communicate()[0]).split(' ')
            
            # outputText = os.popen("nmap -sn "+ip).read()
            # print(f'outputText: {outputText}')
            
            prYellow('\n' + 96*'#' + "START SCANNING" + 95*'#' + '\n')
            print(f"{'scanning LAN under '+LAN_ip:^205s}")

            Scan.scan(hosts=LAN_ip, arguments="-sn", sudo=True)
            hosts_list = Scan.all_hosts()
            print(f'alive host in LAN {LAN_ip}: {hosts_list}\n')

            for ip in hosts_list:
                self.ip_list.append(ip)
                AsyncScan.scan(hosts=ip, arguments=cmd, callback=self.callback_result, sudo=True)
                # AsyncScan.scan(hosts=ip, arguments=cmd, callback=self.test_callback, sudo=True)
                while AsyncScan.still_scanning():
                    AsyncScan.wait(2)
        end_time = datetime.now()
        print("\nDuration: {}".format(end_time - start_time))