import sys
import Constant
from xml.etree import ElementTree
from gear import OperatorManager
from parser import QHParser
from description.StructureDescription import TurtleStructureDescription

class RadixManager:
	def __init__(self, codeInfoEncoder):
		self.codeInfoEncoder=codeInfoEncoder
		self.radixCodeInfoDB={}

		self.operationMgr=OperatorManager.OperatorManager(self)
		self.parser=QHParser.QHParser(self.operationMgr.getOperatorGenerator())

	# 多型
	def parseToRadixInfoSet(self, characterNode):
		structDescList=self.getDesc_TurtleCharacterList(characterNode)
		radixInfoSet=structDescList
		return radixInfoSet

	# 多型
	def convertRadixInfoToCodeInfo(self, radixInfo):
		structDesc=radixInfo
		if structDesc.isTurtle():
			codeVariance=structDesc.getCodeVarianceType()
			codeInfoProperties=structDesc.getCodeInfoDict()
			codeInfo=self.codeInfoEncoder.generateCodeInfo(codeInfoProperties)
			codeInfo.multiplyCodeVarianceType(codeVariance)
		else:
			print("型態錯誤", file=sys.stderr)
			codeInfo=None
		return codeInfo

	# 多型
	def setRadixInfoList(self, radixInfoList):
		for [charName, radixInfoSet] in radixInfoList:
			radixCodeInfoList=[]
			for radixInfo in radixInfoSet:
				codeInfo=self.convertRadixInfoToCodeInfo(radixInfo)
				if codeInfo:
					radixCodeInfoList.append(codeInfo)
			oldRadixCodeInfoList=self.radixCodeInfoDB.get(charName, [])
			oldRadixCodeInfoList.extend(radixCodeInfoList)
			self.radixCodeInfoDB[charName]=oldRadixCodeInfoList


	def getRadixCodeInfo(self, radixName):
		return self.radixCodeInfoDB.get(radixName)[0]

	def getRadixCodeInfoList(self, radixName):
		return self.radixCodeInfoDB.get(radixName)

	def hasRadix(self, radixName):
		return (radixName in self.radixCodeInfoDB)


	def loadRadix(self, toRadixList):
		allRadixInfoList=[]
		for filename in toRadixList:
			radixInfoList=self.loadRadixFromXML(filename, fileencoding=Constant.FILE_ENCODING)
			allRadixInfoList.extend(radixInfoList)

		self.setRadixInfoList(allRadixInfoList)

	def loadRadixFromXML(self, filename, fileencoding=Constant.FILE_ENCODING):
		f=open(filename, encoding=fileencoding)
		xmlNode=ElementTree.parse(f)
		rootNode=xmlNode.getroot()

		radixInfoList=self.loadRadixInfo(rootNode)
		return radixInfoList

	def loadRadixInfo(self, rootNode):
		characterSetNode=rootNode.find(Constant.TAG_CHARACTER_SET)
		characterNodeList=characterSetNode.findall(Constant.TAG_CHARACTER)
		radixInfoList=[]
		for characterNode in characterNodeList:
			charName=characterNode.get(Constant.TAG_NAME)
			structureList=self.parseToRadixInfoSet(characterNode)

			radixInfoList.append([charName, structureList])
		return radixInfoList

	def getDesc_TurtleCharacterList(self, nodeCharacter):
		nodeCodeInfoList=nodeCharacter.findall(Constant.TAG_CODE_INFORMATION)
		turtleList=[]
		for nodeCodeInfo in nodeCodeInfoList:
			infoDict=None
			if nodeCodeInfo is not None:
				infoDict=nodeCodeInfo.attrib

			turtle=TurtleStructureDescription(infoDict)
			turtle.setStructureProperties(nodeCodeInfo.attrib)

			turtleList.append(turtle)
		return turtleList

