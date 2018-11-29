from hero.qt_herlper import QtHelper
import hero.proto.hero_time_recommend_pb2 as pb

qt = QtHelper()
sess = qt.createSessInfo(pb.CMD_HEROTIMESVR, pb.SUBCMD_GET_RECOMMEND_VIDEO, 0)

req = pb.GetRecommendVideoReq()
req.game_id = 0
req.area_id = 0
req.type = 3
req.num = 100
req.from_num = 0


res = qt.buildSendPkg(sess, req)
b = res.serialize()

f = open('data2', 'wb')
f.write(b)
