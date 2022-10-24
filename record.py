from os import stat
from unittest import result
import matplotlib.pyplot as plt
from sympy import content

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
                for p in tag['Porte']:
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
        print("In record, add new chain:\n", new_chain_rec)
        print("Record content:", self.chain_record)

    def add_chain_info(self, chain_name, class_name, block_name, block):
        self.chain_record[chain_name]['block_list'][block_name] = self.add_block_info(class_name, block_name, block)

    def add_block_info(self, class_name, block_name, block):
        new_block_rec = dict()
        new_block_rec['class_name'] = class_name
        new_block_rec['block_name'] = block_name
        new_block_rec['description'] = block.description
        new_block_rec['success'] = False
        
        print("Record content:", self.chain_record)
        return new_block_rec

    def add_chain_mark(self, chain_name, success):
        self.chain_record[chain_name]['success'] = success
        print("mark atk_chain", chain_name, "'s result", success)
        print("Record content:", self.chain_record)

    def add_block_mark(self, chain_name, block_name, success):
        self.chain_record[chain_name]['block_list'][block_name]['success'] = success
        print("mark atk_chain", chain_name, "block:", block_name, "'s result", success)
        print("Record content:", self.chain_record)

    def add_chain_status(self, chain_name):
        print("After this excution of attack chain/block, which status do you reach?\nPlease select the highest that meets your condition.\n")
        print("0. not getting anything interesting\n")
        print("1. access data\n")
        print("2. get shell or user credentials\n")
        print("3. get root permission\n")
        status = -1
        while(status not in range(4)):
            try:
                status = int(input(">"))
            except ValueError:
                pass
        self.chain_record[chain_name]['status'] = status
        print("Record content:", self.chain_record)

    def add_chain_status_directly(self, chain_name, status):
        self.chain_record[chain_name]['status'] = status

    def gen_report(self):
        print(self.target_host_info)
        print(self.chain_record)
        report_file = open('./report/report.html', 'w+')
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
        return head
    
    def gen_success_rate(self):
        labels = ['fail', 'else', 'get data', 'get shell', 'get root']
        count = [0, 0, 0, 0, 0]
        colors = ['tab:blue', 'tab:cyan', 'tab:gray', 'tab:orange', 'tab:red']
        for k in self.chain_record.keys():
            status = self.chain_record[k]['status']
            idx = status + 1
            count[idx] = count[idx] + 1
        
        fig, ax = plt.subplots()

        labels = [label for label in labels if count[labels.index(label)] != 0]
        count = [c for c in count if c != 0]
        
        ax.pie(count, labels = labels, colors = colors, autopct=lambda p: '{:.1f}%'.format(round(p)) if p > 0 else '')
        plt.axis('equal')
        plt.legend(loc = "best")
        plt.savefig("./report/status_pie.jpg")
        plt.close()

        content = "<h1>result</h1>\n"
        content = content + "<img src=\"status_pie.jpg\">\n\n"
        return content

    def gen_target_host_info(self):
        content = "<h1>target host information</h1>\n"
        content = content + "<p>IP: {IP}</p>\n".format(IP=str(self.target_host_info['IP']))
        content = content + "<p>Service: {Service}</p>\n".format(Service=str(self.target_host_info['Service']))
        content = content + "<p>OS: {OS}</p>\n".format(OS=str(self.target_host_info['OS']))
        content = content + "<p>Port: {Port}</p>\n".format(Port=str(self.target_host_info['Port']))
        content = content + "<p>Apache: {Apache}</p>\n\n".format(Apache=str(self.target_host_info['Apache']))
        return content

    def gen_overview(self):
        content = "<h1>attack chain overview</h1>\n"
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
            status_list = ['fail', 'else', 'get data', 'get shell', 'get root']
            content = content + "<td>" +  status_list[self.chain_record[chain_name]['status']+1] +"</td>\n"
            
            content = content + "</tr>\n"
        content = content + "</table>\n"
        return content

    def gen_detail(self):
        content = "<h1>attack chain details</h1>\n"
        for chain_name in self.chain_record.keys():
            content = content + "<table>\n"
            num_block = len(self.chain_record[chain_name]['block_list'].keys())
            
            content = content + "<tr>\n" + "<th colspan=\"{col}\">{chain_name}</th>\n".format(col=num_block+1, chain_name=chain_name) + "<th colspan=\"1\">result</th>\n" + "</tr>\n"
            #class row
            content = content + "<tr>\n" + "<th>class</th>\n"
            block_list = self.chain_record[chain_name]['block_list']
            for block_name in block_list:
                content = content + "<td colspan=\"1\">" + block_list[block_name]['class_name'] + "</td>\n"
            status_list = ['fail', 'else', 'get data', 'get shell', 'get root']
            content = content + "<td rowspan=\"3\">{result}</td>".format(result=status_list[self.chain_record[chain_name]['status']+1])
            content = content + "</tr>\n"
            
            #block row
            content = content + "<tr>\n" + "<th>block</th>\n"
            block_list = self.chain_record[chain_name]['block_list']

            class_suc = ""
            for block_name in block_list:
                if block_list[block_name]['success'] == True:
                    class_suc = "sucessful_block"
                else:
                    class_suc = "failed_block"
                content = content + "<td class=\"{successful}\">".format(successful=class_suc) + block_name + "</td>\n"
            content = content + "</tr>\n"

            #tag row
            content = content + "<tr>\n" + "<th>tags</th>\n" +"<td  colspan=\"{num_block}\">".format(num_block=num_block)
            for t in self.chain_record[chain_name]['tag']:
                content = content + t + " "            
            content = content + "</tr>\n"
            
            content = content + "</td>\n" + "</table>\n"
        return content

    def gen_foot(self):
        template = open("report_template.html", "r").read()
        foot = template.split("<p>content</p>")[1]
        return foot

    def test(self):
        self.target_host_info = {'IP': '99.83.179.177', 'Service': ['http', 'https'], 'OS': None, 'Port': ['80', '443'], 'Apache': None}
        self.chain_record = {'annie.yml': {'block_list': {'nmap_sC_sV': {'class_name': 'Reconnaissance', 'block_name': 'nmap_sC_sV', 'description': 'Nmap scan to get the useful info', 'success': True}, 'CVE-2020–13160': {'class_name': 'Initial Access', 'block_name': 'CVE-2020–13160', 'description': 'create and send reverse shell by python2', 'success': True}, 'get_bash_by_python': {'class_name': 'Initial Access', 'block_name': 'get_bash_by_python', 'description': 'get bash through python', 'success': True}}, 'status': 2, 'success': True, 'tag': ['#PT01', '#PT05']}, 'postgres_login.yml': {'block_list': {'postgres_login.yml': {'class_name': 'Credential Access', 'block_name': 'postgres_login.yml', 'description': 'scan postgres username and password', 'success': False}}, 'status': -1, 'success': False, 'tag': []}, 'pwntools.yml': {'block_list': {'pwntools.yml': {'class_name': 'Privilege Escalation', 'block_name': 'pwntools.yml', 'description': 'Binary Exploitation', 'success': False}}, 'status': -1, 'success': False, 'tag': []}} 
        self.gen_report()

# test_record = Record()
# test_record.test()
