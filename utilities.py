import sys

class Helper:
    '''
        This class supports the execution of the program.
        The commands are:
            __init__                        initializes value
            decimalToBinary                 converts decimal to binary
            calculate_mask                  calculates the mask of a given subnet mask
    '''
    def __init__(self):
        self.haha="hello"

    def decimalToBinary(self, n):
        """
            Convert decimal to binary.
            Argument(s):
                - self
                - n: a decimal number
            Returns: the corresponding binary of the decimal number.
        """
        return bin(n).replace("0b", "")

    def calculateMask(self, subnet_mask):
        """
            Calculates the mask value of a subnet mask.
            Argument(s):
                - self
                - subnet mask value
            Returns: an integer, the mask value.
        """
        try:
            parse_lst = subnet_mask.split('.')
            tmp = []
            for i in parse_lst:
                tmp.append(self.decimalToBinary(int(i)))
            mask_str = ''.join(tmp)
            return mask_str.count('1')
        except:
            sys.stderr.write("An error has occured.")
    def getOS(self):
        OS=int(input("Please input your OS(1-win, 2-linux)"))
        if OS ==1: 
            return "win"
        elif OS==2:
            return "linux"
        else:
            return "OS not recognized"