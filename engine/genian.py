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
    
    def __init__(self, ip, key):
        self.ip = ip
        self.key = key
        self.url = 'https://%s:443/mc2/rest/nodes/?apiKey=%s' % (self.ip, self.key)
        self.headers = {
            'Content-Type' : 'application/json',
            'Accept' : 'application/json'
        }
    
    def addHost(self, mac, ip, sensornid='', genidev=0, do_not_delete_node=False):
        data = [{
            'nl_ipstr' : mac,
            'nl_mac' : ip,
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
        try: return resp.json()
        except: raise Exception('[ERROR] Response to Json:%s' % str(e))
