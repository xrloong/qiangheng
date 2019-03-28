from .CodeInfo import CodeInfo

import Constant
from model import OperatorManager
from model.element.CodeVarianceType import CodeVarianceTypeFactory

import yaml

class RadixParser:
	TAG_CODE_INFORMATION='編碼資訊'
	TAG_CODE='編碼'

	def __init__(self, nameInputMethod, codeInfoEncoder, imRadixParser):
		self.nameInputMethod=nameInputMethod
		self.codeInfoEncoder=codeInfoEncoder
		self.imRadixParser=imRadixParser

		self.radixCodeInfoDB={}

		self.radixDescriptionManager=self.createRadixDescriptionManager()

	def loadRadix(self, radixFileList):
		self.parse(radixFileList)

		self.convert()
		return (self.radixDescriptionManager.getResetRadixList(), self.radixDescriptionManager.getCodeInfoDB())


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
		codeInfo=self.imRadixParser.convertRadixDescToCodeInfo(radixDesc)

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
		rootNode=yaml.load(open(filename), Loader=yaml.SafeLoader)

		self.parseRadixInfo(rootNode)

	def parseRadixInfo(self, rootNode):
		characterSetNode=rootNode.get(Constant.TAG_CHARACTER_SET)
		for characterNode in characterSetNode:
			charName=characterNode.get(Constant.TAG_NAME)
			radixDescription=self.parseRadixDescription(characterNode)

			self.radixDescriptionManager.addDescription(charName, radixDescription)

	def parseRadixDescription(self, nodeCharacter):
		radixCodeInfoDescList=[]
		toOverridePrev=("是" == nodeCharacter.get("覆蓋"))
		for elementCodeInfo in nodeCharacter.get(RadixParser.TAG_CODE_INFORMATION):
			radixCodeInfoDesc=self.convertElementToRadixInfo(elementCodeInfo)
			radixCodeInfoDescList.append(radixCodeInfoDesc)
		return RadixDescription(radixCodeInfoDescList, toOverridePrev)

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
	def __init__(self, radixCodeInfoList, toOverride=True):
		self.radixCodeInfoList=radixCodeInfoList
		self.toOverridePrev=toOverride

	def isToOverridePrev(self):
		return self.toOverridePrev

	def getRadixCodeInfoDescriptionList(self):
		return self.radixCodeInfoList

	def getRadixCodeInfoDescription(self, index):
		if index in range(leng(self.radixCodeInfoList)):
			return self.radixCodeInfoList[index]

	def mergeRadixDescription(self, radixDesc):
		radixCodeInfoList=radixDesc.getRadixCodeInfoDescriptionList()
		self.radixCodeInfoList.extend(radixCodeInfoList)

