from ..base.IMInfo import IMInfo
from .CJRadixManager import CJRadixParser
from .CJCodeInfoEncoder import CJCodeInfoEncoder

class CangJieInfo(IMInfo):
	"倉頡輸入法"

	IMName="倉頡"
	def __init__(self):
		self.keyMaps=[
			['a', '日',],
			['b', '月',],
			['c', '金',],
			['d', '木',],
			['e', '水',],
			['f', '火',],
			['g', '土',],
			['h', '竹',],
			['i', '戈',],
			['j', '十',],
			['k', '大',],
			['l', '中',],
			['m', '一',],
			['n', '弓',],
			['o', '人',],
			['p', '心',],
			['q', '手',],
			['r', '口',],
			['s', '尸',],
			['t', '廿',],
			['u', '山',],
			['v', '女',],
			['w', '田',],
			['x', '難',],
			['y', '卜',],
			['z', '符',],
			]
		self.nameDict={
				'cn':'仓颉',
				'tw':'倉頡',
				'hk':'倉頡',
				'en':'CangJie',
				}
		self.iconfile="qhcj.svg"
		self.maxkeylength=5

IMInfo=CangJieInfo

codeInfoEncoder=CJCodeInfoEncoder()
radixParser=CJRadixParser(IMInfo.IMName, codeInfoEncoder)

if __name__=='__main__':
	pass

