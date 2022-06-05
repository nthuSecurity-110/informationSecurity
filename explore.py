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
        self.process = Process(target=self.exploring, args=())
        self.Data={
            'ip': None,
            'OS': None
        }
        path = os.walk("./attack_chain")
        for root, directories, files in path:
            for file in files:
                with open("./attack_chain/"+file, "r") as attack_chain:
                    # print(yaml.load(attack_chain))
                    self.class_chain, self.block_chain = self.load_block(attack_chain)
                    # print(self.class_chain, self.block_chain)
                for i in range(len(self.block_chain)):
                #     if(self.match_rule(self.block_chain[i])=="lack"):
                #         Data = self.user_take_over(self.block_chain[i], Data)
                    if(not self.match_rule(self.block_chain[i])):
                        Data, failed = self.run_class(self.class_chain[i], Data)
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
    def match_rule(self,blockname="nmap_scan"):
        # return value: true or false
        block = Block(blockname)
        
        # if rule mismatch, return false
        # compare Data and block, if lacking of input, user take over.
        # after that, if still lack of input, return false
        # return false means we won't use this block, but use other blocks with run_class
        
        time.sleep(2)
        None


    def load_block(self, attack_chain):
        Data = yaml.load(attack_chain, Loader=yaml.SafeLoader)
        return Data["class_chain"], Data["block_chain"]

    def exploring(self):
        print("\n\n\nhalting for 5 sec.\ndo_something........\n\n\n")
        time.sleep(5)
        
        tree = Tree()
        # root_data = NodeData()
        # tree.create_node(identifier='root_nmapScan',data=root_data)
        # print("tree show:", tree.show())
        # print("tree depth:", tree.depth())
        print("done exploring!")

    def start(self):
        self.process.start()
        
    def kill(self):
        self.process.kill()
