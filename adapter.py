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

ctrl = Controller(APIC_IP, APIC_USERNAME, APIC_PASSWORD)

class Genian(Event):
    
    def handle(self, status, obj):
        print status
        print obj

ctrl.Endpoint.event(Genian())

Task.idle()
