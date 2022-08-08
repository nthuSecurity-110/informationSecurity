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
        None

    def choose_mode(self): # Choose mode 1 will skip nmap discovery LAN. Default mode is 2.
        mode = input("Choose the mode.\n1: a specific target was known.\n2: search for a target!\n3: modify attack chain (create a rule)\n4: insert an existing block.\nMode: ")
        if mode in ['1', '2', '3', '4']:
            return int(mode)
        else:
            print("Default mode: 1")
            return 1

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

            