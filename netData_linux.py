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
        '''
        tmp_ip_list = []
        ip_list = []
        info_list = []
        network_type = []

        self.net_dict = {}

        cnt = 0
        for item in self.data:
            if item == '\r' or item == '':
                if (cnt == 2 and item == '\r') or (cnt == 2 and item == ''):
                    tmp_ip_list.extend(info_list)
                    tmp_ip_list.extend(['-1:-1'])
                    info_list.clear()
                    cnt = 1
                else:
                    cnt += 1
            else:
                if cnt == 2:
                    info_list.append(item)
                if cnt == 1:
                    network_type.append(item)

        i = (list(g) for _, g in groupby(tmp_ip_list, key='-1:-1'.__ne__))
        tmp_ip_list = [a + b for a, b in zip(i, i)]

        for elm in tmp_ip_list:
            for str in elm:
                elm = [elem.replace(' ', '').replace('\r', '') for elem in elm]
            ip_list.append(elm)

        tmp = []
        for lists in ip_list:
            for str_val in lists:
                list_of_words = str_val.split(':', 1)
                if len(list_of_words) > 1:
                    list_of_words = [list_of_words[0].replace('.', ''), list_of_words[1]]
                tmp.append(list_of_words)

        for sublists in tmp:
            if sublists == ['-1', '-1']:
                tmp[tmp.index(sublists)] = '-1'

        j = (list(g) for _, g in groupby(tmp, key='-1'.__ne__))
        ip_list = [a + b for a, b in zip(j, j)]

        for items in ip_list:
            items.remove('-1')
        for elm in network_type:
            network_type = [elem.replace('\r', '').replace(':', '') for elem in network_type]
        
        #remove elements with incomplete information
        for items in ip_list:
            for sub_elm in items:
                if len(sub_elm) != 2:
                    items.remove(items[items.index(sub_elm)])

        for idx in range(0, len(network_type)):
            self.net_dict[network_type[idx]] = dict(ip_list[idx])
        '''
        # print(self.net_dict)
    
    def getGateway11(self):
        """
            Retrieves the gateway value of the Wireless LAN Adapter Wi-Fi connection.
            Argument(s): self
            Returns: gateway value of Wireless LAN Adapter Wi-Fi connection.
        """
        return self.ip
        '''
        TYPE = "Wireless LAN adapter Wi-Fi"
        REQ_DATA = "DefaultGateway"
        TYPE_CH = "無線區域網路介面卡 Wi-Fi"
        REQ_DATA_CH = "預設閘道"
        default_gateway = ''
        try:
            if TYPE in self.net_dict.keys():
                default_gateway = self.net_dict[TYPE][REQ_DATA]
            elif TYPE_CH in self.net_dict.keys():
                default_gateway = self.net_dict[TYPE_CH][REQ_DATA_CH]
            else:
                print("We don't recognize your language.")
        except KeyError:
            sys.stderr.write("Default Gateway does not exist.")
        except:
            sys.stderr.write("An error has occured.")
        return default_gateway
        '''

    def getSubnet11(self):
        """
            Retrieves the subnet mask value of the Wireless LAN Adapter Wi-Fi connection.
            Argument(s): self
            Returns: subnet mask value of Wireless LAN Adapter Wi-Fi connection.
        """
        return self.subnet
        '''
        TYPE = "Wireless LAN adapter Wi-Fi"
        REQ_DATA = "SubnetMask"
        TYPE_CH = "無線區域網路介面卡 Wi-Fi"
        REQ_DATA_CH = "子網路遮罩"
        subnet_mask = '' 
        try:
            if TYPE in self.net_dict.keys():
                subnet_mask = self.net_dict[TYPE][REQ_DATA]
            elif TYPE_CH in self.net_dict.keys():
                subnet_mask = self.net_dict[TYPE_CH][REQ_DATA_CH]
            else:
                print("We don't recognize your language.")
        except KeyError:
            sys.stderr.write("Default Gateway does not exist.")
        except:
            sys.stderr.write("An error has occured.")
        return subnet_mask
        '''
