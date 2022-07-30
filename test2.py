import yaml
from pathlib import Path
import ast

# with open("./block/Initial Access/upload_file.yml", "r") as ymlFile:
#     Data = yaml.load(ymlFile ,Loader=yaml.SafeLoader)
#     print(Data['file'])

# str = '(Apache > 3.1 || 1==1)'

open_list = ["[","{","("]
close_list = ["]","}",")"]

def check(myStr):
    stack = []
    for i in myStr:
        if i in open_list:
            stack.append(i)
        elif i in close_list:
            pos = close_list.index(i)
            if ((len(stack) > 0) and
                (open_list[pos] == stack[len(stack)-1])):
                stack.pop()
            else:
                return False
    if len(stack) == 0:
        return True
    else:
        return False

def convert_condition(c):
    if check(c):
        d = ""
        lst = []
        length = len(c)
        i = 0
        tmp = ''
        pair = 0
        while i < length: 
            if c[i] == '(':
                d += '{'
                i += 1
            elif c[i] == '|' and c[i+1] == '|':
                lst.append(tmp.strip())
                tmp = ''
                d += "'or': ["
                pair += 1
                d += "'"
                d += lst.pop()
                d += "' , "
                i += 2
            elif c[i] == '&' and c[i+1] == '&':
                lst.append(tmp.strip())
                tmp = ''
                d += "'and': ["
                pair += 1
                d += "'"
                d += lst.pop()
                d += "' , "
                i += 2
            elif c[i] == ')':
                if tmp != '':
                    lst.append(tmp.strip())
                    tmp = ''
                if len(lst) > 0:
                    d += "'"
                    d += lst.pop()
                    d += "'"
                    if pair > 0:
                        d += ']}'
                    else:
                        d += '}'
                else:
                    if pair > 0:
                        d += ']}'
                    else:
                        d += '}'
                i += 1
            else:
                tmp += c[i]
                i += 1
        res = '[' + d + ']'
        return res
    else:
        return "Cannot solve"

# print(convert_condition(str))


with open("attack_chain/rootme.yml", "r") as ymlFile:
    content = ymlFile.readlines()
tmp_class = content[0][13:].strip()
tmp_block = content[1][13:].strip()
class_chain = ''
for c in tmp_class:
    if c == '[':
        class_chain += "['"
    elif c == ']':
        class_chain += "']"
    elif c == ',':
        class_chain += "', '"
    else:
        class_chain += c
block_chain = ''
for b in tmp_block:
    if b == '[':
        block_chain += "['"
    elif b == ']':
        block_chain += "']"
    elif b == ',':
        block_chain += "', '"
    else:
        block_chain += b
class_chain = ast.literal_eval(class_chain)
block_chain = ast.literal_eval(block_chain)
# class_chain.append(self.folder)
# block_chain.append(self.file_name)
class_chain.append('rootme')
block_chain.append('rootme')
class_chain = [elm.strip() for elm in class_chain]
block_chain = [elm.strip() for elm in block_chain]
print(class_chain)
print(block_chain)
class_str = str(class_chain).replace("'", "")
block_str = str(block_chain).replace("'", "")
res = class_str + '\n' + block_str
attack_path = 'attack_chain/rootme.txt'
with open(attack_path, 'w') as file:
    file.writelines(res)
p = Path(attack_path)
p.rename(p.with_suffix('.yml'))
