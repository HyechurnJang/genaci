# -*- coding: utf-8 -*-
'''
Created on 2018. 5. 11.
@author: HyechurnJang
'''

from engine import ACI

APIC_IP = '10.72.86.21'
APIC_USERNAME = 'admin'
APIC_PASSWORD = '1234Qwer'

GENIAN_IP = '100.1.1.10'
GENIAN_KEY = '5482d439-b0b3-407e-8daf-139a90e3a26f'
STDOUT = False

EPGS = [
    'A/APP/A',
]

aci = ACI(APIC_IP, APIC_USERNAME, APIC_PASSWORD, GENIAN_IP, GENIAN_KEY, STDOUT)

for epg in EPGS: aci.addEPG(epg)

aci.run()
