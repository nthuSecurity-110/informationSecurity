import sys
from ipaddress import ip_address
from subprocess import Popen, PIPE


def getLANRouters(tracertList):  # Get the direct ancestors in LAN
    ip_list = []
    for i in range(len(tracertList)):
        # some IP is in [], we have to take it out
        if (tracertList[i] != '' and tracertList[i][0] == '[') or \
            (tracertList[i] != '' and tracertList[i][0] == '(' and tracertList[i][-1] == ')'):
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

    return IP,ip_list


if len(sys.argv) < 2:
    print('Usage:python tracert.py "command to watch"\n\
Example:python tracert.py tracert 192.168.0.1\n')
    sys.exit(1)

cmdline_ins = sys.argv[1:]
p = Popen(cmdline_ins, stdout=PIPE)
outputText = str(p.communicate()[0]).split(' ')
print(outputText)

print("\nIP:")
b,a=getLANRouters(outputText)
print(a)
print(b)
