import os
from xmlrpc.client import Boolean, boolean
from iniconfig import ParseError
import yaml
# path = os.walk("./attack_chain")
# for root, directories, files in path:
#     for file in files:
#         with open("./attack_chain/"+file, "r") as attack_chain:
#             # print(yaml.load(attack_chain))
#             atk_chain = yaml.load(attack_chain, Loader=yaml.SafeLoader)
#             class_chain, block_chain= atk_chain["class_chain"], atk_chain["block_chain"]

def solve(rule):
    # print("typeevalrule:", type(eval(rule)))
    # print("typeTrue:", type(True))
    if isinstance(rule, str) and type(eval(rule)) == Boolean:
        return eval(rule)
    print("call solve!",rule)
    for i,(key,val) in enumerate(rule.items()):
        print(f"key:{key}, val:{val}")
        # print(type(val))
        if isinstance(val, list):
            result = (key=='and')
            for item in val:
                # print("items:", item)
                if isinstance(item, dict):
                    outcome = solve(item)
                else:
                    # print("inn")
                    outcome = eval(item)
                    # print("outcomee:", outcome)
                
                if key == 'or':
                    # print("result1bef:", result)
                    result = (outcome or result)
                    # print("outcome1:", outcome)
                    # print("result1:", result)
                elif key =='and':
                    # print("result2bef:", result)
                    result = (outcome and result)
                    # print("outcome2:", outcome)
                    # print("result2:", result)
                else:
                    print("Non-exist key")
            return result
        else:
            print("It should be list!")
    
# path = os.walk("./folder")
# for root, directories, files in path:
#     for file in files:
#         with open("./folder/"+file, "r") as testfile:
#             F= yaml.load(testfile, Loader=yaml.SafeLoader)
#             F = solve(F)

with open("./folder/"+"test.yml", "r") as testfile:
    try:
        F= yaml.load(testfile, Loader=yaml.SafeLoader)
        if len(F) > 1:
            raise ParseError #problem: calls TypeError instead
        print("F:", len(F))
        print("F[0]:", F[0])
        print("======================")
        print(solve(F[0]))
    except TypeError:
        print("I cannot find any rules!")
    except FileNotFoundError:
        print("Please double check the file name!")
    except ParseError:
        print("Please input one rule at a time!")
    except:
        print("Rule syntax error! Please re-check the .yml file content.")