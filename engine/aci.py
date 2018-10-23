# -*- coding: utf-8 -*-
'''
Created on 2018. 5. 11.
@author: HyechurnJang
'''

import re
import json
import pygics
from acidipy import Controller, Event
from .genian import Genian

class ACI:
    
    class EPEvent(Event):
        def __init__(self, aci): self.aci = aci
        def handle(self, status, obj):
            try: self.aci.__filter__(status, obj)
            except Exception as e: print(str(e))
    
    def __init__(self, apic_ip, apic_username, apic_password, genian_ip, genian_key, stdout=False):
        self.stdout = stdout
        self.epgs = []
        self.apic = Controller(apic_ip, apic_username, apic_password)
        if not self.stdout:
            self.genian = Genian(genian_ip, genian_key)
    
    def __filter__(self, status, obj):
        # filter deleted case
        if status == 'deleted': return
        
        # filter non registered epg
        dn = obj['dn']
        kv = re.match('uni/tn-(?P<tn>[\W\w]+)/ap-(?P<ap>[\W\w]+)/epg-(?P<epg>[\W\w]+)/.+$', dn)
        if not kv: return
        path = '%s/%s/%s' % (kv.group('tn'), kv.group('ap'), kv.group('epg'))
        if path not in self.epgs: return
        
        # filter uncompleted parameters
        if 'ip' not in obj: return
        
        mac = dn.split('/cep-')[1]
        ip = obj['ip']
        
        # filter ip 0.0.0.0
        if ip == '0.0.0.0': return
        
        # add host
        print('[ACI] %s : %s/%s/%s' % (status, path, mac, ip))
        if not self.stdout:
            self.genian.addHost(mac, ip)
    
    def addEPG(self, path):
        if not re.search('^[\W\w]+/[\W\w]+/[\W\w]+', path): raise Exception('invalid epg path')
        self.epgs.append(path)
        print(path)
        tn, ap, epg = path.split('/')
        epg = self.apic.Tenant(tn).AppProfile(ap).EPG(epg).detail()
        print(json.dumps(epg, indent=2))
        eps = epg.Endpoint.list(detail=True)
        print(json.dumps(eps, indent=2))
        for ep in eps:
            self.__filter__('inherited', ep)
            
    
    def run(self):
        self.apic.Endpoint.event(ACI.EPEvent(self))
        pygics.Task.idle()
