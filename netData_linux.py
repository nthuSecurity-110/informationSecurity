import sys
import subprocess
from itertools import groupby
  
class NetworkData_Linux:
    '''
        This class utilizes subprocess to generate a dictionary of Windows IP Configuration.
        The IP Configuration list includes:
            Windows IP Configuration                            as 1
            Ethernet adapter Ethernet                           as 2
            Unknown adapter OpenVPN Wintun                      as 3
            Ethernet adapter Ethernet 2                         as 4
            Unknown adapter Local Area Connection               as 5
            Wireless LAN adapter Local Area Connection* 1       as 6
            Wireless LAN adapter Local Area Connection* 2       as 7
            Ethernet adapter VMware Network Adapter VMnet1      as 8
            Ethernet adapter VMware Network Adapter VMnet8      as 9
            Ethernet adapter VMware Network Adapter VMnet5      as 10
            Wireless LAN adapter Wi-Fi                          as 11
            Ethernet adapter Bluetooth Network Connection       as 12
        The commands are:
            __init__                      initialized the dictionary of Windows IP Configuration
            getGateway11                  returns the gateway of Wireless LAN adapter Wi-Fi connection
            getSubnet11                   returns the Subnet Mask of Wireless LAN adapter Wi-Fi connection
    '''
    def __init__(self):
        """
            Creates a dictionary of Windows IP Configurations by utilizing subprocess.
            Argument(s): self
            Returns: a dictionary
        """
        brd_grep= "ip a|grep brd|grep inet|cut -d ' '  -f 6" # the script that get ip and subnet
        ip_and_subnet = subprocess.check_output(brd_grep, shell=True).decode('big5', errors='ignore')
        self.ip ,self.subnet = ip_and_subnet.split('/')[0], ip_and_subnet.split('/')[1]
        print(f"ip: {self.ip}\nsubnet: {self.subnet}")
    
    def getGateway11(self):
        """
            Retrieves the gateway value of the Wireless LAN Adapter Wi-Fi connection.
            Argument(s): self
            Returns: gateway value of Wireless LAN Adapter Wi-Fi connection.
        """
        return self.ip

    def getSubnet11(self):
        """
            Retrieves the subnet mask value of the Wireless LAN Adapter Wi-Fi connection.
            Argument(s): self
            Returns: subnet mask value of Wireless LAN Adapter Wi-Fi connection.
        """
        return self.subnet