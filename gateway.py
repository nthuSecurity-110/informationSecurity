"""
UNUSED
"""

import sys
import ifcfg

class Gateway:
    '''
    This class utilizes ifcfg to generate a dictionary of Windows IP Configuration.
    The IP Configuration list includes:
        Ethernet adapter Ethernet,
        Unknown adapter OpenVPN Wintun                          as 1
        Ethernet adapter Ethernet 2                             as 2
        Unknown adapter Local Area Connection                   as 3
        Wireless LAN adapter Local Area Connection* 2           as 4
        Ethernet adapter VMware Network Adapter VMnet1          as 5
        Ethernet adapter VMware Network Adapter VMnet8          as 6
        Ethernet adapter VMware Network Adapter VMnet5          as 7
        Wireless LAN adapter Local Area Connection* 1           as 8
        Wireless LAN adapter Wi-Fi                              as 9
        Ethernet adapter 1                                      as 10
        Ethernet adapter Bluetooth Network Connection           as 11
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
        self.net_dict = ifcfg.interfaces()

    def get_gateway_9(self):
        """
        """
        CUR_WIFI = "Wireless LAN adapter Wi-Fi"
        DEF_GATEWAY = "default_gateway"

        try:
            if CUR_WIFI in self.net_dict.keys():
                default_gateway = self.net_dict[CUR_WIFI][DEF_GATEWAY]
        except KeyError:
            sys.stderr.write("Default Gateway does not exist.")
        except:
            sys.stderr.write("An error has occured.")
    
        return default_gateway
