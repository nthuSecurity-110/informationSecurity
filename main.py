from netData import *
from netData_linux import NetworkData_Linux
from utilities import Helper
from checkLanHost import LanHost
import sys

util = Helper()



    
if __name__ == '__main__':
    user_os = util.getOS()
    if user_os == "win":
        config = NetworkData()
    elif user_os == "linux": 
        config = NetworkData_Linux()
    else:
        sys.stderr(user_os)

    
    
    LanHost(config)
    