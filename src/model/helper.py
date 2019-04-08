from injector import inject

from coding.Base import CodeInfo

from .element.StructureDescription import StructureDescription
from .element.CodeVarianceType import CodeVarianceTypeFactory
from .manager import OperatorManager


import Constant

class StructureDescriptionGenerator:
	@inject
	def __init__(self, operationManager: OperatorManager):
		self.operationManager = operationManager

	def generateLeafNode(self, nodeExpression):
		structDesc=self.generateNode()
		structDesc.setReferenceExpression(nodeExpression)
		structDesc.generateName()
		return structDesc

	def generateNode(self, structInfo=['龜', []]):
		operatorName, compList=structInfo
		operator=self.operationManager.generateOperator(operatorName)
		structDesc=StructureDescription(operator, compList)
		structDesc.generateName()
		return structDesc

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
	def __init__(self, radixName, radixCodeInfoList, toOverride=True):
		self.radixName=radixName
		self.radixCodeInfoList=radixCodeInfoList
		self.toOverridePrev=toOverride

	def isToOverridePrev(self):
		return self.toOverridePrev

	def getRadixName(self):
		return self.radixName

	def getRadixCodeInfoDescriptionList(self):
		return self.radixCodeInfoList

	def getRadixCodeInfoDescription(self, index):
		if index in range(leng(self.radixCodeInfoList)):
			return self.radixCodeInfoList[index]

	def mergeRadixDescription(self, radixDesc):
		radixCodeInfoList=radixDesc.getRadixCodeInfoDescriptionList()
		self.radixCodeInfoList.extend(radixCodeInfoList)


