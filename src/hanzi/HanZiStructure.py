import sys
from . import HanZiCodeInfo

class HanZiStructure:
	def __init__(self):
		pass

	def getStructureList(self):
		return []

	def getCodeInfoList(self):
		return []

	def setCompositions(self):
		pass

	def printAllCodeInfo(self):
		for codeInfo in self.getCodeInfoList():
			pass

class HanZiUnitStructure(HanZiStructure):
	def __init__(self, codeType, codeInfoProperties):
		codeInfo=HanZiCodeInfo.HanZiCodeInfo(codeInfoProperties, codeType)
		self.codeInfoList=[codeInfo]

	def getStructureList(self):
		return []

	def getCodeInfoList(self):
		return self.codeInfoList

	def setCompositions(self):
		pass

class HanZiWrapperStructure(HanZiStructure):
	def __init__(self, referenceNode, expression):
		self.referenceNode=referenceNode
		self.expression=expression
		self.codeInfoList=[]

	def getStructureList(self):
		return self.getTargetStructureList()

	def getCodeInfoList(self):
		codeInfoList=[]
		for structure in self.getStructureList():
			codeInfoList.extend(structure.getCodeInfoList())
		return codeInfoList

	def setCompositions(self):
		self.referenceNode.setNodeTree()

	def getReferenceNode(self):
		return self.referenceNode

	def getExpression(self):
		return self.expression

	def getTargetStructureList(self):
		tempList=self.expression.split(".")
		if(len(tempList)>1):
			referenceName=tempList[0]
			index=int(tempList[1])
			structureList=self.referenceNode.getSubStructureList(index)
		else:
			structureList=self.referenceNode.getStructureList()
		return structureList

class HanZiAssemblageStructure(HanZiStructure):
	def __init__(self, codeType, operator, structureList):
		self.operator=operator
		self.structureList=structureList

		self.codeInfoList=[]
		self.codeType=codeType

		self.flagIsSet=False

	def getStructureList(self):
		return self.structureList

	def getCodeInfoList(self):
		return self.codeInfoList

	def setCompositions(self):
		if self.flagIsSet:
			return

		self.flagIsSet=True

		structureList=self.structureList
		for structure in structureList:
			structure.setCompositions()

		infoListList=HanZiAssemblageStructure.getAllCodeInfoListFromNodeList(structureList)

		for infoList in infoListList:
			codeInfo=HanZiCodeInfo.HanZiCodeInfo({}, self.codeType)
			codeInfo.setCompositions(self.operator, infoList)

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


