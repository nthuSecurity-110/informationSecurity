import yaml
from pathlib import Path

# with open("./block/Initial Access/upload_file.yml", "r") as ymlFile:
#     Data = yaml.load(ymlFile ,Loader=yaml.SafeLoader)
#     print(Data['file'])

with open("folder/test2.yml", "r") as ymlFile:
    Data = yaml.load(ymlFile ,Loader=yaml.SafeLoader)
    # print(Data)

with open("folder/new.yml", "w") as filee:
    conditions = [{'or': ['Apache>3.1', {'and': ['80 in port', {'or': ['a==b', 'b==c']}]}]}]
    hints = ["hi there~", "here is a hint.", "good luck! XD"]
    documents = yaml.dump(conditions, filee)


p = Path("folder/new.yml")
# p.rename(p.with_suffix('.txt'))
# f = open("folder/new.txt", "r")

# print(f.readlines())