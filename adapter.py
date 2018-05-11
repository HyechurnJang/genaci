# -*- coding: utf-8 -*-
'''
Created on 2018. 5. 11.
@author: HyechurnJang
'''

import json
from pygics import Task
from acidipy import Controller, Event

APIC_IP = '10.72.86.21'
APIC_USERNAME = 'admin'
APIC_PASSWORD = '1234Qwer'
APIC_DEBUG = True

FILTER_EPG = 'tn-SDS-Tenant-01/ap-APP-01/epg-WAS'

ctrl = Controller(APIC_IP, APIC_USERNAME, APIC_PASSWORD, debug=APIC_DEBUG)

class Genian(Event):
    
    def filter(self, status, obj):
        if FILTER_EPG not in obj['dn']: return
        print status
        print json.dumps(obj, indent=2)
    
    def handle(self, status, obj):
        self.filter(status, obj)

ctrl.Endpoint.event(Genian())

Task.idle()
