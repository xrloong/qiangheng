from .IMInfo import IMInfo
from ..CodeInfo import ARCodeInfo
from ..CodeInfoEncoder import ARCodeInfoEncoder
from ..RadixManager import ARRadixManager
from gear.CharacterDescriptionRearranger import CharacterDescriptionRearranger

class ArrayInfo(IMInfo):
	"行列輸入法"

	IMName="行列"
	def __init__(self):
		self.keyMaps=[
			['a', '1-',],
			['b', '5v',],
			['c', '3v',],
			['d', '3-',],
			['e', '3^',],
			['f', '4-',],
			['g', '5-',],
			['h', '6-',],
			['i', '8^',],
			['j', '7-',],
			['k', '8-',],
			['l', '9-',],
			['m', '7v',],
			['n', '6v',],
			['o', '9^',],
			['p', '0^',],
			['q', '1^',],
			['r', '4^',],
			['s', '2-',],
			['t', '5^',],
			['u', '7^',],
			['v', '4v',],
			['w', '2^',],
			['x', '2v',],
			['y', '6^',],
			['z', '1v',],
			['.', '9v',],
			['/', '0v',],
			[';', '0-',],
			[',', '8v',],
			]
		self.nameDict={
				'cn':'行列',
				'tw':'行列',
				'hk':'行列',
				'en':'Array',
				}
		self.iconfile="qhar.svg"
		self.maxkeylength=4

IMInfo=ArrayInfo
CodeInfoGenerator=ARCodeInfo.ARCodeInfo

codeInfoEncoder=ARCodeInfoEncoder.ARCodeInfoEncoder()
CharacterDescriptionRearrangerGenerator=CharacterDescriptionRearranger

radixManager=ARRadixManager.ARRadixManager(codeInfoEncoder)

if __name__=='__main__':
	pass

