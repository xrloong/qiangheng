import sys

class RadixManager:
	def __init__(self, codeInfoEncoder):
		self.codeInfoEncoder=codeInfoEncoder
		self.radixCodeInfoDB={}

	def setTurtleInfoList(self, charDescList):
		for charDesc in charDescList:
			charName=charDesc.getName()
			for structDesc in charDesc.getStructureList():
				if structDesc.isTurtle():
					codeVariance=structDesc.getCodeVarianceType()
					codeInfoProperties=structDesc.getCodeInfoDict()
					codeInfo=self.codeInfoEncoder.generateCodeInfo(codeInfoProperties)
					codeInfo.multiplyCodeVarianceType(codeVariance)

					radixCodeInfoList=self.radixCodeInfoDB.get(charName, [])
					radixCodeInfoList.append(codeInfo)
					self.radixCodeInfoDB[charName]=radixCodeInfoList
					pass
				else:
					print("型態錯誤", file=sys.stderr)

	def getRadixCodeInfo(self, radixName):
		return self.radixCodeInfoDB.get(radixName)[0]

	def getRadixCodeInfoList(self, radixName):
		return self.radixCodeInfoDB.get(radixName)

	def hasRadix(self, radixName):
		return (radixName in self.radixCodeInfoDB)

