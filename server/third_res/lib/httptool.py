import json
import urllib2
from urllib2 import urlopen
#from urllib.request import urlopen

def open_url(url='', data = None, timeout=10000):
    if data:
        data = urllib.urlencode(data)
    f = urlopen(url, data = data , timeout = timeout)
    o=f.read().decode()
    return json.loads(o)

def open_url_json(url='', data = None, timeout=10000):
    if data:
        data = json.dumps(data)
        request = urllib2.Request(url,data)
        request.add_header('Content-Type', 'application/json')

        f = urlopen(request,timeout = timeout)
        o=f.read().decode()
        return json.loads(o)
