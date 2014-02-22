from ..base.IMInfo import IMInfo
from .GXRadixManager import GXRadixParser
from .GXCodeInfoEncoder import GXCodeInfoEncoder

class GuiXieInfo(IMInfo):
	"中國字庋㩪"

	IMName="庋㩪"
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
				'cn':'庋㩪',
				'tw':'庋㩪',
				'hk':'庋㩪',
				'en':'GuiXie',
				}
		self.iconfile="qhgx.svg"
		self.maxkeylength=6

IMInfo=GuiXieInfo

codeInfoEncoder=GXCodeInfoEncoder()
radixParser=GXRadixParser(IMInfo.IMName, codeInfoEncoder)

if __name__=='__main__':
	pass

