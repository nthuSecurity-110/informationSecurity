import sys
from ipaddress import ip_address
from subprocess import Popen, PIPE

from matplotlib.pyplot import contour

class Trace:
    def __init__(self):
        self.root_IP=input("input root ip: ") # tracert stop at root ip provided by use        
        self.cmdline = ['traceroute', self.root_IP]

        p = Popen(self.cmdline, stdout=PIPE)
        outputText = str(p.communicate()[0]).split(' ')
        # print(outputText)

        print("\nIP:")
        self.IPdict,self.IPlist=self.getLANRouters(outputText)
        print(self.IPdict)

    def getLANRouters(self, tracertList):
        # Get the direct ancestors in LAN
        ip_list = []
        for i in range(len(tracertList)):
            # some IP is in [], we have to take it out
            if (tracertList[i] != '' and tracertList[i][0] == '[') or (tracertList[i] != '' and tracertList[i][0] == '('  and tracertList[i][-1] == ')'):
                ip_list.append(tracertList[i][1:-1])

            if(all([item.isnumeric() for item in tracertList[i].split('.')]) and
                    len(tracertList[i].split('.')) == 4):  # if the string is in format of IP addr
                ip_list.append(tracertList[i])  # append it into ip_list
                
        ip_list.pop(0) # since the first ip would must be root_ip
        ip_list = list(dict.fromkeys(ip_list)) # remove duplicate ip in ip_list
        
        IP_dict={'private': [], 'public':[]}
        for ip in ip_list:
            if(ip_address(ip).is_private):
                IP_dict['private'].append(ip)
            else:
                IP_dict['public'].append(ip)

        # self.IPdict = IP
        return IP_dict,ip_list
