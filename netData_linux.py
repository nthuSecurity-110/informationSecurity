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
            __init__                        initialized the dictionary of Windows IP Configuration
            getGateway11                  returns the gateway of Wireless LAN adapter Wi-Fi connection
            getSubnet11                   returns the Subnet Mask of Wireless LAN adapter Wi-Fi connection
    '''
    def __init__(self):
        """
            Creates a dictionary of Windows IP Configurations by utilizing subprocess.
            Argument(s): self
            Returns: a dictionary
        """
        # Traverse the ipconfig information
        self.data = subprocess.check_output(['ip','a']).decode('big5', errors='ignore').split('\n')
        for i in range(0, len(self.data)):
                self.data[i] = self.data[i].lstrip()
        self.info_arr = self.data[8].split(' ')
        self.net_arr = self.info_arr[1].split('/')
        self.ip = self.net_arr[0]
        self.subnet = self.net_arr[1]
        print("ip", self.ip)
        print("subnet", self.subnet)
        # for item in data:
        #      print(item.split('\r')[:-1])
        # print(self.net_dict)
    
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