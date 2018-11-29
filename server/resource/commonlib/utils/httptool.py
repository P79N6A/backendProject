import json
import traceback
import re
import urllib2
from urllib2 import urlopen


def open_url_json(url='', data = None, timeout=10000):
    if data:
        data = json.dumps(data)
        request = urllib2.Request(url,data)
        request.add_header('Content-Type', 'application/json')

        f = urlopen(request,timeout = timeout)
        o=f.read().decode()
        return json.loads(o)

def open_url(url='', data = None, timeout=10000):
    if data:
        data = urllib.urlencode(data)
    f = urlopen(url, data = data , timeout = timeout)
    o=f.read().decode()

    try:
        #return o
        return json.loads(o)
    except:
        return o

def open_url_kv(url='', data = None, timeout=10000):
    if data:
        data = urllib.urlencode(data)
    f = urlopen(url, data = data , timeout = timeout)
    o=f.read().decode()
    try:
        obj = {}
        for item in o.split('&'):
            k,v = item.split('=')
            obj[k] = v
        return obj
    except:
        return o

def open_url_jsonp(url='', data = None, timeout=10000):
    if data:
        data = urllib.urlencode(data)
    f = urlopen(url, data = data , timeout = timeout)
    o=f.read().decode()
    try:
	result = re.match(r'^callback\((.*)\);$', o, re.M|re.I)
	if (result):
            return json.loads(result.group(1))
	else:
            return o
        #return json.loads(o.replace('callback','').replace('(','').replace(')','').replace(';',''))
    except:
        return o
