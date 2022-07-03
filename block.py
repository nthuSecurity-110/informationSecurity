import yaml

class Block():
    def __init__(self, classname, filename):
        try:
            with open("./block/" + classname + "/" + filename+ ".yml", "r") as ymlFile:
                Data = yaml.load(ymlFile ,Loader=yaml.SafeLoader)
                print("data:", Data)
                self.function = Data['function']
                self.condition = Data['condition'] #from yaml file
                self.description = Data['description']
                self.argument = Data['argument']
                self.In = Data['In']
                self.Out = Data['Out']
                self.blockInfo()
                self.valid = True
        except FileNotFoundError:
            print(f"Block '{filename}' does not exist. Skipping it!")
            self.valid = False


    def blockInfo(self):
        print("="*10 + "Block Info" + "="*10)
        print("description:", self.description)
        print("function:", self.function)
        print("condition:", self.condition)
        print("argument:", self.argument)
        print("In:", self.In)
        print("Out:", self.Out)
        print("="*30)
