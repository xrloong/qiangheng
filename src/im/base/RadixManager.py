from .CodeInfo import CodeInfo
from .CodeInfoEncoder import CodeInfoEncoder

import Constant
#from xml.etree import ElementTree as ET
from xml.etree import cElementTree as ET
#import lxml.etree as ET
#import lxml.objectify as ET
from ..gear import OperatorManager
from gear.CodeVarianceType import CodeVarianceTypeFactory

import yaml

class RadixParser:
	TAG_CODE_INFORMATION='編碼資訊'
	TAG_CODE='編碼'

	def __init__(self, nameInputMethod, codeInfoEncoder):
		self.nameInputMethod=nameInputMethod
		self.codeInfoEncoder=codeInfoEncoder

		self.radixCodeInfoDB={}

		self.radixDescriptionManager=self.createRadixDescriptionManager()

	def loadRadix(self, radixFileList):
		self.parse(radixFileList)

		self.convert()
		return self.radixDescriptionManager.getCodeInfoDB()


	def getEncoder(self):
		return self.codeInfoEncoder


	def createRadixDescriptionManager(self):
		return RadixDescriptionManager()


	def getRadixDescription(self, radixName):
		return self.radixDescriptionManager.getDescription(radixName)


	def convert(self):
		radixDescList=self.radixDescriptionManager.getDescriptionList()

		for [charName, radixDesc] in radixDescList:
			radixCodeInfoList=self.convertRadixDescToCodeInfoList(radixDesc)
			self.radixDescriptionManager.addCodeInfoList(charName, radixCodeInfoList)

	def convertRadixDescToCodeInfoList(self, radixDesc):
		radixCodeInfoList=[]
		tmpRadixCodeInfoList=radixDesc.getRadixCodeInfoDescriptionList()
		for radixInfo in tmpRadixCodeInfoList:
			codeInfo=self.convertRadixDescToCodeInfoWithAttribute(radixInfo)
			if codeInfo:
				radixCodeInfoList.append(codeInfo)
		return radixCodeInfoList

	def convertRadixDescToCodeInfoWithAttribute(self, radixDesc):
		codeInfo=self.convertRadixDescToCodeInfo(radixDesc)

		codeVariance=radixDesc.getCodeVarianceType()
		isSupportCharacterCode=radixDesc.isSupportCharacterCode()
		isSupportRadixCode=radixDesc.isSupportRadixCode()
		codeInfo.setCodeInfoAttribute(codeVariance, isSupportCharacterCode, isSupportRadixCode)

		return codeInfo

	def convertElementToRadixInfo(self, elementCodeInfo):
		infoDict={}
		if elementCodeInfo is not None:
			infoDict=elementCodeInfo.attrib

		codeElementCodeInfo=elementCodeInfo.find(RadixParser.TAG_CODE)
		radixInfoDescription=RadixCodeInfoDescription(infoDict, codeElementCodeInfo)
		return radixInfoDescription

	# 多型
	def convertRadixDescToCodeInfo(self, radixDesc):
		codeInfo=CodeInfo()
		return codeInfo

	def parse(self, toRadixList):
		for filename in toRadixList:
			self.parseRadixFromXML(filename)

	def parseRadixFromXML(self, filename):
		xmlNode=ET.parse(filename)
		rootNode=xmlNode.getroot()

		fileType=self.parseFileType(rootNode)
		assert fileType==Constant.TAG_FILE_TYPE_RADIX, \
			"文字類型錯誤，預期為＜字根＞，實際為＜%s＞。"%(fileType)

		nameInputMethod=self.parseInputMethod(rootNode)
		assert nameInputMethod==self.nameInputMethod, \
			"輸入法錯誤，預期為＜%s＞，實際為＜%s＞。"%(self.nameInputMethod, nameInputMethod)

		self.parseRadixInfo(rootNode)

	def parseRadixInfo(self, rootNode):
		characterSetNode=rootNode.find(Constant.TAG_CHARACTER_SET)
		characterNodeList=characterSetNode.findall(Constant.TAG_CHARACTER)
		for characterNode in characterNodeList:
			charName=characterNode.get(Constant.TAG_NAME)
			radixDescription=self.parseRadixDescription(characterNode)

			self.radixDescriptionManager.addDescription(charName, radixDescription)

	def parseRadixDescription(self, nodeCharacter):
		elementCodeInfoList=nodeCharacter.findall(RadixParser.TAG_CODE_INFORMATION)
		radixCodeInfoDescList=[]
		for elementCodeInfo in elementCodeInfoList:
			radixCodeInfoDesc=self.convertElementToRadixInfo(elementCodeInfo)
			radixCodeInfoDescList.append(radixCodeInfoDesc)
		return RadixDescription(radixCodeInfoDescList)


	def parseFileType(self, rootNode):
		fileType=rootNode.get(Constant.TAG_FILE_TYPE)
		return fileType

	def parseInputMethod(self, rootNode):
		nameInputMethod=rootNode.get(Constant.TAG_INPUT_METHOD)
		return nameInputMethod

class RadixParserYAML:
	TAG_CODE_INFORMATION='編碼資訊'
	TAG_CODE='編碼'

	def __init__(self, nameInputMethod, codeInfoEncoder):
		self.nameInputMethod=nameInputMethod
		self.codeInfoEncoder=codeInfoEncoder

		self.radixCodeInfoDB={}

		self.radixDescriptionManager=self.createRadixDescriptionManager()

	def loadRadix(self, radixFileList):
		self.parse(radixFileList)

		self.convert()
		return self.radixDescriptionManager.getCodeInfoDB()


	def getEncoder(self):
		return self.codeInfoEncoder


	def createRadixDescriptionManager(self):
		return RadixDescriptionManager()


	def getRadixDescription(self, radixName):
		return self.radixDescriptionManager.getDescription(radixName)


	def convert(self):
		radixDescList=self.radixDescriptionManager.getDescriptionList()

		for [charName, radixDesc] in radixDescList:
			radixCodeInfoList=self.convertRadixDescToCodeInfoList(radixDesc)
			self.radixDescriptionManager.addCodeInfoList(charName, radixCodeInfoList)

	def convertRadixDescToCodeInfoList(self, radixDesc):
		radixCodeInfoList=[]
		tmpRadixCodeInfoList=radixDesc.getRadixCodeInfoDescriptionList()
		for radixInfo in tmpRadixCodeInfoList:
			codeInfo=self.convertRadixDescToCodeInfoWithAttribute(radixInfo)
			if codeInfo:
				radixCodeInfoList.append(codeInfo)
		return radixCodeInfoList

	def convertRadixDescToCodeInfoWithAttribute(self, radixDesc):
		codeInfo=self.convertRadixDescToCodeInfo(radixDesc)

		codeVariance=radixDesc.getCodeVarianceType()
		isSupportCharacterCode=radixDesc.isSupportCharacterCode()
		isSupportRadixCode=radixDesc.isSupportRadixCode()
		codeInfo.setCodeInfoAttribute(codeVariance, isSupportCharacterCode, isSupportRadixCode)

		return codeInfo

	def convertElementToRadixInfo(self, elementCodeInfo):
		infoDict={}
		if elementCodeInfo is not None:
			infoDict=elementCodeInfo

		codeElementCodeInfo=elementCodeInfo
		radixInfoDescription=RadixCodeInfoDescription(infoDict, codeElementCodeInfo)
		return radixInfoDescription

	# 多型
	def convertRadixDescToCodeInfo(self, radixDesc):
		codeInfo=CodeInfo()
		return codeInfo

	def parse(self, toRadixList):
		for filename in toRadixList:
			self.parseRadixFromYAML(filename)

	def parseRadixFromYAML(self, filename):
		rootNode=yaml.load(open(filename))

#		fileType=self.parseFileType(rootNode)
#		assert fileType==Constant.TAG_FILE_TYPE_RADIX, \
#			"文字類型錯誤，預期為＜字根＞，實際為＜%s＞。"%(fileType)

#		nameInputMethod=self.parseInputMethod(rootNode)
#		assert nameInputMethod==self.nameInputMethod, \
#			"輸入法錯誤，預期為＜%s＞，實際為＜%s＞。"%(self.nameInputMethod, nameInputMethod)

		self.parseRadixInfo(rootNode)

	def parseRadixInfo(self, rootNode):
		characterSetNode=rootNode.get(Constant.TAG_CHARACTER_SET)
		for characterNode in characterSetNode:
			charName=characterNode.get(Constant.TAG_NAME)
			radixDescription=self.parseRadixDescription(characterNode)

			self.radixDescriptionManager.addDescription(charName, radixDescription)

	def parseRadixDescription(self, nodeCharacter):
		radixCodeInfoDescList=[]
		for elementCodeInfo in nodeCharacter.get(RadixParser.TAG_CODE_INFORMATION):
			radixCodeInfoDesc=self.convertElementToRadixInfo(elementCodeInfo)
			radixCodeInfoDescList.append(radixCodeInfoDesc)
		return RadixDescription(radixCodeInfoDescList)

	def parseFileType(self, rootNode):
		fileType=rootNode.get(Constant.TAG_FILE_TYPE)
		return fileType

	def parseInputMethod(self, rootNode):
		nameInputMethod=rootNode.get(Constant.TAG_INPUT_METHOD)
		return nameInputMethod

class RadixDescriptionManager:
	def __init__(self):
		self.descriptionDict={}
		self.radixCodeInfoDB={}
		self.radixDescDB={}

	def addCodeInfoList(self, charName, radixCodeInfoList):
		self.radixCodeInfoDB[charName]=radixCodeInfoList

	def getCodeInfoList(self, charName):
		return self.radixCodeInfoDB[charName]

	def getCodeInfoDB(self):
		return self.radixCodeInfoDB

	def addDescription(self, charName, description):
		if charName in self.descriptionDict:
			tmpRadixDesc=self.descriptionDict.get(charName)
		else:
			tmpRadixDesc=RadixDescription([])
		tmpRadixDesc.mergeRadixDescription(description)
		self.descriptionDict[charName]=tmpRadixDesc
		self.radixDescDB[charName]=tmpRadixDesc

	def getDescriptionList(self):
		return list(self.descriptionDict.items())

	def getDescription(self, radixName):
		return self.radixDescDB[radixName]

class RadixCodeInfoDescription:
	def __init__(self, infoDict, codeElementCodeInfo):
		self.codeVariance=CodeVarianceTypeFactory.generate()
		self.codeElementCodeInfo=codeElementCodeInfo

		self.setupCodeAttribute(infoDict)

	def setupCodeAttribute(self, infoDict):
		codeVarianceString=infoDict.get(Constant.TAG_CODE_VARIANCE_TYPE, Constant.VALUE_CODE_VARIANCE_TYPE_STANDARD)
		self.setCodeVarianceType(codeVarianceString)

		[isSupportCharacterCode, isSupportRadixCode]=CodeInfo.computeSupportingFromProperty(infoDict)
		self.setSupportCode(isSupportCharacterCode, isSupportRadixCode)

	def setSupportCode(self, isSupportCharacterCode, isSupportRadixCode):
		self._isSupportCharacterCode=isSupportCharacterCode
		self._isSupportRadixCode=isSupportRadixCode

	def setCodeVarianceType(self, codeVarianceString):
		self.codeVariance=CodeVarianceTypeFactory.generateByString(codeVarianceString)

	def getCodeVarianceType(self):
		return self.codeVariance

	def isSupportCharacterCode(self):
		return self._isSupportCharacterCode

	def isSupportRadixCode(self):
		return self._isSupportRadixCode

	def getCodeElement(self):
		return self.codeElementCodeInfo

class RadixDescription:
	def __init__(self, radixCodeInfoList):
		self.radixCodeInfoList=radixCodeInfoList

	def getRadixCodeInfoDescriptionList(self):
		return self.radixCodeInfoList

	def getRadixCodeInfoDescription(self, index):
		if index in range(leng(self.radixCodeInfoList)):
			return self.radixCodeInfoList[index]

	def mergeRadixDescription(self, radixDesc):
		radixCodeInfoList=radixDesc.getRadixCodeInfoDescriptionList()
		self.radixCodeInfoList.extend(radixCodeInfoList)

