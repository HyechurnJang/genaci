# -*- coding: utf-8 -*-
'''
Created on 2018. 5. 11.
@author: HyechurnJang
'''

from engine import ACI

APIC_IP = '10.72.86.21'
APIC_USERNAME = 'admin'
APIC_PASSWORD = '1234Qwer'

GENIAN_IP = '192.168.2.100'
GENIAN_KEY = 'ad611193-3876-43bc-bab9-bab63acf80d1'

EPGS = [
    'SDS-Tenant-01/APP-01/WAS',
]

aci = ACI(APIC_IP, APIC_USERNAME, APIC_PASSWORD, GENIAN_IP, GENIAN_KEY)

for epg in EPGS: aci.addEPG(epg)

aci.run()
