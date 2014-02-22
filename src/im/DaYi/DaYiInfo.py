from ..base.IMInfo import IMInfo
from . import DYRadixManager

class DaYiInfo(IMInfo):
	"大易輸入法"

	IMName="大易"
	def __init__(self):
		self.keyMaps=[
			[',', '力',],
			['.', '點',],
			['/', '竹',],
			['0', '金',],
			['1', '言',],
			['2', '牛',],
			['3', '目',],
			['4', '四',],
			['5', '王',],
			['6', '門',],
			['7', '田',],
			['8', '米',],
			['9', '足',],
			[';', '虫',],
			['a', '人',],
			['b', '馬',],
			['c', '七',],
			['d', '日',],
			['e', '一',],
			['f', '土',],
			['g', '手',],
			['h', '鳥',],
			['i', '木',],
			['j', '月',],
			['k', '立',],
			['l', '女',],
			['m', '雨',],
			['n', '魚',],
			['o', '口',],
			['p', '耳',],
			['q', '石',],
			['r', '工',],
			['s', '革',],
			['t', '糸',],
			['u', '艸',],
			['v', '禾',],
			['w', '山',],
			['x', '水',],
			['y', '火',],
			['z', '心',],
			]
		self.nameDict={
				'cn':'大易',
				'tw':'大易',
				'hk':'大易',
				'en':'DaYi',
				}
		self.iconfile="qhdy.svg"
		self.maxkeylength=4

IMInfo=DaYiInfo

radixManager=DYRadixManager.DYRadixManager(IMInfo.IMName)

if __name__=='__main__':
	pass

