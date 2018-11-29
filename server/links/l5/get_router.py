from lib64 import l5sys
def get_router(modId, cmdId):
    ret,qos = l5sys.ApiGetRoute({'modId':int(modId),'cmdId':int(cmdId)},0.2)
    if ret < 0:
        print 
        return 0,0

    #print "ip:"+qos['hostIp']+",port:"+repr(qos['hostPort'])

    iret = 0
    use_time =200

    ret = l5sys.ApiRouteResultUpdate(qos,iret,use_time)
    #print ret

    return qos['hostIp'],qos['hostPort']
