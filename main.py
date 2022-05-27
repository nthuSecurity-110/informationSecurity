from netData import *
from netData_linux import *
from utilities import *
from checkLanHost import *
import sys

util = Helper()
    
if __name__ == '__main__':
    
    check = CheckLanHost()
    config = NetworkData_Linux()
    check.AllLanHost(config)