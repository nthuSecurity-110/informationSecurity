import yaml
import os
from pathlib import Path

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

    def prompt_contents(self):
        ask_user = "You will be creating the file " + self.file_name + ".yml under the folder " + self.folder + ". Enter 'Y' if you would like to continue. "
        self.is_agree = input(ask_user)
        if self.is_agree.upper() == 'Y':
            view_format = input("The rules inside the yaml file have a few formats that you need to follow. Would you like to view the format? (y/n): ")
            if view_format.upper() == 'Y':
                print('''
                Description: a brief introduction to the block.\n
                Function: the name of the function to use.\n
                Argument: The parameter that will be used when using the function, eg. -V of "nmap -V".\n
                In: Which inputs are required to execute this block.
                if there are multiple, separate them with commas. Put in square brackets at the end.\n
                Out: Expected information (output).
                if there are multiple, separate them with commas. Put in square brackets at the end.\n
                Condition: The conditions required to execute the function.\n
                Hint: The hints that might help you.\n
                ''')
            self.description = input("Please enter a brief description about the block: ")
            while self.description == '':
                self.description = input("Description cannot be empty! Prompting for an input: ")
            self.function = input("Please enter the function name: ")
            while self.function == '':
                self.function = input("Function cannot be empty! Prompting for an input: ")
            self.argument_items = input("Please enter the parameters, separated by a whitespace: ")
            self.input_items = input("Please enter the expected input(s), separated by a comma ',': ")
            self.output_items = input("Please enter the expected output(s), separated by a comma ',': ")
            self.condition = input("Please enter the condition if any: ")
            self.hint = input("Please enter a hint if any: ")
        else:
            print("Aborting...")

    def prompt_input(self):
        try:
            self.folder = input("The folder will automatically be created under the 'block' folder.\nPlease enter the name of the folder that you want the file to be located at: ")
            path_folder = 'block/' + self.folder
            self.is_folder = os.path.isdir(path_folder)
            if self.is_folder == False:
                self.create_folder = input("Folder does not exist! Create a new folder? (y/n) ")
                if self.create_folder.upper() == 'Y':
                    new_path = 'block/' + self.folder
                    os.mkdir(new_path)
                    self.file_name = input("Please enter the file name (yaml file): ")
                    self.path_file = new_path + '/' + self.file_name
                    self.prompt_contents()
                else:
                    print("Can't continue, sorry!")
            else:
                self.file_name = input("Please enter the file name (yaml file): ")
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
        self.argument = self.argument_items.split(' ')
        self.argument = [] if self.argument[0] == '' else self.argument
        # print("arguments:", self.argument)
        tmp_input = self.input_items.split(',')
        tmp_input = [] if tmp_input[0] == '' else tmp_input
        for items in tmp_input:
            self.input.append(items.strip())
        # print("input:", self.input)
        tmp_output = self.output_items.split(',')
        tmp_output = [] if tmp_output[0] == '' else tmp_output
        for items in tmp_output:
            self.output.append(items.strip())
        # print("output:", self.output)
    
    def create_yaml(self):
        self.dict[0] = "description: " + self.description + '\n'
        self.dict[1] = "function: " + self.function + '\n'
        self.dict[2] = "argument: " + str(self.argument) + '\n'
        self.dict[3] = "In: " + str(self.input) + '\n'
        self.dict[4] = "condition: " + self.condition + '\n'
        self.dict[5] = "Out: " + str(self.output) + '\n'
        self.dict[6] = "hint: " + self.hint + '\n'.replace(" ", ' ' + self.hint)
        # print("selfdict:", self.dict)

    def write_file(self):
        self.prompt_input()
        if self.is_agree.upper() == 'Y' and self.create_folder.upper() == 'Y' and self.is_overwrite.upper() == 'Y':
            self.handle_input()
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