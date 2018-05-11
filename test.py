# -*- coding: utf-8 -*-
'''
Created on 2018. 5. 11.
@author: HyechurnJang
'''

import json
import requests

IP = ''
KEY = ''

url = 'https://%s:443/mc2/rest/nodes/?apiKey=%s' % (IP, KEY)

headers = {
    'Content-Type' : 'application/json',
    'Accept' : 'application/json'
}

data = [{
    'nl_ipstr' : '',
    'nl_mac' : '',
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
