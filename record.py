from os import stat
import matplotlib.pyplot as plt
from datetime import date

class Record():
    """
    This is used for recording the excuted chains and results, 
    for the purpose of report generatiion
    """
    def __init__(self):
        self.target_host_info = {}
        self.chain_record = {}

    def add_target_host_info(self, Data):
        self.target_host_info['IP'] = Data['IP']
        self.target_host_info['URL'] = Data['URL']
        self.target_host_info['Service'] = Data['Service']
        self.target_host_info['OS'] = Data['OS']
        self.target_host_info['Port'] = Data['Port']
        self.target_host_info['Apache'] = Data['Apache']

    def ini_chain_info(self, chain_name, tag=[]):
        new_chain_rec = {}
        #new_chain_rec['chain_name'] = chain_name
        new_chain_rec['block_list'] = {}
        new_chain_rec['status'] = -1
        new_chain_rec['success'] = False
        new_chain_rec['tag'] = []
        if tag != []:
            if 'Service' in tag.keys():
                for s in tag['Service']:
                    new_chain_rec['tag'].append('#' + s)
            if 'Port' in tag.keys():
                for p in tag['Port']:
                    new_chain_rec['tag'].append('#Port' + p)
            if 'OS' in tag.keys():
                for o in tag['OS']:
                    new_chain_rec['tag'].append('#' + o)
            if 'Apache' in tag.keys():
                for a in tag['Apache']:
                    new_chain_rec['tag'].append('#Apache:' + a)
            if 'PT' in tag.keys():
                for pt in tag['PT']:
                    new_chain_rec['tag'].append('#PT' + pt)

        self.chain_record[chain_name] = new_chain_rec
        #print("In record, add new chain:\n", new_chain_rec)
        #print("Record content:", self.chain_record)

    def add_chain_info(self, chain_name, class_name, block_name, block):
        self.chain_record[chain_name]['block_list'][block_name] = self.add_block_info(class_name, block_name, block)

    def add_block_info(self, class_name, block_name, block):
        new_block_rec = dict()
        new_block_rec['class_name'] = class_name
        new_block_rec['block_name'] = block_name
        new_block_rec['description'] = block.description
        new_block_rec['success'] = False
        
        #print("Record content:", self.chain_record)
        return new_block_rec

    def add_chain_mark(self, chain_name, success):
        self.chain_record[chain_name]['success'] = success
        #print("mark atk_chain", chain_name, "'s result", success)
        #print("Record content:", self.chain_record)

    def add_block_mark(self, chain_name, block_name, success):
        self.chain_record[chain_name]['block_list'][block_name]['success'] = success
        #print("mark atk_chain", chain_name, "block:", block_name, "'s result", success)
        #print("Record content:", self.chain_record)

    def add_chain_status(self, chain_name, success):
        status = -1
        if success:
            print("After this excution of attack chain/block, which status do you reach?\nPlease select the highest that meets your condition.\n")
            print("0. not getting anything interesting\n")
            print("1. get information or access data\n")
            print("2. get shell or user credentials\n")
            print("3. get root permission\n")
            
            while(status not in range(4)):
                try:
                    status = int(input(">"))
                except ValueError:
                    pass
        self.chain_record[chain_name]['status'] = status
        #print("Record content:", self.chain_record)

    def add_chain_status_directly(self, chain_name, status):
        self.chain_record[chain_name]['status'] = status

    def gen_report(self):
        print(self.target_host_info)
        print(self.chain_record)
        report_file = open('./report/report_{date}.html'.format(date=date.today().strftime('%Y-%m-%d')), 'w+')
        title = self.gen_head()
        success_rate = self.gen_success_rate()
        target_host_info = self.gen_target_host_info()
        overview = self.gen_overview()
        detail = self.gen_detail()
        foot = self.gen_foot()
        report_file.write(title)
        report_file.write(success_rate)
        report_file.write(target_host_info)        
        report_file.write(overview)
        report_file.write(detail)
        report_file.write(foot)
        report_file.close()
        

    def gen_head(self):
        template = open("report_template.html", "r").read()
        head = template.split("<p>content</p>")[0]
        head = head + "<h2>Date: {date}</h3>".format(date=date.today().strftime('%Y-%m-%d'))
        return head
    
    def gen_success_rate(self):
        labels = ['fail', 'ineffective', 'get data', 'get shell', 'get root']
        count = [0, 0, 0, 0, 0]
        colors = ['#003049', '#7f908f', '#c1121f', '#9d0910', '#780000']
        for k in self.chain_record.keys():
            status = self.chain_record[k]['status']
            idx = status + 1
            count[idx] = count[idx] + 1
        
        fig, ax = plt.subplots()
      
        #remove 0%
        while 0 in count:              
            colors.remove(colors[count.index(0)])
            labels.remove(labels[count.index(0)])
            count.remove(0)
        
        _, _, autotexts = ax.pie(count, labels = labels, colors = colors, autopct='%1.1f%%', pctdistance=0.5)
        for autotext in autotexts:
            autotext.set_color('white')
        plt.axis('equal')
        plt.legend(loc = "best")
        plt.savefig("./report/status_pie_{date}.jpg".format(date=date.today().strftime('%Y-%m-%d')), transparent=True, dpi=300)
        plt.close()

        content = "<h1>Pentest Result</h1>\n"
        content = content + "<img src=\"status_pie_{date}.jpg\">\n\n".format(date=date.today().strftime('%Y-%m-%d'))
        return content

    def gen_target_host_info(self):
        content = "<h1>Target Host Information</h1>\n"
        content = content + "<p>IP: {IP}</p>\n".format(IP=str(self.target_host_info['IP']))
        content = content + "<p>URL: {URL}</p>\n".format(URL=str(self.target_host_info['URL']))
        if isinstance(self.target_host_info['Service'], list):
            content = content + "<p>Service:"
            for s in self.target_host_info['Service']:
                content = content + " " + s
                if self.target_host_info['Service'].index(s) != len(self.target_host_info['Service'])-1:
                    content = content + ","
            content = content + " </p>\n"
        else:
            content = content + "<p>Service: {Service}</p>\n".format(Service=str(self.target_host_info['Service']))
        content = content + "<p>OS: {OS}</p>\n".format(OS=str(self.target_host_info['OS']))        
        if isinstance(self.target_host_info['Port'], list):
            content = content + "<p>Port:"
            for p in self.target_host_info['Port']:
                content = content + " " + p
                if self.target_host_info['Port'].index(p) != len(self.target_host_info['Port'])-1:
                    content = content + ","
            content = content + " </p>\n"
        else:
            content = content + "<p>Port: {Port}</p>\n".format(Port=str(self.target_host_info['Port']))
        content = content + "<p>Apache: {Apache}</p>\n\n".format(Apache=str(self.target_host_info['Apache']))
        return content

    def gen_overview(self):
        content = "<h1>Attack Chain Overview</h1>\n"
        content = content + "<table>\n"\
        "<tr>\n"\
            "<th>chain name</th>\n"\
            "<th>tags</th>\n"\
            "<th>result</th>\n"\
        "</tr>\n"
        for chain_name in self.chain_record.keys():
            content = content + "<tr>\n"
            #chain name
            content = content + "<td>{chain_name}</td>\n".format(chain_name=chain_name)
            #tags
            content = content + "<td>"
            for t in self.chain_record[chain_name]['tag']:
                content = content + t + " "
            content = content + "</td>\n"
            #result
            status_list = ['fail', 'ineffective', 'get data', 'get shell', 'get root']
            content = content + "<td>" +  status_list[self.chain_record[chain_name]['status']+1] +"</td>\n"
            
            content = content + "</tr>\n"
        content = content + "</table>\n"
        return content

    def gen_detail(self):
        content = "<h1>Attack Chain Details</h1>\n"
        content = content + "<table class=\"legend\">\n" + "<tr>\n" + "<td class=\"success\">successful excution</td>\n" + "<td class=\"fail\">failed excution</td>\n" + "</tr>\n" + "</table>\n"
        for chain_name in self.chain_record.keys():
            content = content + "<table>\n"
            num_block = len(self.chain_record[chain_name]['block_list'].keys())
            
            #head row
            content = content + "<tr>\n" + "<th width=\"60%\">{chain_name}</th>\n".format(chain_name=chain_name) + "<th colspan=\"1\">result</th>\n" + "</tr>\n"
            #chain part
            content = content + "<tr>\n" + "<td width=\"60%\">\n" + "<table class=\"chain\">\n"
            
            block_list = self.chain_record[chain_name]['block_list']
            class_suc = ""
            
            #class part
            content = content + "<tr>\n" + "<th class=\"chain\">class</th>\n"           
            for block_name in block_list:
                if block_list[block_name]['success'] == True:
                    class_suc = "success"
                else:
                    class_suc = "fail"
                content = content + "<td class=\"{successful}\">".format(successful=class_suc) + block_list[block_name]['class_name'] + "</td>\n"
            content = content + "</tr>"

            #block row
            content = content + "<tr>\n" + "<th class=\"chain\">block</th>\n"
            for block_name in block_list:
                if block_list[block_name]['success'] == True:
                    class_suc = "success"
                else:
                    class_suc = "fail"
                content = content + "<td class=\"{successful}\">".format(successful=class_suc) + block_name + "</td>\n"
            content = content + "</tr>\n"

            #info row
            content = content + "<tr>\n" + "<th class=\"chain\">info</th>\n"
            for block_name in block_list:
                if block_list[block_name]['success'] == True:
                    class_suc = "success"
                else:
                    class_suc = "fail"
                content = content + "<td class=\"{successful}\">".format(successful=class_suc) + block_list[block_name]['description'] + "</td>\n"
            content = content + "</tr>\n"

            #tag row
            content = content + "<tr>\n" + "<th class=\"chain\">tags</th>\n" +"<td class=\"chain\" colspan=\"{num_block}\">".format(num_block=num_block)
            for t in self.chain_record[chain_name]['tag']:
                content = content + "<span class=\"tag\">" + t + "</span>"
            content = content + "</td>\n" + "</tr>\n" + "</table>\n"

            #result part
            status_list = ['fail', 'ineffective', 'get data', 'get shell', 'get root']
            content = content + "</td>\n" + "<td>{result}</td>".format(result=status_list[self.chain_record[chain_name]['status']+1])
            content = content + "</tr>\n" + "</table>\n"
        return content

    def gen_foot(self):
        template = open("report_template.html", "r").read()
        foot = template.split("<p>content</p>")[1]
        return foot

    def test(self):
        #self.target_host_info = {'IP': '99.83.179.177', 'URL': 'https://hackmd.io/', 'Service': ['http', 'https'], 'OS': None, 'Port': ['80', '443'], 'Apache': None}
        #self.chain_record = {'annie.yml': {'block_list': {'nmap_sC_sV': {'class_name': 'Reconnaissance', 'block_name': 'nmap_sC_sV', 'description': 'Nmap scan to get the useful info', 'success': True}, 'CVE-2020–13160': {'class_name': 'Initial Access', 'block_name': 'CVE-2020–13160', 'description': 'create and send reverse shell by python2', 'success': True}, 'get_bash_by_python': {'class_name': 'Initial Access', 'block_name': 'get_bash_by_python', 'description': 'get bash through python', 'success': True}}, 'status': 2, 'success': True, 'tag': ['#PT01', '#PT05']}, 'postgres_login.yml': {'block_list': {'postgres_login.yml': {'class_name': 'Credential Access', 'block_name': 'postgres_login.yml', 'description': 'scan postgres username and password', 'success': False}}, 'status': -1, 'success': False, 'tag': []}, 'pwntools.yml': {'block_list': {'pwntools.yml': {'class_name': 'Privilege Escalation', 'block_name': 'pwntools.yml', 'description': 'Binary Exploitation', 'success': False}}, 'status': -1, 'success': False, 'tag': []}} 
        #self.target_host_info = {'IP': '10.10.110.108', 'URL': 'http://10.10.110.108/', 'Service': ['ftp', 'ssh'], 'OS': None, 'Port': ['21', '22'], 'Apache': None}
        #self.chain_record = {'annoymous.yml': {'block_list': {'ftp_anonymous_login': {'class_name': 'Credential Access', 'block_name': 'ftp_anonymous_login', 'description': 'login as anonymous to find legitimate username for further exploit', 'success': True}, 'ftp_find_sh': {'class_name': 'Initial Access', 'block_name': 'ftp_find_sh', 'description': 'find script running at remote', 'success': True}, 'reverse_shell_python': {'class_name': 'Initial Access', 'block_name': 'reverse_shell_python', 'description': 'create and upload python reverse shell', 'success': True}, 'get_bash_by_python': {'class_name': 'Initial Access', 'block_name': 'get_bash_by_python', 'description': 'get bash through python', 'success': True}, 'get_root_by_env': {'class_name': 'Privilege Escalation', 'block_name': 'get_root_by_env', 'description': 'get root by using usr/bin/env', 'success': True}}, 'status': 1, 'success': True, 'tag': ['#ftp', '#PT05', '#PT10', '#PT13']}, 'anonforce.yml': {'block_list': {'ftp_anonymous_login': {'class_name': 'Credential Access', 'block_name': 'ftp_anonymous_login', 'description': 'login as anonymous to find legitimate username for further exploit', 'success': True}, 'crack_gpg': {'class_name': 'Initial Access', 'block_name': 'crack_gpg', 'description': 'crack gpg file', 'success': True}, 'crack_hash_by_john': {'class_name': 'Credential Access', 'block_name': 'crack_hash_by_john', 'description': 'crack hash file by john', 'success': True}, 'ssh_login': {'class_name': 'Credential Access', 'block_name': 'ssh_login', 'description': 'login ssh as user', 'success': True}}, 'status': 3, 'success': True, 'tag': ['#ftp', '#PT02', '#PT03', '#PT04', '#PT13']}, 'brooklyn99.yml': {'block_list': {'ftp_anonymous_login': {'class_name': 'Credential Access', 'block_name': 'ftp_anonymous_login', 'description': 'login as anonymous to find legitimate username for further exploit', 'success': True}, 'exploit_user': {'class_name': 'Credential Access', 'block_name': 'exploit_user', 'description': "get the user's password by hydra and login", 'success': False}}, 'status': 2, 'success': False, 'tag': ['#ftp', '#PT03', '#PT04', '#PT05', '#PT13']}}        
        #self.target_host_info = {'IP': '10.10.110.108', 'URL': 'http://10.10.110.108/', 'Service': ['ftp', 'ssh'], 'OS': None, 'Port': ['21', '22'], 'Apache': None}
        #self.chain_record = {'anonforce.yml': {'block_list': {'ftp_anonymous_login': {'class_name': 'Credential Access', 'block_name': 'ftp_anonymous_login', 'description': 'login as anonymous to find legitimate username for further exploit', 'success': True}, 'crack_gpg': {'class_name': 'Initial Access', 'block_name': 'crack_gpg', 'description': 'crack gpg file', 'success': True}, 'crack_hash_by_john': {'class_name': 'Credential Access', 'block_name': 'crack_hash_by_john', 'description': 'crack hash file by john', 'success': True}, 'ssh_login': {'class_name': 'Credential Access', 'block_name': 'ssh_login', 'description': 'login ssh as user', 'success': True}}, 'status': 3, 'success': True, 'tag': ['#ftp', '#PT02', '#PT03', '#PT04', '#PT13']}, 'brooklyn99.yml': {'block_list': {'ftp_anonymous_login': {'class_name': 'Credential Access', 'block_name': 'ftp_anonymous_login', 'description': 'login as anonymous to find legitimate username for further exploit', 'success': True}, 'exploit_user': {'class_name': 'Credential Access', 'block_name': 'exploit_user', 'description': "get the user's password by hydra and login", 'success': False}}, 'status': -1, 'success': False, 'tag': ['#ftp', '#PT03', '#PT04', '#PT05', '#PT13']}, 'agentT.yml': {'block_list': {'nmap_http_php_version': {'class_name': 'Reconnaissance', 'block_name': 'nmap_http_php_version', 'description': 'scan the webserver for PHP version by nmap (PHP versions after 5.5.0 will not respond)', 'success': True}, 'php-8.1.0-dev-exploit': {'class_name': 'Initial Access', 'block_name': 'php-8.1.0-dev-exploit', 'description': 'use script to exploit PHP 8.1.0-dev Backdoor Remote Code Execution', 'success': True}}, 'status': 1, 'success': True, 'tag': ['#Port80', '#PT01', '#PT07']}, 'postgres_login.yml': {'block_list': {'postgres_login.yml': {'class_name': 'Credential Access', 'block_name': 'postgres_login.yml', 'description': 'scan postgres username and password', 'success': False}}, 'status': -1, 'success': False, 'tag': []}, 'ftp_find_sh.yml': {'block_list': {'ftp_find_sh.yml': {'class_name': 'Initial Access', 'block_name': 'ftp_find_sh.yml', 'description': 'find script running at remote', 'success': False}}, 'status': -1, 'success': False, 'tag': []}, 'smbclient.yml': {'block_list': {'smbclient.yml': {'class_name': 'Discovery', 'block_name': 'smbclient.yml', 'description': 'mount a SMB file share', 'success': False}}, 'status': -1, 'success': False, 'tag': []}, 'nmap_sC_sV.yml': {'block_list': {'nmap_sC_sV.yml': {'class_name': 'Reconnaissance', 'block_name': 'nmap_sC_sV.yml', 'description': 'Nmap scan to get the useful info', 'success': True}}, 'status': 1, 'success': True, 'tag': []}, 'pwntools.yml': {'block_list': {'pwntools.yml': {'class_name': 'Privilege Escalation', 'block_name': 'pwntools.yml', 'description': 'Binary Exploitation', 'success': False}}, 'status': 0, 'success': False, 'tag': []}, 'crack_hash_by_john.yml': {'block_list': {'crack_hash_by_john.yml': {'class_name': 'Credential Access', 'block_name': 'crack_hash_by_john.yml', 'description': 'crack hash file by john', 'success': True}}, 'status': 2, 'success': True, 'tag': []}}
        #self.target_host_info = {'IP': '10.10.8.92', 'URL': 'http://10.10.8.92/', 'Service': ['ftp', 'ssh', 'http'], 'OS': None, 'Port': ['21', '22', '80'], 'Apache': None}
        #self.chain_record = {'brooklyn99.yml': {'block_list': {'ftp_anonymous_login': {'class_name': 'Credential Access', 'block_name': 'ftp_anonymous_login', 'description': 'login as anonymous to find legitimate username for further exploit', 'success': True}, 'exploit_user': {'class_name': 'Credential Access', 'block_name': 'exploit_user', 'description': "get the user's password by hydra and login", 'success': True}}, 'status': 2, 'success': True, 'tag': ['#ftp', '#PT03', '#PT04', '#PT05', '#PT13']}, 'pwntools.yml': {'block_list': {'pwntools.yml': {'class_name': 'Privilege Escalation', 'block_name': 'pwntools.yml', 'description': 'Binary Exploitation', 'success': False}}, 'status': 0, 'success': False, 'tag': []}, 'bypass_by_unix_binary.yml': {'block_list': {'bypass_by_unix_binary.yml': {'class_name': 'Privilege Escalation', 'block_name': 'bypass_by_unix_binary.yml', 'description': 'check the user have any sudo permission that we can use to escalate', 'success': True}}, 'status': 3, 'success': True, 'tag': []}}
        self.gen_report()

#test_record = Record()
#test_record.test()
