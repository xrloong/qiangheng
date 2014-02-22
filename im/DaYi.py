from .IM import IM
from character import DYCharInfo

class DaYi(IM):
	"大易輸入法"

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
			['A', '人',],
			['B', '馬',],
			['C', '七',],
			['D', '日',],
			['E', '一',],
			['F', '土',],
			['G', '手',],
			['H', '鳥',],
			['I', '木',],
			['J', '月',],
			['K', '立',],
			['L', '女',],
			['M', '雨',],
			['N', '魚',],
			['O', '口',],
			['P', '耳',],
			['Q', '石',],
			['R', '工',],
			['S', '革',],
			['T', '糸',],
			['U', '艸',],
			['V', '禾',],
			['W', '山',],
			['X', '水',],
			['Y', '火',],
			['Z', '心',],
			]
		self.nameDict={
				'cn':'大易',
				'tw':'大易',
				'hk':'大易',
				'en':'DaYi',
				}
		self.iconfile="qhdy.svg"
		self.maxkeylength=4

IMInfo=DaYi
CharInfoGenerator=DYCharInfo.DYCharInfo

if __name__=='__main__':
	pass

