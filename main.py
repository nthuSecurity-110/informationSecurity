from netData import *
from netData_linux import *
from utilities import *
from checkLanHost import *
from nodeData import *
from explore import *
import sys

util = Helper()
    
if __name__ == '__main__':
    
    check = CheckLanHost()
    
    config = NetworkData_Linux()
    mode = Helper().choose_mode()
    if mode == 2:
        check.AllLanHost(config)
    explore = Explore(config.getGateway11())
    explore.exploring()

    node = NodeData(check.getIP())
    node.createDict()