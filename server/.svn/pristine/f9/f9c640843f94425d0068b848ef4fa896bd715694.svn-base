import uuid
import re
import hashlib

def get_user_id(mac_id='', android_id=''):
    if mac_id or android_id:
        h_md5 = hashlib.md5(mac_id + android_id)
        return h_md5.hexdigest()
    else:
        return str(uuid.uuid1()).replace('-', '')

def get_session(openid='', token=''):
    import time
    if openid and token:
        ts = int(time.time())
        h_md5 = hashlib.md5(openid + token + str(ts))
        return h_md5.hexdigest()
    else:
        return ''

def validSqlInject(param=''):
    check = "(?:')|(?:--)|(/\\*(?:.|[\\n\\r])*?\\*/)|(\\b(select|update|and|or|delete|insert|trancate|char|into|substr|ascii|declare|exec|count|master|into|drop|execute)\\b)"
    return re.search(check, param, re.M|re.I)
