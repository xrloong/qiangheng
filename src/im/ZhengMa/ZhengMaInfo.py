from ..base.IMInfo import IMInfo
from . import ZMRadixManager

class ZhengMaInfo(IMInfo):
	"鄭碼輸入法"

	IMName="鄭碼"
	def __init__(self):
		self.keyMaps=[
			['a', 'Ａ',],
			['b', 'Ｂ',],
			['c', 'Ｃ',],
			['d', 'Ｄ',],
			['e', 'Ｅ',],
			['f', 'Ｆ',],
			['g', 'Ｇ',],
			['h', 'Ｈ',],
			['i', 'Ｉ',],
			['j', 'Ｊ',],
			['k', 'Ｋ',],
			['l', 'Ｌ',],
			['m', 'Ｍ',],
			['n', 'Ｎ',],
			['o', 'Ｏ',],
			['p', 'Ｐ',],
			['q', 'Ｑ',],
			['r', 'Ｒ',],
			['s', 'Ｓ',],
			['t', 'Ｔ',],
			['u', 'Ｕ',],
			['v', 'Ｖ',],
			['w', 'Ｗ',],
			['x', 'Ｘ',],
			['y', 'Ｙ',],
			['z', 'Ｚ',],
			]
		self.nameDict={
				'cn':'郑码',
				'tw':'鄭碼',
				'hk':'鄭碼',
				'en':'ZhengMa',
				}
		self.iconfile="qhzm.svg"
		self.maxkeylength=4

IMInfo=ZhengMaInfo

radixManager=ZMRadixManager.ZMRadixManager(IMInfo.IMName)

if __name__=='__main__':
	pass

