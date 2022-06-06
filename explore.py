from multiprocess import Process
from nodeData import *
from treelib import Tree, Node
from block import Block
import time
import os
import yaml
class Explore():
    """
    This is used for exploring one specific host. 
    To parallelize the execution between "exploring" and "nmap searching"
    We use subprocess here, which has to be use very carefully.
    """
    def __init__(self):
        # self.process = Process(target=self.exploring, args=())
        self.Data={
            # 'ip': None,
            'OS': None,
            'port': "445",
        }
        path = os.walk("./attack_chain")
        for root, directories, files in path:
            for file in files:
                with open("./attack_chain/"+file, "r") as attack_chain:
                    # print(yaml.load(attack_chain))
                    self.load_block(attack_chain)
                    
                for i in range(len(self.block_chain)):
                    if(not self.match_rule(self.block_chain[i])):
                        self.Data, failed = self.run_class(self.class_chain[i])
                    if failed:
                        break
                # continue
                    
                    
    """ 
            for i in range(len(block_chain)):
                
                if !match_rule(block_chain[i]):
                    Data = user_take_over() # user take over only when lacking of input info, instead of rule mismatch

                Data = run(block_chain[i], Data)

                if !match_rule(block_chain[i]):
                    Data = run_class(class_chain[i], Data)
                if !match_rule(block_chain[i]):
                    output_report()
                    halt()
                
    """
    def match_rule(self, blockname="nmap_scan"):
        # return value: true or false
        block = Block(blockname)
        block.blockInfo()

        for para in block.In: # para means input parameters
            try:
                print(self.Data[para])
            except KeyError:
                print(para + " missing data")
                self.user_takeover(para)
                # break
        
        # if(not eval(block.rule)):
        #     return False

            
        # if rule mismatch, return false
        # compare Data and block, if lacking of input, user take over.
        # after that, if still lack of input, return false
        # return false means we won't use this block, but use other blocks with run_class


    def user_takeover(self, lack_input):
        # while(input("input missing")):
        #     None
        # exec("self."+input+" = usr_in")
        # we need to rebuild checkLanHost, it seems like AsyncScan make EOFError keeps happening
        # Find the target host, then we call explore.py, I think the problem would be solved
        exec("self."+lack_input+" = input('Please input missing parameter(" +lack_input +"):')")
        


    def run_class(self, Class):
        None
    def load_block(self, attack_chain):
        atk_chain = yaml.load(attack_chain, Loader=yaml.SafeLoader)
        self.class_chain, self.block_chain= atk_chain["class_chain"], atk_chain["block_chain"]

    def exploring(self):
        print("\n\n\nhalting for 5 sec.\ndo_something........\n\n\n")
        time.sleep(5)
        
        tree = Tree()
        # root_data = NodeData()
        # tree.create_node(identifier='root_nmapScan',data=root_data)
        # print("tree show:", tree.show())
        # print("tree depth:", tree.depth())
        print("done exploring!")

    # def start(self):
    #     self.process.start()
        
    # def kill(self):
    #     self.process.kill()
