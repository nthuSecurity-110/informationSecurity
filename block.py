import yaml

class Block():
    def __init__(self, filename):
        with open("./block/" + filename + ".yml", "r") as rule:
            Data = yaml.load(rule,Loader=yaml.SafeLoader)
            self.function = Data['function']
            self.rule = Data['rule'] #from yaml file
            self.description = Data['description']
            self.In = Data['In']
            self.Out = Data['Out']
            self.blockInfo()
            
    def blockInfo(self):
        print("function",self.function)
        print("rule",self.rule)
        print("description",self.description)
        print("In",self.In)
        print("Out",self.Out)
