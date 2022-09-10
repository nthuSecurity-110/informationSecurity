from curses.ascii import isdigit
from unittest import result
from sympy import evaluate
from function import Function
from nodeData import *
from block import Block
from termios import tcflush, TCIFLUSH
import sys
import time
import os
import yaml
import nmap
from createMdReport import *

from xmlrpc.client import Boolean, boolean
class Explore():
    """
    This is used for exploring one specific host. 
    To parallelize the execution between "exploring" and "nmap searching"
    We use subprocess here, which has to be used very carefully.
    """
    def __init__(self,myIP):
        # self.process = Process(target=self.exploring, args=())
        # nmap get basic info, fill into Data

        explored_host = input("Which host you want to explore? (ex: 99.83.179.177)\n").strip() # 99.83.179.177
        url = input('Input target url(ex: https://hackmd.io/):\n')

        if explored_host == '':
            explored_host = '99.83.179.177'
        if url == '':
            url = 'https://hackmd.io/'
        
        self.Data={
            'URL': url
        }
        
        print("START EXPLORING!")

        L = os.popen(f"sudo nmap -sS -F -O -T4 {explored_host} | grep '/tcp\|/udp'").read().split('\n')
        # processing nmap output
        p = [item.split('/')[0] for item in L if item.split('/')[0]!='']
        l = [item.split('/')[1] for item in L if item.split('/')[0]!='']
        s = [item.split('  ')[-1] for item in l]
        # self.Data={
        #     'myIP': myIP,
        #     'IP': explored_host,
        #     'Service': s,
        #     'OS': None,
        #     'Port': p,
        #     'Apache': None,
        # }
        self.Data['myIP']= myIP
        self.Data['IP']= explored_host
        self.Data['Service']= s
        self.Data['OS']= None
        self.Data['Port']= p
        self.Data['Apache']= None
        self.selected_chains = []

        #print(f'self.data:\n{self.Data}\n')
        
        print(f'{"*"*15}Begin initial reconnaissance{"*"*15}\n')
        Recon_files = ['nmap_A', 'gobuster']

        for i in range(len(Recon_files)):
            blockname = Recon_files[i]
            if(blockname == 'gobuster' and '80' not in self.Data['Port'] and '443' not in self.Data['Port']):
                continue
            
            tcflush(sys.stdin, TCIFLUSH)
            block = Block('Reconnaissance', blockname)
            block_func = getattr(Function, block.function) # get the required function from block
            func_in = {item:self.Data[item] for item in block.In} # find the function input from Data
            self.Data, match_condition = block_func(func_in, self.Data, block.argument, block.In, block.Out, block.hint)
        print(f'{"*"*15}End initial reconnaissance{"*"*15}\n')
        while(1):
            try:
                mnl_or_auto = int(input('Show suggested chain(1) or manually choose from all chains(2)?\n'))
                if(mnl_or_auto==1 or mnl_or_auto==2):
                    break
            except ValueError:
                mnl_or_auto = int(input('Show suggested chain(1) or manually choose from all chains(2)?\n'))
                continue
        
        if (mnl_or_auto ==1):
            self.show_suggested_chains()
            self.show_selected_chains()
            modify = input("Do you want to modifiy selected chains(y/N)")
            if modify == 'y':
                self.modify_selected_chains()
        elif(mnl_or_auto ==2):
            self.modify_selected_chains()

            # print("Choose the attack chain you want to use from the following table.\n"+'='*30)
            # atk_chain_list = []
            # path = os.walk("./attack_chain")
            # for root, directories, files in path:
            #     for file in files:
            #         atk_chain_list.append(file)
        
            # for i in range(len(atk_chain_list)):
            #     print(f'{i}: {atk_chain_list[i]}')
            # print('='*30)
            # chosen_atk_chain = input("Enter the atk chain number you choose.\nIf choose more than one chains, seperate it with space.\n(ex. 1 2 5)\n")

            # while(1):
            #     try: # filter the invalid atk chain idx (have to be number)
            #         chosen_atk_chain = [ int(x) for x in chosen_atk_chain.split(' ') ]
            #         break
            #     except ValueError:
            #         chosen_atk_chain = input("Enter the atk chain number you choose.\nIf choose more than one chains, seperate it with space.\n(ex. 1 2 5)\n")
            #         continue

            # self.selected_chains = []
            # for idx in chosen_atk_chain:
            #     # filter the invalid idx range and repeated chosen chain
            #     if idx <len(atk_chain_list) and idx>-1 and atk_chain_list[idx] not in self.selected_chains:
            #         self.selected_chains.append(atk_chain_list[idx])
            # print(f'You choose {len(self.selected_chains)} valid atk chain: {self.selected_chains}')

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
                # case of checking if something is in Data(list type) eg. http in Service
                if "in" in condition:
                    element, op, param_list = condition.split(" ")
                    print("check if", element, "is in", self.Data[param_list])
                    return element in self.Data[param_list]
                # case that need to substitute the parameter with exact value store in self.Data eg. Apache == 2.49
                else:
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
        print("\nenter run_class")
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
                result = self.match_condition_format(block)
                if result == True:
                    block_func = getattr(Function, block.function) # get the required function from block
                    func_in = {item:self.Data[item] for item in block.In} # find the function input from Data
                    self.Data, match_condition = block_func(func_in, self.Data, block.argument, block.In, block.Out, block.hint)
                else:
                    continue

    def load_block(self, attack_chain):
        atk_chain = yaml.load(attack_chain, Loader=yaml.SafeLoader)
        self.class_chain, self.block_chain= atk_chain["class_chain"], atk_chain["block_chain"]

    def exploring(self):
        #path = os.walk("./attack_chain")
        #for root, directories, files in path:
        for file in self.selected_chains:
            print("\n"+'*'*20+"Running atk chain:"+file+'*'*20+"\n")
            with open("./attack_chain/"+file, "r") as attack_chain:
                #print(yaml.load(attack_chain))
                self.load_block(attack_chain)
                
            for i in range(len(self.block_chain)): # for all blocks in block chain
                blockname = self.block_chain[i]
                classname = self.class_chain[i]
                # flush input buffer, in case there are any unexpected user input before
                tcflush(sys.stdin, TCIFLUSH)
                block = Block(classname, blockname)
                result = self.match_condition_format(block)
                if result == True:
                    try:
                        block_func = getattr(Function, block.function) # get the required function from block
                        func_in = {item:self.Data[item] for item in block.In} # find the function input from Data
                        self.Data, match_condition = block_func(func_in, self.Data, block.argument, block.In, block.Out, block.hint) 
                        if match_condition:
                            print("MATCH RULE~~~!!!!\n")
                        else:
                            print("FAIL TO GET DESIRED OUTPUT~~~!!!!\n")
                            self.run_class(self.class_chain[i])
                    except AttributeError: # if block use undefined function, skip to next chain
                        print(f"Function '{block.function}' is not defined, skip to next chain.")
                elif result == False:
                    if not self.match_condition_format(block):
                        print("fail to get needed data by run_class, skip")
                        break
                    else:
                        self.run_class(self.class_chain[i])
                else:
                    print('There are some missing data..')
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
        createMD = MdReport(self.Data)
        createMD.createMd()

    # def start(self):
    #     self.process.start()
        
    # def kill(self):
    #     self.process.kill()

        # auto search for suggested chains
    def show_suggested_chains(self):
        print("your condition:", "\nService:", self.Data['Service'], "\nOS:", self.Data['OS'], "\nPort:", self.Data['Port'], "\nApache:", self.Data['Apache'])
        path = os.walk("./attack_chain")
        for root, directories, files in path:
            for file in files:
                with open("./attack_chain/"+file, "r") as attack_chain:
                    atk_chain = yaml.load(attack_chain, Loader=yaml.SafeLoader)
                    print("attack chain", file, "'s tag:", atk_chain["tag"])
                    if atk_chain["tag"] == None:
                        continue
                    if "Service" in atk_chain["tag"].keys():
                        for s1 in atk_chain["tag"]["Service"]:
                            if file in self.selected_chains:
                                break
                            for s2 in self.Data['Service']:
                                if s1 == s2:
                                   self.selected_chains.append(file)
                    if "Port" in atk_chain["tag"].keys():
                        for p1 in atk_chain["tag"]["Port"]:
                            if file in self.selected_chains:
                                break
                            for p2 in self.Data['Port']:
                                if p1 == p2:
                                   self.selected_chains.append(file)
                    if "OS" in atk_chain["tag"].keys():
                        for o1 in atk_chain["tag"]["OS"]:
                            if file in self.selected_chains:
                                break
                            for o2 in self.Data['OS']:
                                if o1 == o2:
                                   self.selected_chains.append(file)
                    if "Apache" in atk_chain["tag"].keys():
                        for a1 in atk_chain["tag"]["Apache"]:
                            if file in self.selected_chains:
                                break
                            for a2 in self.Data['Apache']:
                                if a1 == a2:
                                   self.selected_chains.append(file)
        print("\nsuggested chains:\n", self.selected_chains, sep='\n')
        print(f'{"*"*15}End suggestion{"*"*15}\n')
    
    def show_selected_chains(self):
        print("\nselected chains:", self.selected_chains, sep='\n')

    def modify_selected_chains(self):
        print("type `viewall` to show all attack chains")
        print("type `checkout <chain_name>` to see the detail of a specific chain, chain_name includes '.yml'")
        print("type `search <feature> <value>` to search for attack chain")        
        print("type `add <chain_name>` to add the chain to selected chain list, chain_name includes '.yml'")
        print("or `add <atk_chain_number>` to add the chain to selected chain list\nIf choose more than one chains, seperate it with space.\n(ex. add 1 2 5)")
        print("type `rm <chain_name>` to remove the chain from selected chain list, chain_name includes '.yml'")
        print("type `end` to end modifying selected chain list")

        print("Choose the attack chain you want to use from the following table.\n"+'='*30)
        atk_chain_list = []
        path = os.walk("./attack_chain")
        for root, directories, files in path:
            for file in files:
                atk_chain_list.append(file)
        
        for i in range(len(atk_chain_list)):
            print(f'{i}: {atk_chain_list[i]}')
        print('='*30)

        while(1):
            print(">", end="")
            user_input = input().split(' ')
            if user_input[0] == 'viewall':
                for i in range(len(atk_chain_list)):
                    print(f'{i}: {atk_chain_list[i]}')
                print('='*30)
            elif user_input[0] == 'checkout':
                try:
                    with open("./attack_chain/"+user_input[1], "r") as attack_chain:
                        atk_chain = yaml.load(attack_chain, Loader=yaml.SafeLoader)
                        print(atk_chain)
                except:
                    print("unknown chain name")
            elif user_input[0] == 'search':
                feature, value = user_input[1], user_input[2]
                
                print("result:")
                for file in atk_chain_list:
                    with open("./attack_chain/"+file, "r") as attack_chain:
                        atk_chain = yaml.load(attack_chain, Loader=yaml.SafeLoader)
                        if atk_chain["tag"] == None:
                            continue
                        if feature == "Service" and "Service" in atk_chain["tag"].keys():
                            for s1 in atk_chain["tag"]["Service"]:
                                if s1 == value:
                                    print(file)
                                    print(atk_chain)
                        elif feature == "Port" and "Port" in atk_chain["tag"].keys():
                            for p1 in atk_chain["tag"]["Port"]:
                                if p1 == value:
                                    print(file)
                                    print(atk_chain)
                        elif feature == "OS" and "OS" in atk_chain["tag"].keys():
                            for o1 in atk_chain["tag"]["OS"]:
                                if o1 == value:
                                    print(file)
                                    print(atk_chain)
                        elif feature == "Apache" and "Apache" in atk_chain["tag"].keys():
                            for a1 in atk_chain["tag"]["Apache"]:
                                if a1 == value:
                                    print(file)
                                    print(atk_chain)
            elif user_input[0] == 'add':
                try:
                    if isdigit(user_input[1][0]):
                        idxs = user_input[1:]
                        # filter the invalid atk chain idx (have to be number)
                        try:
                            idxs = [ int(x) for x in idxs ]
                        except ValueError:
                            print("invalid index")
                        for idx in idxs:
                            # filter the invalid idx range and repeated chosen chain
                            if idx in range(len(atk_chain_list)) and atk_chain_list[idx] not in self.selected_chains:
                                self.selected_chains.append(atk_chain_list[idx])
                    else:
                        chain_name = user_input[1]
                        if chain_name in atk_chain_list and chain_name not in self.selected_chains:
                            self.selected_chains.append(chain_name)
                        else:
                            print("invalid chain name or chain already selected")
                except:
                    print("invalied command")
                self.show_selected_chains()
            elif user_input[0] == 'rm':
                chain_name = user_input[1]
                if chain_name in self.selected_chains:
                    self.selected_chains.remove(chain_name)
                else:
                    print("unknown chain name")
                self.show_selected_chains()
            elif user_input[0] == 'end':
                self.show_selected_chains()
                break
            else:
                print("invalid command")
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