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

	def getKeyList(self):
		return "".join(list(zip(*self.keyMaps))[0])

	def setTable(self, tb):
		self.tb=tb
		self.method='T'

	def setStruct(self, descMgr):
		self.descMgr=descMgr
		self.method='D'

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

		if self.method=='D':
			table=[]
			for chname in getTargetChars():
#				expandDesc=self.descMgr.getExpandDescriptionByName(chname)
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
#					print("Debug", chname)
		elif self.method=='T':
			table=self.tb
		else:
			table=[]
		return table

if __name__=='__main__':
	pass

