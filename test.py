'''
FOR TESTING PURPOSES ONLY.
'''

import sys
import subprocess
from itertools import groupby

# Traverse the ipconfig information
data = subprocess.check_output(['ipconfig','/all']).decode('utf-8').split('\n')
for item in data:
     print(item.split('\r')[:-1])

tmp_ip_list = []
ip_list = []
info_list = []
network_type = []

ip_dict = {}

cnt = 0
for item in data:
    if item == '\r' or item == '':
        if (cnt == 2 and item == '\r') or (cnt == 2 and item == ''):
            tmp_ip_list.extend(info_list)
            tmp_ip_list.extend(['-1:-1'])
            info_list.clear()
            cnt = 1
        else:
            cnt += 1
    else:
        if cnt == 2:
            info_list.append(item)
        if cnt == 1:
            network_type.append(item)

i = (list(g) for _, g in groupby(tmp_ip_list, key='-1:-1'.__ne__))
tmp_ip_list = [a + b for a, b in zip(i, i)]

for elm in tmp_ip_list:
    for str in elm:
        elm = [elem.replace(' ', '').replace('\r', '') for elem in elm]
    ip_list.append(elm)

tmp = []
for lists in ip_list:
    for str_val in lists:
        list_of_words = str_val.split(':', 1)
        if len(list_of_words) > 1:
            list_of_words = [list_of_words[0].replace('.', ''), list_of_words[1]]
        tmp.append(list_of_words)

for sublists in tmp:
    if sublists == ['-1', '-1']:
        tmp[tmp.index(sublists)] = '-1'

j = (list(g) for _, g in groupby(tmp, key='-1'.__ne__))
ip_list = [a + b for a, b in zip(j, j)]

for items in ip_list:
    items.remove('-1')
for elm in network_type:
    network_type = [elem.replace('\r', '').replace(':', '') for elem in network_type]

#remove elements with incomplete information
for items in ip_list:
    for sub_elm in items:
        if len(sub_elm) != 2:
            items.remove(items[items.index(sub_elm)])

# print(network_type)
for idx in range(0, len(network_type)):
    ip_dict[network_type[idx]] = dict(ip_list[idx])

print(ip_dict)