from this import d
import yaml

class NodeData():
    """
    Put rule in yaml format, and add some operation
    """
    def __init__(self, ip_list):
        self.ip = ip_list
        self.ip_yaml = []
        self.list_of_dict = []
        print("self ip:", self.ip)

    def ipToList(self):
        for ip in self.ip:
            self.ip_yaml.append({'ip': ip})

    def getIP(self):
        return self.ip_yaml
    
    def commandToList(self):
        self.cmd_yaml = []

    def contentDict(self):
        self.ipToList()
        content = {'ip': '', 'command': ''}
        for i in range(len(self.ip)):
            content['ip'] = self.ip[i]
            content['command'] = 'ins'
            print("content:", content)
            self.list_of_dict.append(content)

    def processData(self):
        self.contentDict()
        

    def createDict(self):
        self.contentDict()
        self.yaml_format = [{'rule': 'nodeA',
                                'AAA': [it for it in self.list_of_dict]
                            }]
        print(self.yaml_format)
        
    def generateYaml(self):
        with open('data.yaml', 'w') as f:
            data = yaml.dump(self.data, f)