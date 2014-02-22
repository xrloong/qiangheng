class NoneIM:
	"輸入法"

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

	def setStruct(self, descMgr):
		self.descMgr=descMgr

	def genIMMapping(self):
		def getTargetChars():
			charPool=[
					'土',
					'吉',
					'夠',
					'炎',
					'畦',
					'海',
					]
			charPool=self.descMgr.keys()
			return charPool

		table=[]
		for chname in getTargetChars():
			expandDesc=self.descMgr.getExpandDescriptionByNameInNetwork(chname)

			if expandDesc==None:
				continue

			self.descMgr.setCharTree(expandDesc)

			chinfo=expandDesc.getChInfo()
			code=chinfo.getCode()
			if chinfo.isToShow() and code:
				table.append([code, chname])
			else:
				pass
		return table

if __name__=='__main__':
	pass

