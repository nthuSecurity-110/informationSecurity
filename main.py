from netData import *
from netData_linux import *
from utilities import *
from checkLanHost import *
from nodeData import *
from explore import *
from createRule import *
import sys

util = Helper()
    
if __name__ == '__main__':
    
    check = CheckLanHost()
    generateRule = CreateRule()
    
    config = NetworkData_Linux()
    mode = Helper().choose_mode()
    if mode == 1:
        explore = Explore(config.getGateway11())
        explore.exploring()
    elif mode == 2:
        check.AllLanHost(config)
    elif mode == 3:
        generateRule.create_attack_chain()
    elif mode == 4:
        generateRule.insert_ac()
    else:
        explore = Explore(config.getGateway11())
        explore.exploring()

    # node = NodeData(check.getIP())
    # node.createDict()