import yaml
with open("./block/Initial Access/upload_file.yml", "r") as ymlFile:
    Data = yaml.load(ymlFile ,Loader=yaml.SafeLoader)
    print(Data['file'])