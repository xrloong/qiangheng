from .IMInfo import IMInfo
from ..CodeInfo import FCCodeInfo
from ..CodeInfoEncoder import FCCodeInfoEncoder
from gear.CharacterDescriptionRearranger import CharacterDescriptionRearranger
from gear import RadixManager

class FourCornerInfo(IMInfo):
	"範例輸入法"

	IMName="範例"
	def __init__(self):
		self.keyMaps=[
			['0', '0',],
			['1', '1',],
			['2', '2',],
			['3', '3',],
			['4', '4',],
			['5', '5',],
			['6', '6',],
			['7', '7',],
			['8', '8',],
			['9', '9',],
			]
		self.nameDict={
				'cn':'四角',
				'tw':'四角',
				'hk':'四角',
				'en':'FourCourner',
				}
		self.iconfile="qhfc.svg"
		self.maxkeylength=4

IMInfo=FourCornerInfo
CodeInfoGenerator=FCCodeInfo.FCCodeInfo

codeInfoEncoder=FCCodeInfoEncoder.FCCodeInfoEncoder()
CharacterDescriptionRearrangerGenerator=CharacterDescriptionRearranger

radixManager=RadixManager.RadixManager(codeInfoEncoder)

if __name__=='__main__':
	pass

