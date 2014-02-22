import sys
import Constant
from xml.etree import ElementTree
from gear import OperatorManager
from parser import QHParser
from gear.CodeVarianceType import CodeVarianceType

class RadixManager:
	def __init__(self, codeInfoEncoder):
		self.codeInfoEncoder=codeInfoEncoder
		self.radixCodeInfoDB={}

		self.operationMgr=OperatorManager.OperatorManager(self)
		self.parser=QHParser.QHParser(self.operationMgr.getOperatorGenerator())

	# 多型
	def convertRadixInfoToCodeInfo(self, radixInfo):
		codeVariance=radixInfo.getCodeVarianceType()
		codeInfoProperties=radixInfo.getCodeInfoDict()
		codeInfo=self.codeInfoEncoder.generateCodeInfo(codeInfoProperties)
		codeInfo.multiplyCodeVarianceType(codeVariance)
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

	# 多型
	def parseRadixDescriptionList(self, nodeCharacter):
		nodeCodeInfoList=nodeCharacter.findall(Constant.TAG_CODE_INFORMATION)
		radixDescList=[]
		for nodeCodeInfo in nodeCodeInfoList:
			infoDict={}
			if nodeCodeInfo is not None:
				infoDict=nodeCodeInfo.attrib

			radixDesc=RadixDescription(infoDict)

			radixDescList.append(radixDesc)
		return radixDescList


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
			radixInfoSet=self.parseRadixDescriptionList(characterNode)

			radixInfoList.append([charName, radixInfoSet])
		return radixInfoList

class RadixDescription:
	def __init__(self, codeInfoDict):
		self.codeVariance=CodeVarianceType()
		self.setCodeVarianceType(codeInfoDict)
		self.codeInfoDict=codeInfoDict

	def setCodeVarianceType(self, codeInfoDict):
		codeVarianceString=codeInfoDict.get(Constant.TAG_CODE_VARIANCE_TYPE, Constant.VALUE_CODE_VARIANCE_TYPE_STANDARD)
		self.codeVariance.setVarianceByString(codeVarianceString)

	def getCodeVarianceType(self):
		return self.codeVariance

	def getCodeInfoDict(self):
		return self.codeInfoDict

