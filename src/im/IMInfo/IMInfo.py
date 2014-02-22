from gear.CodeInfo import CodeInfo

class IMInfo:
	"輸入法"

	IMName="空"
	def __init__(self):
		self.keyMaps=[]
		self.nameDict={
				'cn':'空',
				'tw':'空',
				'hk':'空',
				'en':'None',
				}
		self.iconfile="empty.png"
		self.maxkeylength=0

	def getName(self, localization):
		return self.nameDict.get(localization, "")

	def getIconFileName(self):
		return self.iconfile

	def getMaxKeyLength(self):
		return self.maxkeylength

	def getKeyMaps(self):
		return self.keyMaps

	def getKeyList(self):
		return "".join(list(zip(*self.keyMaps))[0])

CodeInfoGenerator=CodeInfo

if __name__=='__main__':
	pass

