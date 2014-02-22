from .IMInfo import IMInfo
from ..CodeInfo import SPCodeInfo
from ..CodeInfoEncoder import SPCodeInfoEncoder
from gear.CharacterDescriptionRearranger import CharacterDescriptionRearranger

class SampleInfo(IMInfo):
	"範例輸入法"

	IMName="範例"
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
				'cn':'范例',
				'tw':'範例',
				'hk':'範例',
				'en':'Sample',
				}
		self.iconfile="qhsp.svg"
		self.maxkeylength=4

IMInfo=SampleInfo
CodeInfoGenerator=SPCodeInfo.SPCodeInfo

codeInfoEncoder=SPCodeInfoEncoder.SPCodeInfoEncoder()
CharacterDescriptionRearrangerGenerator=CharacterDescriptionRearranger

if __name__=='__main__':
	pass

