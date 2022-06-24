import yaml

class Block():
    def __init__(self, filename):
        try:
            with open("./block/" + filename+ ".yml", "r") as condition:
                Data = yaml.load(condition,Loader=yaml.SafeLoader)
                self.function = Data['function']
                self.condition = Data['condition'] #from yaml file
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
        print("condition:",self.condition)
        print("In:",self.In)
        print("Out:",self.Out)
        print("=====================")
