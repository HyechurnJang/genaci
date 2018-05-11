# -*- coding: utf-8 -*-
'''
Created on 2018. 5. 11.
@author: HyechurnJang
'''

import json
import requests
from pygics import Task
from acidipy import Controller, Event

APIC_IP = '10.72.86.21'
APIC_USERNAME = 'admin'
APIC_PASSWORD = '1234Qwer'
APIC_DEBUG = True

GEN_IP = '192.168.2.100'
GEN_KEY = '36854bcd-6083-4701-b2c9-9e545048c26d'

FILTER_EPG = 'tn-SDS-Tenant-01/ap-APP-01/epg-WAS'

ctrl = Controller(APIC_IP, APIC_USERNAME, APIC_PASSWORD, debug=APIC_DEBUG)

class Genian(Event):
    
    def __init__(self, ip, key):
        self.ip = ip
        self.key = key
        self.url = 'https://%s:443/mc2/rest/nodes/?apiKey=%s' % (self.ip, self.key)
        self.headers = {
            'Content-Type' : 'application/json',
            'Accept' : 'application/json'
        }
    
    def handle(self, status, obj):
        self.filter(status, obj)
    
    def filter(self, status, obj):
        if FILTER_EPG not in obj['dn']: return
        if status == 'deleted': return
        if 'ip' not in obj: return
        if 'mac' not in obj: return
        if obj['ip'] == '0.0.0.0': return
        mac = obj['mac']
        ip = obj['ip']
        print 'ENDPOINT EVENT : %s > %s / %s' % (status, mac, ip)
        self.forward(mac, ip)
    
    def forward(self, mac, ip):
        try:
            data = [{
                'nl_ipstr' : mac,
                'nl_mac' : ip,
                'nl_sensornid' : '',
                'nl_genidev' : 0,
                'doNotDeleteNode' : False
            }]
            resp = requests.post(
                self.url,
                headers=self.headers,
                data=json.dumps(data),
                verify=False
            )
            print 'Genian Status : %d' % resp.status_code
            if resp.status_code != 200: return False
            print json.dumps(resp.json(), indent=2)
            print ''
        except Exception as e:
            print 'Error : %s' % str(e)
            return False
        return True

ctrl.Endpoint.event(Genian(GEN_IP, GEN_KEY))

Task.idle()
