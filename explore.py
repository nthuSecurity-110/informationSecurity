from sympy import evaluate
from function import Function
from multiprocess import Process
from nodeData import *
from treelib import Tree, Node
from block import Block
import time
import os
import yaml
import nmap

from xmlrpc.client import Boolean, boolean
class Explore():
    """
    This is used for exploring one specific host. 
    To parallelize the execution between "exploring" and "nmap searching"
    We use subprocess here, which has to be use very carefully.
    """
    def __init__(self):
        # self.process = Process(target=self.exploring, args=())
        # nmap get basic info, fill into Data
        
        explored_host = input("Which host you want to explore? (Testing default: 163.32.250.178)\n").strip() # 163.32.250.178
        if explored_host == '':
            explored_host = '163.32.250.178'
        print("START EXPLORING!")

        L = os.popen(f"sudo nmap -sS -F -O -T4 {explored_host} | grep '/tcp\|/udp'").read().split('\n')
        # processing nmap output
        p = [item.split('/')[0] for item in L if item.split('/')[0]!='']
        l = [item.split('/')[1] for item in L if item.split('/')[0]!='']
        s = [item.split('  ')[-1] for item in l]

        self.Data={
            'IP': explored_host,
            'Service': s,
            'OS': None,
            'Port': p,
            'Apache': None,
        }
        # print(self.Data)

    def compare_version(self, v1, v2):
        '''
        source from GeeksforGeeks
        '''
        arr1 = v1.split(".")
        arr2 = v2.split(".")
        n = len(arr1)
        m = len(arr2)
        
        arr1 = [int(i) for i in arr1]
        arr2 = [int(i) for i in arr2]
    
        if n>m:
            for i in range(m, n):
                arr2.append(0)
        elif m>n:
            for i in range(n, m):
                arr1.append(0)

        for i in range(len(arr1)):
            if arr1[i]>arr2[i]:
                return 1
            elif arr2[i]>arr1[i]:
                return -1
        return 0

    def get_comparison_result(self, res, op):
            if op == '<':
                if res < 0:
                    return True
                elif res > 0:
                    return False
                else:
                    return False
            elif op == '>':
                if res < 0:
                    return False
                elif res > 0:
                    return True
                else:
                    return False
            elif op == '<=':
                if res < 0:
                    return True
                elif res > 0:
                    return False
                else:
                    return True
            elif op == '>=':
                if res < 0:
                    return False
                elif res > 0:
                    return True
                else:
                    return True
            elif op == '==' or op == '=':
                if res < 0:
                    return False
                elif res > 0:
                    return False
                else:
                    return True
            elif op == '!=':
                if res == 0:
                    return False
                else:
                    return True
            else:   #default
                return False

    def evaluate_condition(self, condition):
        if isinstance(condition, str):
            try:                 
                # case that need to substitute the parameter with exact value store in self.Data
                param = condition.split(" ", 1)[0]
                print("param:", param)
                new_condition = self.Data[param] + condition.split(" ", 1)[1]
                print("condition:"+ new_condition)
                return eval(new_condition)
            except KeyError:
                # the condition that can evalute directly eg.  '1==1'
                return eval(condition)  
            except SyntaxError:
                # it's a comparison of version
                param, op, v2 = condition.split(" ", 2)
                v1 = self.Data[param]
                cmp_result = self.compare_version(v1, v2)
                return self.get_comparison_result(cmp_result, op)
            except:
                # default
                print("condition:", condition, "failed, return false by default")
                return False
        else:
            print("condition in eva_con else:", condition)
            for i, (key,val) in enumerate(condition.items()):
                print(f"key:{key}, val:{val}")
                if isinstance(val, list):
                    result = (key=='and')
                    for item in val:
                        outcome = self.evaluate_condition(item)                
                    
                        if key == 'or':
                            result = (outcome or result)
                        elif key == 'and':
                            result = (outcome and result)
                        else:
                            print("Non-existing key")
                    return result
                else:
                    print("It should be list!")
                    return False

    def match_condition_format(self, block):
        '''
        if condition mismatch, return false
        compare Data and block, if lacking of input, user take over.
        after that, if still lack of input, return false
        return false means we won't use this block, but use other blocks with run_class
        return value: true or false
        '''
        if not block.valid:
            return False

        missing_paras = []

        # check if any parameter is missing
        for para in block.In: # para means input parameters
            try: # if Data doesn't contain para, we give it as None
                self.Data[para]
            except KeyError:
                self.Data[para] = None
            
            if self.Data[para] == None:
                # print(f'missing data "{para}"')
                # self.user_takeover(para)
                missing_paras.append(para)

        # deal with the missing ones (if there are)
        if missing_paras:
            print('There are some missing data.')
            mode = input("Please choose next step. 1 for user take over, 2 for running other class methods.\nNext step: ")
            if mode == '1':
                for para in missing_paras:
                    self.user_takeover(para)
            elif mode == '2':
                return False
            else:
                print("default step: 2")
                return False

        # check condition
        if block.condition == None:
            return True
        else:
            return self.evaluate_condition(block.condition[0])
            '''
            new_condition = block.condition
            for param in block.In:
                if param in block.condition:
                    print("param:", param)
                    new_condition = self.Data[param] + block.condition.split(" ", 1)[1]
                    print("new block condition:"+ new_condition)
            return eval(new_condition)
            '''

    def user_takeover(self, lack_input):
        exec("self.Data['"+lack_input+"'] = input('Please input missing parameter (" + lack_input +"): ')")

    def run_class(self, Class):
        print("enter run_class")
        print("className:", Class)
        files = os.listdir('./block/{classname}'.format(classname=Class))
        for file in files:
            print("file:", file)
            fileName = file.split('.')[0]

            if fileName == '':
                print("Not a valid yml file!")
                break
            else:
                block = Block(Class, fileName)
                block_func = getattr(Function, block.function) # get the required function from block
                func_in = {item:self.Data[item] for item in block.In} # find the function input from Data
                self.Data, match_condition = block_func(func_in, self.Data)

    def load_block(self, attack_chain):
        atk_chain = yaml.load(attack_chain, Loader=yaml.SafeLoader)
        self.class_chain, self.block_chain= atk_chain["class_chain"], atk_chain["block_chain"]

    def exploring(self):
        path = os.walk("./attack_chain")
        for root, directories, files in path:
            for file in files:
                with open("./attack_chain/"+file, "r") as attack_chain:
                    # print(yaml.load(attack_chain))
                    self.load_block(attack_chain)
                    
                for i in range(len(self.block_chain)): # for all blocks in block chain
                    blockname = self.block_chain[i]
                    classname = self.class_chain[i]
                    block = Block(classname, blockname)
                    result = self.match_condition_format(block)
                    if result == True:
                        try:
                            block_func = getattr(Function, block.function) # get the required function from block
                            func_in = {item:self.Data[item] for item in block.In} # find the function input from Data
                            args = block.argument
                            self.Data, match_condition = block_func(func_in, self.Data) #error , args)
                            if match_condition:
                                print("MATCH RULE~~~!!!!\n")
                        except AttributeError: # if block use undefined function, skip to next chain
                            print(f"Function '{block.function}' is not defined, skip to next chain.")
                    elif result == False:
                        self.run_class(self.class_chain[i])
                    else:
                        print('There are some missing data.')
                        mode = input("Please choose next step. 1 for user take over, 2 for running other class methods.\nNext step: ")
                        if mode == '1':
                    	    for para in result:
                                self.user_takeover(para)
                    
                # continue
        
        # time.sleep(5)
        # tree = Tree()
        # root_data = NodeData()
        # tree.create_node(identifier='root_nmapScan',data=root_data)
        # print("tree show:", tree.show())
        # print("tree depth:", tree.depth())
        print("done exploring!")

    # def start(self):
    #     self.process.start()
        
    # def kill(self):
    #     self.process.kill()
"""
src: https://tryhackme.com/room/rrootme#
ans: https://medium.com/@canturkbal/tryhackme-rootme-ctf-walkthrough-915a014a0cf2
php_file: https://github.com/pentestmonkey/php-reverse-shell/blob/master/php-reverse-shell.php
Todo:
1. gobuster (dirb)
2. upload a file
3. nc -lvp 1234
4. get root(skip user.txt)
"""
