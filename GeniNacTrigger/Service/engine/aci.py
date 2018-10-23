# -*- coding: utf-8 -*-
'''
Created on 2018. 5. 11.
@author: HyechurnJang
'''

import re
import json
import pygics
from acidipy import Controller, Event

class ACI:
    
    class EPEvent(Event):
        def __init__(self, aci): self.aci = aci
        def handle(self, status, obj):
            try: self.aci.__filter__(status, obj)
            except Exception as e: print(str(e))
    
    def __init__(self, address, username, password):
        self.apic = Controller(address, username, password)
        try: self.apic.Tenant.list(detail=True)
        except:
            print('[ACI] ERROR : connect to APIC(%s) with %s/%s' % (address, username, password))
            raise
        self.address = address
        self.username = username
        self.password = password
        self.epgs = []
        self.apic.Endpoint.event(ACI.EPEvent(self))
        print('[ACI] INFO : connect to APIC(%s) with %s/%s' % (address, username, password))
    
    def close(self):
        self.apic.close()
    
    def checkEPG(self):
        epg_list = [path for path in GENACI.TARGET_EPG_LIST]
        del_list = []
        for epg in self.epgs:
            if epg not in epg_list: del_list.append(epg)
        for epg in del_list:
            self.epgs.remove(epg)
        for path in epg_list:
            if path in self.epgs: continue
            tn, ap, epg = path.split('/')
            try:
                epg = self.apic.Tenant(tn).AppProfile(ap).EPG(epg).detail()
                eps = epg.Endpoint.list(detail=True)
            except Exception as e:
                print('[ACI:checkEPG] ERROR : getting ep list in epg : %s' % str(e))
                GENACI.TARGET_EPG_LIST.remove(path)
                print('[ACI:checkEPG] WARN : %s epg is deleted' % path)
                continue
            for ep in eps:
                try: self.__filter__('inherited', ep)
                except Exception as e:
                    print('[ACI:checkEPG] ERROR : filtering ep failed : %s' % str(e))
            self.epgs.append(path)
    
    def __filter__(self, status, obj):
        # filter deleted case
        if status == 'deleted': return
        
        # filter non registered epg
        dn = obj['dn']
        kv = re.match('uni/tn-(?P<tn>[\W\w]+)/ap-(?P<ap>[\W\w]+)/epg-(?P<epg>[\W\w]+)/.+$', dn)
        if not kv: return
        path = '%s/%s/%s' % (kv.group('tn'), kv.group('ap'), kv.group('epg'))
        if path not in GENACI.TARGET_EPG_LIST: return
        
        # filter uncompleted parameters
        if 'ip' not in obj: return
        
        mac = dn.split('/cep-')[1]
        ip = obj['ip']
        
        # filter ip 0.0.0.0
        if ip == '0.0.0.0': return
        
        # add host
        print('[ACI] INFO : %s/%s/%s by %s' % (path, mac, ip, status))
        if GENACI.GENIAN.HANDLE:
            try: GENACI.GENIAN.HANDLE.addHost(mac, ip)
            except: GENACI.GENIAN.unregister()
