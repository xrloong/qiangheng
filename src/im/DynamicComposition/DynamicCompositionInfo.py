from ..base.IMInfo import IMInfo
from . import DCRadixManager

class DynamicCompositionInfo(IMInfo):
	"動態組字"

	IMName="動組"
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
				'cn':'動態組字',
				'tw':'動態組字',
				'hk':'動態組字',
				'en':'DynamicComposition',
				}
		self.iconfile="qhdc.svg"
		self.maxkeylength=4

IMInfo=DynamicCompositionInfo

radixManager=DCRadixManager.DCRadixManager()

if __name__=='__main__':
	pass

