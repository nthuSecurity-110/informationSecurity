from function import Function
from multiprocess import Process
from nodeData import *
from treelib import Tree, Node
from block import Block
import time
import os
import yaml
import nmap
class Explore():
    """
    This is used for exploring one specific host. 
    To parallelize the execution between "exploring" and "nmap searching"
    We use subprocess here, which has to be use very carefully.
    """
    def __init__(self):
        # self.process = Process(target=self.exploring, args=())
        # nmap get basic info, fill into Data
        
        explored_host = input("Which host you want to explore?(for testing default: 163.32.250.178)\n") # 163.32.250.178
        if explored_host == '':
            explored_host = '163.32.250.178'
        print("START EXPLORING!")

        L = os.popen("sudo nmap -sS -F -O -T4 140.114.206.90 | grep '/tcp\|/udp'").read().split('\n')
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
                    
    def match_condition_format(self, block):
        # return value: true or false
        if not block.valid:
            return False

        for para in block.In: # para means input parameters
            try: # if Data doesn't contain para, we give it as None
                self.Data[para]
            except KeyError:
                self.Data[para] = None
            
            if self.Data[para]==None:
                print(f'missing data "{para}"')
                self.user_takeover(para)
        
        if block.condition == "" and not eval(block.condition):
            return False
        else:
            return True

            
        # if condition mismatch, return false
        # compare Data and block, if lacking of input, user take over.
        # after that, if still lack of input, return false
        # return false means we won't use this block, but use other blocks with run_class


    def user_takeover(self, lack_input):
        exec("self.Data['"+lack_input+"'] = input('Please input missing parameter(" +lack_input +"):')")
        


    def run_class(self, Class):
        # problem 2: if condition mismatch, try other block in class. 假設block失敗，到class去掃的部分，我也都還沒寫(可能要等class那邊先出來?)
        None
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
                    block = Block(blockname)
                    if(self.match_condition_format(block)):
                        try:
                            block_func = getattr(Function, block.function) # get the required function from block
                            func_in = {item:self.Data[item] for item in block.In} # find the function input from Data
                            self.Data, match_condition = block_func(func_in, self.Data)
                            if match_condition:
                                print("MATCH RULE~~~!!!!\n")
                        except AttributeError: # if block use undefined function, skip to next chain
                            print(f"Function '{block.function}' is not defined, skip to next chain.")
                    else:
                        self.run_class(self.class_chain[i])
                    
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
