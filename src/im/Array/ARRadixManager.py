from .ARCodeInfo import ARCodeInfo
from .ARCodeInfoEncoder import ARCodeInfoEncoder
from ..base.RadixManager import RadixParser
from ..base.RadixManager import RadixCodeInfoDescription

class ARRadixParser(RadixParser):
	ATTRIB_CODE_EXPRESSION='資訊表示式'
	TAG_SUB_RADIX='子字根'
	ATTRIB_USE_RADIX='使用'

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
		return codeInfo

	def convertRadixDescToCodeInfoByExpression(self, radixInfo):
		elementCodeInfo=radixInfo.getCodeElement()

		infoDict={}
		if elementCodeInfo is not None:
			infoDict=elementCodeInfo.attrib

		codeList=None

		str_rtlist=infoDict.get(ARRadixParser.ATTRIB_CODE_EXPRESSION)
		if str_rtlist!=None:
			codeList=str_rtlist.split(ARCodeInfo.INSTALLMENT_SEPERATOR)
			codeList=list(map(lambda x: x.split(ARCodeInfo.RADIX_SEPERATOR), codeList))

		codeInfo=ARCodeInfo(codeList)
		return codeInfo

	def convertRadixDescToCodeInfoByReference(self, radixDesc):
		nameList=radixDesc.getRadixNameList()

		codeList=[]
		for radixName in nameList:
			radixDesc=self.getRadixDescription(radixName)
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
		subRadixNodeList=elementCodeInfo.findall(ARRadixParser.TAG_SUB_RADIX)
		for subRadixNode in subRadixNodeList:
			radixName=subRadixNode.attrib.get(ARRadixParser.ATTRIB_USE_RADIX)
			radixNameList.append(radixName)

		self.radixNameList=radixNameList

	def getRadixNameList(self):
		return self.radixNameList

	def isWithExpression(self):
		codeExpressionNode=self.getCodeElement()
		return codeExpressionNode!=None

