# -*- coding: utf-8 -*-
'''
Created on 2018. 10. 5.
@author: Hyechurn Jang, <hyjang@cisco.com>
'''

import socket
import json
import struct
import requests

def generate(index):
    base_ip_int = 1701143808
    gen_ip_int = base_ip_int + index
    gen_ip = socket.inet_ntoa(struct.pack('!I', gen_ip_int))
    
    base_mac = 'ab:cd:ef:'
    gen_mac = hex(index).replace('0x', '')
    gen_mac_len = len(gen_mac)
    add_mac_len = 6 - gen_mac_len
    for _ in range(0, add_mac_len):
        gen_mac = '0' + gen_mac
    gen_mac = base_mac + '%s:%s:%s' % (gen_mac[0:2], gen_mac[2:4], gen_mac[4:6])
    return (gen_mac, gen_ip)

burst_list = []
for i in range(1, 1000):
    burst_list.append(generate(i))

print(burst_list)

class Genian:
    
    def __init__(self, ip, key):
        self.ip = ip
        self.key = key
        self.url = 'https://%s:443/mc2/rest/nodes/?apiKey=%s' % (self.ip, self.key)
        self.headers = {
            'Content-Type' : 'application/json',
            'Accept' : 'application/json'
        }
    
    def addHost(self, mac, ip, sensornid='', genidev=10, do_not_delete_node=False):
        data = [{
            'nl_ipstr' : ip,
            'nl_mac' : mac,
            'nl_sensornid' : sensornid,
            'nl_genidev' : genidev,
            'doNotDeleteNode' : do_not_delete_node
        }]
        try:
            resp = requests.post(
                self.url,
                headers=self.headers,
                data=json.dumps(data),
                verify=False
            )
        except Exception as e: raise Exception('[ERROR] POST Request:%s' % str(e))
        if resp.status_code != 200: resp.raise_for_status()
        try:
            print('[Genian] add host : %s/%s' % (mac, ip))
            print(json.dumps(resp.json(), indent=2))
        except: raise Exception('[ERROR] Response to Json:%s' % str(e))


GENIAN_IP = '100.1.1.10'
GENIAN_KEY = '5482d439-b0b3-407e-8daf-139a90e3a26f'
gen = Genian(GENIAN_IP, GENIAN_KEY)
for burst in burst_list:
    gen.addHost(burst[0], burst[1])