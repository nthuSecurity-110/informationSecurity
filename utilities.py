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
        self.string = "hello"

    def decimalToBinary(self, n):
        """
        """
        return bin(n).replace("0b", "")

    def calculateMask(self, subnet_mask):
        """
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