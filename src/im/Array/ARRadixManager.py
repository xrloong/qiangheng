from .ARCodeInfo import ARCodeInfo
from .ARCodeInfoEncoder import ARCodeInfoEncoder
from ..base.RadixManager import RadixParser
from ..base.RadixManager import RadixCodeInfoDescription
import Constant

class ARRadixParser(RadixParser):
	# 多型
	def convertElementToRadixInfo(self, elementCodeInfo):
		radixInfoDescription=ARRadixCodeInfoDescription(elementCodeInfo)
		return radixInfoDescription

	# 多型
	def convertRadixDescToCodeInfo(self, radixDesc):
		if(radixDesc.isWithExpression()):
			codeInfo=self.convertRadixDescToCodeInfoByExpression(radixDesc)
		else:
			codeInfo=self.convertRadixDescToCodeInfoByReference(radixDesc)

		self.setCodeInfoAttribute(codeInfo, radixDesc)
		return codeInfo

	def convertRadixDescToCodeInfoByExpression(self, radixInfo):
		elementCodeInfo=radixInfo.getElement()

		infoDict={}
		if elementCodeInfo is not None:
			infoDict=elementCodeInfo.attrib

		codeList=None
		str_rtlist=infoDict.get(Constant.ATTRIB_CODE_EXPRESSION)
		if str_rtlist!=None:
			codeList=str_rtlist.split(ARCodeInfo.INSTALLMENT_SEPERATOR)
			codeList=list(map(lambda x: x.split(ARCodeInfo.RADIX_SEPERATOR), codeList))

		codeInfo=ARCodeInfo(codeList)
		return codeInfo

	def convertRadixDescToCodeInfoByReference(self, radixDesc):
		nameList=radixDesc.getRadixNameList()

		codeList=[]
		for radixName in nameList:
			radixDesc=self.radixDescriptionManager.getReferenceDescription(radixName)
			radixCodeInfoList=self.convertRadixDescToCodeInfoList(radixDesc)

			radixInfo=radixCodeInfoList[0]
			radixCodeList=radixInfo.getMainCodeList()
			codeList.append(radixCodeList)

		codeInfo=ARCodeInfo(codeList)
		return codeInfo

class ARRadixCodeInfoDescription(RadixCodeInfoDescription):
	def __init__(self, elementCodeInfo):
		RadixCodeInfoDescription.__init__(self, elementCodeInfo)

		radixNameList=[]
		subRadixNodeList=elementCodeInfo.findall(Constant.TAG_SUB_RADIX)
		for subRadixNode in subRadixNodeList:
			radixName=subRadixNode.attrib.get(Constant.ATTRIB_USE_RADIX)
			radixNameList.append(radixName)

		self.radixNameList=radixNameList

	def getRadixNameList(self):
		return self.radixNameList

	def isWithExpression(self):
		elementCodeInfo=self.getElement()

		infoDict={}
		if elementCodeInfo is not None:
			infoDict=elementCodeInfo.attrib
		return (Constant.ATTRIB_CODE_EXPRESSION in infoDict)

