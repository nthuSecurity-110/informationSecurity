from netData import *
from netData_linux import *
from utilities import *
from checkLanHost import *
from nodeData import *
import sys

util = Helper()
    
if __name__ == '__main__':
    
    check = CheckLanHost()
    config = NetworkData_Linux()
    check.AllLanHost(config)
    node = NodeData(check.getIP())
    node.createDict()