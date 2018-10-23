# -*- coding: utf-8 -*-
'''
Created on 2018. 5. 11.
@author: HyechurnJang
'''

import json
import requests
try:
    import requests.packages
    requests.packages.urllib3.disable_warnings()
except: pass

class Genian:
    
    def __init__(self, address, passkey):
        self.address = address
        self.passkey = passkey
        self.url = 'https://%s:443/mc2/rest/nodes/?apiKey=%s' % (self.address, self.passkey)
        self.headers = {
            'Content-Type' : 'application/json',
            'Accept' : 'application/json'
        }
        
        # To Fix Connection Check Procedure
        try: resp = requests.get(self.url, headers=self.headers, timeout=2.0, verify=False)
        except Exception as e:
            print('[Genian] ERROR : connect to Genian NAC(%s) with %s' % (address, passkey))
            raise
        if resp.status_code != 200:
            print('[Genian] ERROR : connect to Genian NAC(%s) with %s' % (address, passkey))
            raise
        print('[Genian] INFO : connect to Genian NAC(%s) with %s' % (address, passkey))
    
    def addHost(self, mac, ip, sensornid='', genidev=10, do_not_delete_node=False):
        data = [{
            'nl_ipstr' : ip,
            'nl_mac' : mac,
            'nl_sensornid' : sensornid,
            'nl_genidev' : genidev,
            'doNotDeleteNode' : do_not_delete_node
        }]
        try: resp = requests.post(self.url, headers=self.headers, data=json.dumps(data), timeout=2.0, verify=False)
        except Exception as e:
            print('[Genian:addHost] ERROR : send data : %s' % str(e))
            raise
        if resp.status_code != 200:
            print('[Genian:addHost] ERROR : send data : response code %d' % resp.status_code)
            raise
        print('[Genian] INFO : add %s/%s' % (mac, ip))
