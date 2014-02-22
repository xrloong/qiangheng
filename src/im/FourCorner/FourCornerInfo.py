from ..base.IMInfo import IMInfo
from . import FCRadixManager

class FourCornerInfo(IMInfo):
	"四角號碼"

	IMName="四角"
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

radixParser=FCRadixManager.FCRadixParser(IMInfo.IMName)
radixManager=radixParser.getRadixManager()

if __name__=='__main__':
	pass

