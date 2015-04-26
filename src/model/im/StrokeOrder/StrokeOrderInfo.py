from model.base.IMInfo import IMInfo

class StrokeOrderInfo(IMInfo):
	"筆順"

	IMName="筆順"
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
				'cn':'笔順',
				'tw':'筆順',
				'hk':'筆順',
				'en':'StrokeOrder',
				}
		self.iconfile="qhdc.svg"
		self.maxkeylength=4

if __name__=='__main__':
	pass

