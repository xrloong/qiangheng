from .IM import IM
from character import BSCharInfo

class Boshiamy(IM):
	"嘸蝦米輸入法"

	IMName="嘸蝦米"
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
				'cn':'呒蝦米',
				'tw':'嘸蝦米',
				'hk':'嘸蝦米',
				'en':'Boshiamy',
				}
		self.iconfile="qhbs.svg"
		self.maxkeylength=4

IMInfo=Boshiamy
CharInfoGenerator=BSCharInfo.BSCharInfo

if __name__=='__main__':
	pass

