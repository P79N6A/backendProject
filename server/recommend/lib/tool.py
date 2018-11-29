import uuid
import hashlib

def get_user_id(mac_id='', android_id=''):
    if mac_id or android_id:
        h_md5 = hashlib.md5(mac_id + android_id)
        return h_md5.hexdigest()
    else:
        return str(uuid.uuid1()).replace('-', '')
