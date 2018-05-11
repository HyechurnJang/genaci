# -*- coding: utf-8 -*-
'''
Created on 2018. 5. 11.
@author: HyechurnJang
'''

import json
import requests

TEST_IP = '192.168.2.90'
TEST_MAC = 'ab:cd:ef:ab:cd:ef'

IP = '192.168.2.100'
KEY = '36854bcd-6083-4701-b2c9-9e545048c26d'
url = 'https://%s:443/mc2/rest/nodes/?apiKey=%s' % (IP, KEY)

headers = {
    'Content-Type' : 'application/json',
    'Accept' : 'application/json'
}

data = [{
    'nl_ipstr' : TEST_IP,
    'nl_mac' : TEST_MAC,
    'nl_sensornid' : '',
    'nl_genidev' : 0,
    'doNotDeleteNode' : False
}]

resp = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
print resp.status_code
if resp.status_code != 200:
    print 'Error'
    exit(1)

data = resp.json()

print json.dumps(data, indent=2)

