import yaml

class Block():
    def __init__(self, filename):
        try:
            with open("./block/" + filename+ ".yml", "r") as rule:
                Data = yaml.load(rule,Loader=yaml.SafeLoader)
                self.function = Data['function']
                self.rule = Data['rule'] #from yaml file
                self.description = Data['description']
                self.In = Data['In']
                self.Out = Data['Out']
                self.blockInfo()
                self.valid = True
        except FileNotFoundError:
            print(f"Block '{filename}' is not exist. Skip it!")
            self.valid = False

            
    def blockInfo(self):
        print("=====block Info=====")
        print("description:",self.description)
        print("function:",self.function)
        print("rule:",self.rule)
        print("In:",self.In)
        print("Out:",self.Out)
        print("=====================")
