from . import HanZiCodeInfo

class HanZiStructure:
	def __init__(self):
		pass

	def getNodeList(self):
		return []

	def getCodeInfoList(self):
		return []

	def setCompositions(self):
		pass

class HanZiUnitStructure(HanZiStructure):
	def __init__(self, codeType, codeInfoProperties):
		codeInfo=HanZiCodeInfo.HanZiCodeInfo(codeInfoProperties, codeType)
		self.codeInfoList=[codeInfo]

	def getNodeList(self):
		return []

	def getCodeInfoList(self):
		return self.codeInfoList

	def setCompositions(self):
		pass

class HanZiWrapperStructure(HanZiStructure):
	def __init__(self, referenceNode, expression):
		self.referenceNode=referenceNode
		self.expression=expression

	def getCodeInfoList(self):
		return self.getTargetNode().getCodeInfoList()

	def getNodeList(self):
		return [self.referenceNode]

	def setCompositions(self):
		struct=self.getTargetStructure()
		struct.setCompositions()

	def getTargetStructure(self):
		struct=self.referenceNode.getFirstStructure()
		return struct

	def getTargetNode(self):
		tempList=self.expression.split(".")
		if(len(tempList)>1):
			index=int(tempList[1])

			struct=self.getTargetStructure()
			nodeList=struct.getNodeList()

			return nodeList[index]
		else:
			return self.referenceNode

class HanZiAssemblageStructure(HanZiStructure):
	def __init__(self, codeType, operator, nodeList):
		self.operator=operator
		self.nodeList=nodeList
		self.structureList=map(lambda node: node.getFirstStructure(), nodeList)

		self.codeInfoList=[]
		self.codeType=codeType

		self.flagIsSet=False

	def getNodeList(self):
		return self.nodeList

	def getCodeInfoList(self):
		return self.codeInfoList

	def setCompositions(self):
		if self.flagIsSet:
			return

		self.flagIsSet=True

		infoListList=HanZiAssemblageStructure.getAllCodeInfoListFromNodeList(self.structureList)

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


