from hero.qt_herlper import QtHelper
import hero.proto.hero_time_recommend_pb2 as pb

qt = QtHelper()
f = open('data2', 'rb')
b = f.read()
resp = qt.parseReceivePkg(b)
resp.unserialize()
print repr(resp.header.c_a)
print repr(resp.header.subcmd)
print repr(resp.header.cldPkgHead.command)
print repr(resp.header.relayPkgHeadEx2.shExLen)
print repr(resp.c_end)

#resp_str = str(bytearray(resp.body_str))
resp_str = str(buffer(resp.body_str)[:])

pb_resp = pb.GetRecommendVideoReq()
pb_resp.ParseFromString(resp_str)

print pb_resp.game_id
print pb_resp.area_id
print pb_resp.type
print pb_resp.num
print pb_resp.from_num

f.close()
