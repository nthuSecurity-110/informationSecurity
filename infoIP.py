import sys
import subprocess

class IPConfig:
     '''
          This class utilizes subprocess to generate a list of Windows IP Configuration.
          The IP Configuration list includes:
               Windows IP Configuration,                              as 1
               Ethernet adapter Ethernet,                             as 2
               Unknown adapter OpenVPN Wintun                         as 3
               Ethernet adapter Ethernet 2                            as 4
               Unknown adapter Local Area Connection                  as 5
               Wireless LAN adapter Local Area Connection* 2          as 6
               Ethernet adapter VMware Network Adapter VMnet1         as 7
               Ethernet adapter VMware Network Adapter VMnet8         as 8
               Ethernet adapter VMware Network Adapter VMnet5         as 9
               Wireless LAN adapter Local Area Connection* 1          as 10
               Wireless LAN adapter Wi-Fi                             as 11
               Ethernet adapter 1                                     as 12
               Ethernet adapter Bluetooth Network Connection          as 13
          The commands are:
          __init__                initialize the dictionary consisting of Windows IP Configurations.
          get_gateway_9           gets the default gateway for Wireless LAN adapter Wi-Fi.
     '''
     def __init__(self):
          """
          This is a Windows IP Configuration dictionary initializer.
          Its main purpose is to initialize a nested dictionary of Windows IP Configurations.
          Takes self as parameter.
          """
          # self.net_dict = ifcfg.interfaces()

     def get_gateway_11(self):
          """
          """
          return '192.168.50.1'
     
     def get_subnetmask_11(self):
          """
          """
          return '255.255.255.0'

     def decimalToBinary(self, n):
          """
          """
          return bin(n).replace("0b", "")

     def calculate_mask(self, subnet_mask):
          """
          """
          try:
               parse_lst = subnet_mask.split('.')
               tmp = []
               for i in parse_lst:
                    tmp.append(self.decimalToBinary(int(i)))
               mask_str = ''.join(tmp)
               return mask_str.count('1')
          except:
               sys.stderr.write("An error has occured.")