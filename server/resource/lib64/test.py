
import l5sys
ret,qos = l5sys.ApiGetRoute({'modId':64020545,'cmdId':196608},0.2)
print ret,qos

print "ip:"+qos['hostIp']+",port:"+repr(qos['hostPort'])

iret = 0
use_time =200

ret = l5sys.ApiRouteResultUpdate(qos,iret,use_time)
print ret

ret, qos = l5sys.ApiGetRoute({'modId':64020545, 'cmdId':327680, 'key':10}, 0.2)
print ret, qos
print "ip:"+qos['hostIp']+",port:"+repr(qos['hostPort'])

iret = 0
use_time =200

ret = l5sys.ApiRouteResultUpdate(qos,iret,use_time)
print ret

ret,qos = l5sys.ApiGetRoute({'modId':64072129,'key':3},0.2)
print ret,qos
print "ip:"+qos['hostIp']+",port:"+repr(qos['hostPort'])

iret = 0
use_time =200

ret = l5sys.ApiRouteResultUpdate(qos,iret,use_time)
print ret
