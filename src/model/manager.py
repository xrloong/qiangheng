from injector import inject

class RadixDescriptionManager:
	@inject
	def __init__(self):
		self.descriptionDict={}
		self.radixCodeInfoDB={}
		self.radixDescDB={}
		self.resetRadixList=[]

	def addCodeInfoList(self, charName, radixCodeInfoList):
		self.radixCodeInfoDB[charName]=radixCodeInfoList

	def getResetRadixList(self):
		return self.resetRadixList

	def getCodeInfoList(self, charName):
		return self.radixCodeInfoDB[charName]

	def getCodeInfoDB(self):
		return self.radixCodeInfoDB

	def addDescription(self, charName, description):
		if description.isToOverridePrev():
			tmpRadixDesc = description
			self.resetRadixList.append(charName)
		else:
			if charName in self.descriptionDict:
				tmpRadixDesc=self.descriptionDict.get(charName)
				tmpRadixDesc.mergeRadixDescription(description)
			else:
				tmpRadixDesc=description

		self.descriptionDict[charName]=tmpRadixDesc
		self.radixDescDB[charName]=tmpRadixDesc

	def getDescriptionList(self):
		return list(self.descriptionDict.items())

	def getDescription(self, radixName):
		return self.radixDescDB[radixName]

