
import re
import sys
import json
from jzlib import setGlobals
from pygics import rest
from .aci import ACI
from .genian import Genian

class __GENACI__:
    
    TARGET_EPG_LIST = []
    STATUS = 'stopped'
    
    class APIC:
        HANDLE = None
        STATUS = 'disconnected'
        
        @classmethod
        def register(cls, address, username, password):
            
            def _register(_address, _username, _password):
                try: __GENACI__.APIC.HANDLE = ACI(_address, _username, _password)
                except Exception as e:
                    __GENACI__.APIC.HANDLE = None
                    __GENACI__.APIC.STATUS = 'disconnected'
                    return str(e)
                __GENACI__.APIC.STATUS = 'connected'
                return None
            
            cur = __GENACI__.APIC.HANDLE
            if cur:
                if cur.address != address or cur.username != username or cur.password != password:
                    cur.close()
                    return _register(address, username, password)
            else: return _register(address, username, password)
            return None
        
        @classmethod
        def unregister(cls):
            if __GENACI__.APIC.HANDLE:
                __GENACI__.APIC.HANDLE.close()
                __GENACI__.APIC.HANDLE = None
                __GENACI__.APIC.STATUS = 'disconnected'
    
    class GENIAN:
        HANDLE = None
        STATUS = 'disconnected'
        
        @classmethod
        def register(cls, address, passkey):
            
            def _register(_address, _passkey):
                try: __GENACI__.GENIAN.HANDLE = Genian(_address, _passkey)
                except Exception as e:
                    __GENACI__.GENIAN.HANDLE = None
                    __GENACI__.GENIAN.STATUS = 'disconnected'
                    return str(e)
                __GENACI__.GENIAN.STATUS = 'connected'
                return None
            
            cur = __GENACI__.GENIAN.HANDLE
            if cur:
                if cur.address != address or cur.passkey != passkey:
                    return _register(address, passkey)
            else: return _register(address, passkey)
            return None
        
        @classmethod
        def unregister(cls):
            if __GENACI__.GENIAN.HANDLE:
                __GENACI__.GENIAN.HANDLE = None
                __GENACI__.GENIAN.STATUS = 'disconnected'
    
    @classmethod
    def toDict(cls):
        result = {
            'status' : __GENACI__.STATUS,
            'target_epg_list' : __GENACI__.TARGET_EPG_LIST,
            'apic' : { 'status' : __GENACI__.APIC.STATUS },
            'genian' : { 'status' : __GENACI__.GENIAN.STATUS }
        }
        if __GENACI__.APIC.HANDLE:
            result['apic']['address'] = __GENACI__.APIC.HANDLE.address
            result['apic']['username'] = __GENACI__.APIC.HANDLE.username
            result['apic']['password'] = __GENACI__.APIC.HANDLE.password
        else:
            result['apic']['address'] = ''
            result['apic']['username'] = ''
            result['apic']['password'] = ''
        if __GENACI__.GENIAN.HANDLE:
            result['genian']['address'] = __GENACI__.GENIAN.HANDLE.address
            result['genian']['passkey'] = __GENACI__.GENIAN.HANDLE.passkey
        else:
            result['genian']['address'] = ''
            result['genian']['passkey'] = ''
        return result
    

setGlobals(GENACI=__GENACI__)

@rest('GET', '/genaci.json')
def get_status(req):
    return __GENACI__.toDict()

@rest('POST', '/genaci.json')
def set_config(req):
    data = req.data
    error = []
    
    if 'genian' in data:
        genian = data['genian']
        address = str(genian['address']).strip() if 'address' in genian else ''
        passkey = str(genian['passkey']).strip() if 'passkey' in genian else ''
        if address and passkey:
            ret = __GENACI__.GENIAN.register(address, passkey)
            if ret: error.append(ret)
    
    if 'target_epg_list' in data:
        target_epg_list = data['target_epg_list']
        if sys.version_info.major < 3:
            if isinstance(target_epg_list, str): target_epg_list = [path.strip() for path in target_epg_list.split(',')]
            elif isinstance(target_epg_list, unicode): target_epg_list = [path.strip() for path in str(target_epg_list).split(',')] 
            elif isinstance(target_epg_list, list): target_epg_list = [str(path).strip() for path in target_epg_list]
        else:
            if isinstance(target_epg_list, str): target_epg_list = [path.strip() for path in target_epg_list.split(',')]
            elif isinstance(target_epg_list, list): target_epg_list = [path.strip() for path in target_epg_list]
        for path in [path for path in target_epg_list]:
            if not re.search('^[\W\w]+/[\W\w]+/[\W\w]+', path): target_epg_list.remove(path)
        __GENACI__.TARGET_EPG_LIST = target_epg_list
    
    ret = None
    if 'apic' in data:
        apic = data['apic']
        address = str(apic['address']).strip() if 'address' in apic else ''
        username = str(apic['username']).strip() if 'username' in apic else ''
        password = str(apic['password']).strip() if 'password' in apic else ''
        if address and username and password:
            ret = __GENACI__.APIC.register(address, username, password)
            if ret: error.append(ret)
    
    if __GENACI__.APIC.HANDLE:
        __GENACI__.APIC.HANDLE.checkEPG()
    
    if __GENACI__.APIC.HANDLE and __GENACI__.GENIAN.HANDLE: __GENACI__.STATUS = 'running'
    elif __GENACI__.APIC.HANDLE: __GENACI__.STATUS = 'Genian NAC is not ready'
    elif __GENACI__.GENIAN.HANDLE: __GENACI__.STATUS = 'APIC is not ready'
    
    result = __GENACI__.toDict()
    if error: result['error'] = ', '.join(error)
    return result 
