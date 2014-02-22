import sys
from state import StateManager

class HanZiStructure:
	def __init__(self):
		self.flagIsSet=False

	def getCodeInfoList(self):
		return []

	def getStructureList(self):
		return []

	def setCompositions(self):
		pass

	def setStructureTree(self):
		if self.flagIsSet:
			return

		self.flagIsSet=True

		structureList=self.getStructureList()
		for structure in structureList:
			structure.setStructureTree()

		self.setCompositions()

	def printAllCodeInfo(self):
		for codeInfo in self.getCodeInfoList():
			pass

class HanZiUnitStructure(HanZiStructure):
	def __init__(self, radixCodeInfo):
		HanZiStructure.__init__(self)
		self.codeInfoList=[radixCodeInfo]

	def getCodeInfoList(self):
		return self.codeInfoList

	def getStructureList(self):
		return []

	def setCompositions(self):
		pass

class HanZiWrapperStructure(HanZiStructure):
	def __init__(self, referenceNode, expression):
		HanZiStructure.__init__(self)

		self.referenceNode=referenceNode
		self.expression=expression
		self.codeInfoList=[]

	def getCodeInfoList(self):
		codeInfoList=[]
		for structure in self.getStructureList():
			codeInfoList.extend(structure.getCodeInfoList())
		return codeInfoList

	def getStructureList(self):
		tempList=self.expression.split(".")
		if(len(tempList)>1):
			referenceName=tempList[0]
			index=int(tempList[1])
			structureList=self.referenceNode.getSubStructureList(index)
		else:
			structureList=self.referenceNode.getStructureList()
		return structureList

	def setCompositions(self):
		self.referenceNode.setNodeTree()

class HanZiAssemblageStructure(HanZiStructure):
	def __init__(self, codeVariance, operator, structureList):
		HanZiStructure.__init__(self)

		self.operator=operator
		self.structureList=structureList

		self.codeInfoList=[]
		self.codeVariance=codeVariance

	def getCodeInfoList(self):
		return self.codeInfoList

	def getStructureList(self):
		return self.structureList

	def setCompositions(self):
		structureList=self.getStructureList()
		infoListList=HanZiAssemblageStructure.getAllCodeInfoListFromNodeList(structureList)

		for infoList in infoListList:
			codeInfo=StateManager.codeInfoEncoder.encode(self.operator, infoList)
			if codeInfo!=None:
				codeInfo.multiplyCodeVarianceType(self.codeVariance)

				for childCodeInfo in infoList:
					codeVariance=childCodeInfo.getCodeVarianceType()
					codeInfo.multiplyCodeVarianceType(codeVariance)

				self.codeInfoList.append(codeInfo)

	@staticmethod
	def getAllCodeInfoListFromNodeList(structureList):
		def combineList(infoListList, infoListOfNode):
			if len(infoListList)==0:
				ansListList=[]
				for codeInfo in infoListOfNode:
					ansListList.append([codeInfo])
			else:
				ansListList=[]
				for infoList in infoListList:
					for codeInfo in infoListOfNode:
						ansListList.append(infoList+[codeInfo])

			return ansListList

		infoListList=[]

		for structure in structureList:
			tmpCodeInfoList=structure.getCodeInfoList()
			codeInfoList=filter(lambda x: x.isSupportRadixCode(), tmpCodeInfoList)
			infoListList=combineList(infoListList, codeInfoList)

		return infoListList


