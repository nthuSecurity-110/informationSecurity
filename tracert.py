import sys
from ipaddress import ip_address
from subprocess import Popen, PIPE

class Trace:
    def __init__(self):
        self.cmdline = ['tracert', '8.8.8.8']
        p = Popen(self.cmdline, stdout=PIPE)
        outputText = str(p.communicate()[0]).split(' ')
        print(outputText)

        print("\nIP:")
        b,a=self.getLANRouters(outputText)
        self.IPdict = a
        print(b)

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

        ip_list.pop(0)
        IP={'private': [], 'public':[]}
        for ip in ip_list:
            if(ip_address(ip).is_private):
                IP['private'].append(ip)
            else:
                IP['public'].append(ip)

        # self.IPdict = IP
        return IP,ip_list