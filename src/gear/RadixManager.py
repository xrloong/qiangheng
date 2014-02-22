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
		elementCodeInfo=radixInfo.getElement()

		infoDict={}
		if elementCodeInfo is not None:
			infoDict=elementCodeInfo.attrib

		codeInfo=self.codeInfoEncoder.generateCodeInfo(infoDict, codeVariance)
		return codeInfo

	# 多型
	def setRadixDescriptionList(self, radixDescList):
		for [charName, radixDesc] in radixDescList:
			tmpRadixCodeInfoList=radixDesc.getRadixCodeInfoDescriptionList()

			radixCodeInfoList=self.radixCodeInfoDB.get(charName, [])
			for radixInfo in tmpRadixCodeInfoList:
				codeInfo=self.convertRadixInfoToCodeInfo(radixInfo)
				if codeInfo:
					radixCodeInfoList.append(codeInfo)
			self.radixCodeInfoDB[charName]=radixCodeInfoList

	# 多型
	def parseRadixDescriptionList(self, nodeCharacter):
		elementCodeInfoList=nodeCharacter.findall(Constant.TAG_CODE_INFORMATION)
		radixDescList=[]
		for elementCodeInfo in elementCodeInfoList:
			radixDesc=RadixCodeInfoDescription(elementCodeInfo)
			radixDescList.append(radixDesc)
		return RadixDescription(radixDescList)


	def getRadixCodeInfo(self, radixName):
		return self.radixCodeInfoDB.get(radixName)[0]

	def getRadixCodeInfoList(self, radixName):
		return self.radixCodeInfoDB.get(radixName)

	def hasRadix(self, radixName):
		return (radixName in self.radixCodeInfoDB)


	def loadRadix(self, toRadixList):
		allRadixDescriptionList=[]
		for filename in toRadixList:
			radixDescriptionList=self.loadRadixFromXML(filename, fileencoding=Constant.FILE_ENCODING)
			allRadixDescriptionList.extend(radixDescriptionList)

		self.setRadixDescriptionList(allRadixDescriptionList)

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

class RadixCodeInfoDescription:
	def __init__(self, elementCodeInfo):
		infoDict={}
		if elementCodeInfo is not None:
			infoDict=elementCodeInfo.attrib

		self.codeVariance=CodeVarianceType()
		self.setCodeVarianceType(infoDict)

		self.elementCodeInfo=elementCodeInfo

	def setCodeVarianceType(self, codeInfoDict):
		codeVarianceString=codeInfoDict.get(Constant.TAG_CODE_VARIANCE_TYPE, Constant.VALUE_CODE_VARIANCE_TYPE_STANDARD)
		self.codeVariance.setVarianceByString(codeVarianceString)

	def getCodeVarianceType(self):
		return self.codeVariance

	def getElement(self):
		return self.elementCodeInfo

class RadixDescription:
	def __init__(self, radixCodeInfoList):
		self.radixCodeInfoList=radixCodeInfoList

	def getRadixCodeInfoDescriptionList(self):
		return self.radixCodeInfoList

	def getRadixCodeInfoDescription(self, index):
		if index in range(leng(self.radixCodeInfoList)):
			return self.radixCodeInfoList[index]

