from .CodeInfo import CodeInfo
from .CodeInfoEncoder import CodeInfoEncoder

import Constant
from xml.etree import ElementTree
from ..gear import OperatorManager
from ..gear.CharacterDescriptionRearranger import CharacterDescriptionRearranger
from gear.CodeVarianceType import CodeVarianceType

class RadixParser:
	def __init__(self, nameInputMethod, codeInfoEncoder):
		self.nameInputMethod=nameInputMethod
		self.codeInfoEncoder=codeInfoEncoder

		self.radixCodeInfoDB={}
		self.radixDescDB={}


	def loadRadix(self, radixFileList):
		self.parseRadixDescriptionList(radixFileList)
		return self.radixCodeInfoDB


	def getEncoder(self):
		return self.codeInfoEncoder

	def getRadixCodeInfoList(self, radixName):
		return self.radixCodeInfoDB.get(radixName)


	def setCodeInfoAttribute(self, codeInfo, radixInfo):
		codeVariance=radixInfo.getCodeVarianceType()
		isSupportCharacterCode=radixInfo.isSupportCharacterCode()
		isSupportRadixCode=radixInfo.isSupportRadixCode()
		codeInfo.setCodeInfoAttribute(codeVariance, isSupportCharacterCode, isSupportRadixCode)

	def setRadixDescriptionList(self, radixDescList):
		for [charName, radixDesc] in radixDescList:
			self.radixDescDB[charName]=radixDesc

		for [charName, radixDesc] in radixDescList:
			self.convertRadixDescIntoDB(charName, radixDesc)

	def convertRadixDescIntoDB(self, charName, radixDesc):
		radixCodeInfoList=[]
		tmpRadixCodeInfoList=radixDesc.getRadixCodeInfoDescriptionList()
		for radixInfo in tmpRadixCodeInfoList:
			codeInfo=self.convertRadixDescToCodeInfo(radixInfo)
			if codeInfo:
				radixCodeInfoList.append(codeInfo)
		self.radixCodeInfoDB[charName]=radixCodeInfoList

	# 多型
	def convertElementToRadixInfo(self, elementCodeInfo):
		radixInfoDescription=RadixCodeInfoDescription(elementCodeInfo)
		return radixInfoDescription

	# 多型
	def convertRadixDescToCodeInfo(self, radixDesc):
		codeVariance=radixDesc.getCodeVarianceType()
		elementCodeInfo=radixDesc.getElement()

		infoDict={}
		if elementCodeInfo is not None:
			infoDict=elementCodeInfo.attrib

		codeInfo=CodeInfo()

		self.setCodeInfoAttribute(codeInfo, radixDesc)
		return codeInfo

	def parseRadixDescriptionList(self, toRadixList):
		allRadixDescriptionList=[]
		for filename in toRadixList:
			radixDescriptionList=self.parseRadixFromXML(filename, fileencoding=Constant.FILE_ENCODING)
			allRadixDescriptionList.extend(radixDescriptionList)

		radixDescriptionList=allRadixDescriptionList
		tmpDict={}
		for [charName, radixDesc] in radixDescriptionList:
			if charName in tmpDict:
				tmpRadixDesc=tmpDict.get(charName)
			else:
				tmpRadixDesc=RadixDescription([])
			tmpRadixDesc.mergeRadixDescription(radixDesc)
			tmpDict[charName]=tmpRadixDesc

		allRadixDescriptionList=list(tmpDict.items())

		self.setRadixDescriptionList(allRadixDescriptionList)

	def parseRadixFromXML(self, filename, fileencoding=Constant.FILE_ENCODING):
		f=open(filename, encoding=fileencoding)
		xmlNode=ElementTree.parse(f)
		rootNode=xmlNode.getroot()

		self.checkFileType(rootNode)
		self.checkInputMethod(rootNode)

		radixInfoList=self.parseRadixInfo(rootNode)
		return radixInfoList

	def parseRadixInfo(self, rootNode):
		characterSetNode=rootNode.find(Constant.TAG_CHARACTER_SET)
		characterNodeList=characterSetNode.findall(Constant.TAG_CHARACTER)
		radixInfoList=[]
		for characterNode in characterNodeList:
			charName=characterNode.get(Constant.TAG_NAME)
			radixInfoSet=self.parseRadixDescription(characterNode)

			radixInfoList.append([charName, radixInfoSet])
		return radixInfoList

	def parseRadixDescription(self, nodeCharacter):
		elementCodeInfoList=nodeCharacter.findall(Constant.TAG_CODE_INFORMATION)
		radixCodeInfoDescList=[]
		for elementCodeInfo in elementCodeInfoList:
			radixCodeInfoDesc=self.convertElementToRadixInfo(elementCodeInfo)
			radixCodeInfoDescList.append(radixCodeInfoDesc)
		return RadixDescription(radixCodeInfoDescList)


	def checkFileType(self, rootNode):
		fileType=rootNode.get(Constant.TAG_FILE_TYPE)
		assert fileType==Constant.TAG_FILE_TYPE_RADIX, \
			"文字類型錯誤，預期為＜字根＞，實際為＜%s＞。"%(fileType)

	def checkInputMethod(self, rootNode):
		nameInputMethod=rootNode.get(Constant.TAG_INPUT_METHOD)
		assert nameInputMethod==self.nameInputMethod, \
			"輸入法錯誤，預期為＜%s＞，實際為＜%s＞。"%(self.nameInputMethod, nameInputMethod)

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

	def mergeRadixDescription(self, radixDesc):
		radixCodeInfoList=radixDesc.getRadixCodeInfoDescriptionList()
		self.radixCodeInfoList.extend(radixCodeInfoList)

