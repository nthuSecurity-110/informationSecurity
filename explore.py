from multiprocess import Process
from nodeData import *
from treelib import Tree, Node
import time
class Explore():
    """
    This is used for exploring one specific host. 
    To parallelize the execution between "exploring" and "nmap searching"
    We use subprocess here, which has to be use very carefully.
    """
    def __init__(self):
        self.process = Process(target=self.exploring, args=())
    
    def exploring(self):
        print("\n\n\nhalting for 5 sec.\ndo_something........\n\n\n")
        time.sleep(5)
        
        tree = Tree()
        root_data = NodeData()
        tree.create_node(identifier='root_nmapScan',data=root_data)
        # print("tree show:", tree.show())
        # print("tree depth:", tree.depth())
        print("done exploring!")

    def start(self):
        self.process.start()
        
    def kill(self):
        self.process.kill()
