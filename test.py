import os
import yaml
# path = os.walk("./attack_chain")
# for root, directories, files in path:
#     for file in files:
#         with open("./attack_chain/"+file, "r") as attack_chain:
#             # print(yaml.load(attack_chain))
#             atk_chain = yaml.load(attack_chain, Loader=yaml.SafeLoader)
#             class_chain, block_chain= atk_chain["class_chain"], atk_chain["block_chain"]

def solve(rule):
    e = 1
    if isinstance(rule, str) and type(eval(rule)) == type(True):
        return eval(rule)
    print("call solve!",rule)
    if e:
        for i,(key,val) in enumerate(rule.items()):
            print(f"key:{key}, val:{val}")
            # print(type(val))
            if isinstance(val, list):
                result = (key=='or')
                for item in val:
                    if isinstance(item, dict):
                        outcome = solve(item)
                    else:
                        outcome = eval(item)
                    
                    if key == 'or':
                        result = (outcome or result)
                    elif key =='and':
                        result = (outcome and result)
                    else:
                        print("Non-exist key")
                return result
            else:
                print("It should be list!")


    else:
        print(rule)
    




# path = os.walk("./folder")
# for root, directories, files in path:
#     for file in files:
#         with open("./folder/"+file, "r") as testfile:
#             F= yaml.load(testfile, Loader=yaml.SafeLoader)
#             F = solve(F)

with open("./folder/"+"test.yml", "r") as testfile:
    F= yaml.load(testfile, Loader=yaml.SafeLoader)
    print(solve(F[0]))