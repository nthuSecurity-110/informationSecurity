from netData import *
from netData_linux import *
from utilities import *
import sys

util = Helper()
    
if __name__ == '__main__':
    # import different module for testing
    # it's just for convenience. 
    test_or_not=input("test or not(y/n)? ")
    user_os = util.getOS()
    if test_or_not =='n':
        from checkLanHost import *
    else:
        from test import *
    
    if test_or_not=='n':
        check = CheckLanHost(user_os)
        if user_os == "win":
            config = NetworkData()
        elif user_os == "linux": 
            config = NetworkData_Linux()
        else:
            sys.stderr(user_os)
        check.AllLanHost(config)
    else:
        tst = Test()
        tst.AllLanHostTest('win', user_os)