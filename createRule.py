import yaml
import os
import ast
import re
from pathlib import Path

invalid_chars = re.compile("#% &{}\<>*?/ $!'\":@+`|=")

class CreateRule():
    def __init__(self):
        self.description = ''
        self.function = ''
        self.argument = []
        self.input = []
        self.output = []
        self.condition = ''
        self.hint = ''
        self.dict = ["description: None\n", "function: None\n", "argument: []\n", "In: []\n", "condition: \n", "Out: []\n", "hint: \n"]
        self.create_folder = 'Y'
        self.is_overwrite = 'Y'
        self.is_agree = 'N'
        self.attack_path = ''
        self.overwrite = False

    def prompt_contents(self):
        ask_user = "File: " + self.file_name + "\nFolder: " + self.folder + "\nVerify? (y/n): "
        self.is_agree = input(ask_user)
        if self.is_agree.upper() == 'Y':
            view_format = input("View format? (y/n): ")
            if view_format.upper() == 'Y':
                print('''
                Description: a brief introduction to the block.\n
                Function: the name of the function to use.\n
                Argument: The parameter that will be used when using the function, eg. -V of "nmap -V".
                If there are anything that needs the user's input, put them in between brackets '<>'.\n
                In: Which inputs are required to execute this block.
                if there are multiple, separate them with commas. Put in square brackets at the end.\n
                Out: Expected information (output).
                if there are multiple, separate them with commas. Put in square brackets at the end.\n
                Condition: The conditions required to execute the function.
                It should follow the pyyaml rule. (e.g. (Apache > 3.1 || (80 in port && (a == b || b == c))))\n
                Hint: The hints that might help you.
                ''')
            self.description = input("Description: ")
            while self.description == '':
                self.description = input("Description cannot be empty: ")
            self.function = input("Function: ")
            while self.function == '':
                self.function = input("Function cannot be empty: ")
            self.argument_items = input("Arguments: ")
            self.input_items = input("Input(s): ")
            self.output_items = input("Output(s): ")
            self.condition = input("Condition: ")
            print("Hint: (type '-' to end the input)\nNote:\n1. When inserting an executable command, type '[EXE]' before the command.\n2. If there is a user's input in the command, wrap it with '{}'")
            hint_lst = []
            inp = ''
            while True:
                inp = input()
                if inp == '-':
                    print("Done receiving output.")
                    break
                else:
                    hint_lst.append(inp)
            self.hint = hint_lst
        else:
            print("Aborting...")

    def prompt_input(self):
        try:
            self.folder = input("The folder will automatically be created under the 'block' folder.\nFolder name: ")
            if self.folder == '':
                self.folder = 'Default'
            path_folder = 'block/' + self.folder
            self.is_folder = os.path.isdir(path_folder)
            if self.is_folder == False:
                self.create_folder = input("Folder does not exist! Create a new folder? (y/n) ")
                if self.create_folder.upper() == 'Y':
                    new_path = 'block/' + self.folder
                    os.mkdir(new_path)
                    self.file_name = input("Block file name: ")
                    while self.file_name == '':
                        self.file_name = input("File name cannot be empty: ")
                    self.path_file = new_path + '/' + self.file_name
                    self.prompt_contents()
                else:
                    print("Can't continue, sorry!")
            else:
                self.file_name = input("Block file name: ")
                while self.file_name == '':
                    self.file_name = input("File name cannot be empty: ")
                path_file = 'block/' + self.folder + '/' + self.file_name + '.yml'
                self.is_file = os.path.isfile(path_file)
                if self.is_file == True:
                    self.is_overwrite = input("File exists! Overwrite? (y/n) ")
                    if self.is_overwrite.upper() == 'Y':
                        self.prompt_contents()
                    else:
                        print("Aborting")
                else:
                    self.prompt_contents()
        except FileNotFoundError:
            print("sth wrong!")

    def handle_input(self):
        self.condition = self.convert_condition(self.condition)
        if self.condition == 'invalid':
            return 1
        else:
            self.argument = self.argument_items.split(' ')
            self.argument = [] if self.argument[0] == '' else self.argument
            tmp_input = self.input_items.split(',')
            tmp_input = [] if tmp_input[0] == '' else tmp_input
            for items in tmp_input:
                self.input.append(items.strip())
            tmp_output = self.output_items.split(',')
            tmp_output = [] if tmp_output[0] == '' else tmp_output
            for items in tmp_output:
                self.output.append(items.strip())
            self.condition = ast.literal_eval(self.condition)
            self.condition = self.handle_conds(self.condition)
            self.hint = self.handle_hints(self.hint)
            return 0
    
    def create_yaml(self):
        self.dict[0] = "description: " + self.description + '\n'
        self.dict[1] = "function: " + self.function + '\n'
        self.dict[2] = "argument: " + str(self.argument) + '\n'
        self.dict[3] = "In: " + str(self.input) + '\n'
        self.dict[4] = "condition:\n" + self.condition
        self.dict[5] = "Out: " + str(self.output) + '\n'
        self.dict[6] = "hint:\n" + self.hint + '\n'.replace(" ", ' ' + self.hint)
        # print("selfdict:", self.dict)

    def check_parentheses(self, myStr):
        open_list = ["[","{","("]
        close_list = ["]","}",")"]
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

    def convert_condition(self, c):
        if self.check_parentheses(c):
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
            return "invalid"

    def handle_conds(self, c):
        with open("dumps/tmp_c.yml", "w") as ymlFile:
            documents = yaml.dump(c, ymlFile)
        p = Path("dumps/tmp_c.yml")
        p.rename(p.with_suffix('.txt'))
        f = open("dumps/tmp_c.txt", "r")
        cond_lst = (f.readlines())
        self.cond_str = ''.join(cond_lst)
        return self.cond_str

    def handle_hints(self, h):
        with open("dumps/tmp_h.yml", "w") as ymlFile:
            documents = yaml.dump(h, ymlFile)
        p = Path("dumps/tmp_h.yml")
        p.rename(p.with_suffix('.txt'))
        f = open("dumps/tmp_h.txt", "r")
        hints_lst = (f.readlines())
        self.hints_str = ''.join(hints_lst)
        return self.hints_str

    def append_attack_chain(self):
        try:
            if self.overwrite == True:
                class_chain = []
                block_chain = []
                class_chain.append(self.folder)
                block_chain.append(self.file_name)
                class_chain = [elm.strip() for elm in class_chain]
                block_chain = [elm.strip() for elm in block_chain]
                class_str = str(class_chain).replace("'", "")
                block_str = str(block_chain).replace("'", "")
                res = "class_chain: " + class_str + '\n' + "block_chain: " + block_str
                attack_path = self.attack_path + '.txt'
                with open(attack_path, 'w') as file:
                    file.writelines(res)
                p = Path(attack_path)
                p.rename(p.with_suffix('.yml'))
                self.overwrite = False
            else:
                with open(self.attack_path + '.yml', "r") as ymlFile:
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
                class_chain.append(self.folder)
                block_chain.append(self.file_name)
                class_chain = [elm.strip() for elm in class_chain]
                block_chain = [elm.strip() for elm in block_chain]
                class_str = str(class_chain).replace("'", "")
                block_str = str(block_chain).replace("'", "")
                res = "class_chain: " + class_str + '\n' + "block_chain: " + block_str
                attack_path = self.attack_path + '.txt'
                with open(attack_path, 'w') as file:
                    file.writelines(res)
                p = Path(attack_path)
                p.rename(p.with_suffix('.yml'))
        except FileNotFoundError:
            print("Attack chain does not exist!")

    def write_file(self):
        self.prompt_input()
        if self.is_agree.upper() == 'Y' and self.create_folder.upper() == 'Y' and self.is_overwrite.upper() == 'Y':
            if self.handle_input() == 1:
                print("Condition invalid!")
            else:
                self.create_yaml()
                if self.is_folder == False:
                    path = self.path_file + '.txt'
                    yml_path = self.path_file + '.yml'
                else:
                    path = 'block/' + self.folder + '/' + self.file_name + '.txt'
                    yml_path = 'block/' + self.folder + '/' + self.file_name + '.yml'
                with open(path, 'w') as file:
                    file.writelines(self.dict)
                p = Path(path)
                p.rename(p.with_suffix('.yml'))
                print("Created " + yml_path + "!")
        else:
            print("No file created!")

    def overwrite_ac(self):
        self.overwrite = True
        attack_path_yml = self.attack_path + '.yml'
        f = open(attack_path_yml,"w")
        f.close()
        while True:
            create_block = input("Create block? (y/n) ")
            if create_block.upper() == 'N':
                break
            else:
                self.write_file()
                self.append_attack_chain()
        
    def create_attack_chain(self):
        create_block = 'y'
        fld_name = "backup_attack_chain"
        fld_name = input("Attack chain folder: ")
        is_fld = os.path.isdir(fld_name)
        if is_fld == False:
            create_fold = input("Folder does not exist! Create a new folder? (y/n) ")
            if create_fold.upper() == 'Y':
                os.mkdir(fld_name)
                fl_name = input("Attack chain file name: ")
                while fl_name == '':
                    fl_name = input("File name cannot be empty: ")
                self.attack_path = fld_name + '/' + fl_name
                self.overwrite_ac()
            else:
                print("Cannot continue without folder.")
        else:
            fl_name = input("Attack chain file name: ")
            while fl_name == '':
                fl_name = input("File name cannot be empty: ")
            self.attack_path = fld_name + '/' + fl_name
            attack_path_yml = self.attack_path + '.yml'
            is_fl = os.path.isfile(attack_path_yml)
            if is_fl == True:
                ow_fl = input("File exists! Append (A)/Overwrite (O)/Cancel (C)? ")
                if ow_fl.upper() == 'A':
                    while True:
                        create_block = input("Create block? (y/n) ")
                        if create_block.upper() == 'N':
                            break
                        else:
                            self.write_file()
                            self.append_attack_chain()
                elif ow_fl.upper() == 'O':
                    self.overwrite_ac()
                else:
                    print("Abort mission.")
            else:
                self.overwrite_ac()

    def insert_ac(self):
        print("Where to insert the block?")
        ac_folder = input("Attack chain folder: ")
        ac_file = input("Attack chain file: ")
        self.attack_path = ac_folder + '/' + ac_file
        ac_exist = os.path.isfile(self.attack_path + '.yml')
        if ac_exist:
            print("Found attack chain. Fetching block info:")
            print("Where is the block located?:")
            self.folder = input("Block folder: ")
            self.file_name = input("Block file name: ")
            block_exist = os.path.isfile('block/' + self.folder + '/' + self.file_name + '.yml')
            if block_exist:
                self.overwrite = False
                self.append_attack_chain()
                print("Block successfully inserted to " + self.attack_path + '.yml')
            else:
                new_block = input("Block doest not exist!\nCreate a new block? (y/n) ")
                if new_block.upper() == 'Y':
                    self.write_file()
                    self.overwrite = False
                    self.append_attack_chain()
                else:
                    print("Abort mission.")
        else:
            new_ac = input("Attack chain does not exist!\nCreate a new one? (y/n) ")
            if new_ac.upper() == 'Y':
                self.create_attack_chain()
            else:
                print("Abort mission.")
