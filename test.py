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

class Error(Exception):
    '''Base class for customized exceptions'''
    pass

class RuleLengthError(Error):
    '''To raise an exception when there is more than one rule in a single yaml file.'''
    pass

def solve(rule):
    if isinstance(rule, str) and type(eval(rule)) == Boolean:
        return eval(rule)
    print("call solve!",rule)
    for i,(key,val) in enumerate(rule.items()):
        print(f"key:{key}, val:{val}")
        if isinstance(val, list):
            result = (key=='and')
            for item in val:
                if isinstance(item, dict):
                    outcome = solve(item)
                else:
                    outcome = eval(item)
                
                if key == 'or':
                    result = (outcome or result)
                elif key == 'and':
                    result = (outcome and result)
                else:
                    print("Non-existing key")
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
        print("F length:", len(F))
        if len(F) > 1:
            raise RuleLengthError
        print("F[0]:", F[0])
        print("======================")
        print(solve(F[0]))
    except TypeError:
        print("I cannot find any rules!")
    except FileNotFoundError:
        print("Please double check the file name!")
    except RuleLengthError:
        print("Please input one rule at a time!")
    except ValueError:
        print("Invalid value!")
    except:
        print("Rule syntax error! Please re-check the .yml file content.")