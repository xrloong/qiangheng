import sys
import Constant
from xml.etree import ElementTree
from parser import QHParser
from gear import OperatorManager
from gear.CodeVarianceType import CodeVarianceType
from gear.CodeInfo import CodeInfo

class RadixManager:
	def __init__(self, codeInfoEncoder):
		self.codeInfoEncoder=codeInfoEncoder
		self.radixCodeInfoDB={}

		self.radixDescDB={}

		self.operationMgr=OperatorManager.OperatorManager(self)
		self.parser=QHParser.QHParser(self.operationMgr.getOperatorGenerator())

	# 多型
	def convertRadixDescToCodeInfo(self, radixDesc):
		codeVariance=radixDesc.getCodeVarianceType()
		elementCodeInfo=radixDesc.getElement()

		infoDict={}
		if elementCodeInfo is not None:
			infoDict=elementCodeInfo.attrib

		codeInfo=self.codeInfoEncoder.generateCodeInfo(infoDict, codeVariance)
		return codeInfo

	# 多型
	def convertElementToRadixInfo(self, elementCodeInfo):
		radixInfoDescription=RadixCodeInfoDescription(elementCodeInfo)
		return radixInfoDescription

	# 多型
	def setRadixDescriptionList(self, radixDescList):
		for [charName, radixDesc] in radixDescList:
			self.radixDescDB[charName]=radixDesc

		for [charName, radixDesc] in radixDescList:
			self.convertRadixDescIntoDB(charName, radixDesc)

	# 遞迴
	def convertRadixDescIntoDB(self, charName, radixDesc):
		radixCodeInfoList=[]
		tmpRadixCodeInfoList=radixDesc.getRadixCodeInfoDescriptionList()
		for radixInfo in tmpRadixCodeInfoList:
			codeInfo=self.convertRadixDescToCodeInfo(radixInfo)
			if codeInfo:
				radixCodeInfoList.append(codeInfo)
		self.radixCodeInfoDB[charName]=radixCodeInfoList

	def parseRadixDescription(self, nodeCharacter):
		elementCodeInfoList=nodeCharacter.findall(Constant.TAG_CODE_INFORMATION)
		radixCodeInfoDescList=[]
		for elementCodeInfo in elementCodeInfoList:
			radixCodeInfoDesc=self.convertElementToRadixInfo(elementCodeInfo)
			radixCodeInfoDescList.append(radixCodeInfoDesc)
		return RadixDescription(radixCodeInfoDescList)


	def setCodeInfoAttribute(self, codeInfo, radixInfo):
		codeVariance=radixInfo.getCodeVarianceType()
		isSupportCharacterCode=radixInfo.isSupportCharacterCode()
		isSupportRadixCode=radixInfo.isSupportRadixCode()
		codeInfo.setCodeInfoAttribute(codeVariance, isSupportCharacterCode, isSupportRadixCode)

	def getMainRadixCodeInfo(self, radixName):
		return self.radixCodeInfoDB.get(radixName)[0]

	def getRadixCodeInfoList(self, radixName):
		return self.radixCodeInfoDB.get(radixName)

	def getRadixDescription(self, radixName):
		return self.radixDescDB.get(radixName)

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
			radixInfoSet=self.parseRadixDescription(characterNode)

			radixInfoList.append([charName, radixInfoSet])
		return radixInfoList

class RadixCodeInfoDescription:
	def __init__(self, elementCodeInfo):
		infoDict={}
		if elementCodeInfo is not None:
			infoDict=elementCodeInfo.attrib

		self.codeVariance=CodeVarianceType()
		self.setCodeVarianceType(infoDict)

		[isSupportCharacterCode, isSupportRadixCode]=CodeInfo.computeSupportingFromProperty(infoDict)
		self._isSupportCharacterCode=isSupportCharacterCode
		self._isSupportRadixCode=isSupportRadixCode

		self.elementCodeInfo=elementCodeInfo

	def setCodeVarianceType(self, codeInfoDict):
		codeVarianceString=codeInfoDict.get(Constant.TAG_CODE_VARIANCE_TYPE, Constant.VALUE_CODE_VARIANCE_TYPE_STANDARD)
		self.codeVariance.setVarianceByString(codeVarianceString)

	def getCodeVarianceType(self):
		return self.codeVariance

	def isSupportCharacterCode(self):
		return self._isSupportCharacterCode

	def isSupportRadixCode(self):
		return self._isSupportRadixCode

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

