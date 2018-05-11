# -*- coding: utf-8 -*-
'''
Created on 2018. 5. 11.
@author: HyechurnJang
'''

import re
import pygics
from acidipy import Controller, Event
from .genian import Genian

class ACI:
    
    class EPEvent(Event):
        def __init__(self, aci): self.aci = aci
        def handle(self, status, obj):
            try: self.aci.__filter__(status, obj)
            except Exception as e: print str(e)
    
    def __init__(self, apic_ip, apic_username, apic_password, genian_ip, genian_key):
        self.epgs = []
        self.apic = Controller(apic_ip, apic_username, apic_password)
        self.genian = Genian(genian_ip, genian_key)
    
    def __filter__(self, status, obj):
        
        print '%s %s' % (status, obj)
        
        # filter deleted case
        if status == 'deleted': return
        
        # filter non registered epg
        dn = obj['dn']
        print dn
        kv = re.match('uni/tn-(?P<tn>[\W\w]+)/ap-(?P<ap>[\W\w]+)/epg-(?P<epg>[\W\w]+)/.+$', dn)
        if not kv: return
        tn = kv.group('tn')
        ap = kv.group('ap')
        epg = kv.group('epg')
        path = '%s/%s/%s' % (tn, ap, epg)
        
        print path
        
        if path not in self.epgs: return
        
        # filter uncompleted parameters
        if 'ip' not in obj: return
        
        mac = dn.split('/cep-')[1]
        ip = obj['ip']
        
        print '%s / %s' % (mac, ip)
        
        # filter ip 0.0.0.0
        if ip == '0.0.0.0': return
        
        # add host
        
        print 'try add host'
        
        self.genian.addHost(mac, ip)
        
        print 'ok'
    
    def addEPG(self, path):
        if not re.search('^[\W\w]+/[\W\w]+/[\W\w]+', path): raise Exception('invalid epg path')
        self.epgs.append(path)
    
    def run(self):
        self.apic.Endpoint.event(ACI.EPEvent(self))
        pygics.Task.idle()
