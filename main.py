from netData import *
from netData_linux import NetworkData_Linux
from utilities import Helper
import sys




util = Helper()



    
if __name__ == '__main__':
    # import different module for testing
    # it's just for convenient, 
    test_or_not=input("test or not(y/n)?")
    if test_or_not =='n':
        from checkLanHost import AllLanHost
    else:
        from test import AllLanHost
    
    if test_or_not=='n':
        user_os = util.getOS()
        if user_os == "win":
            config = NetworkData()
        elif user_os == "linux": 
            config = NetworkData_Linux()
        else:
            sys.stderr(user_os)
        AllLanHost(config,user_os)
    else:
        AllLanHost('win')