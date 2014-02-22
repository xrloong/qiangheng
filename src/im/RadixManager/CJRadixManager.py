

import Constant
from im.CodeInfo.CJCodeInfo import CJCodeInfo
from gear.RadixManager import RadixManager
class CJRadixManager(RadixManager):
	def __init__(self, codeInfoEncoder):
		RadixManager.__init__(self, codeInfoEncoder)

	# 多型
	def convertRadixDescToCodeInfo(self, radixDesc):
		codeInfo=self.convertRadixDescToCodeInfoByExpression(radixDesc)

		self.setCodeInfoAttribute(codeInfo, radixDesc)
		return codeInfo

	def convertRadixDescToCodeInfoByExpression(self, radixInfo):
		elementCodeInfo=radixInfo.getElement()

		infoDict={}
		if elementCodeInfo is not None:
			infoDict=elementCodeInfo.attrib

		direction='*'
		singleCode=infoDict.get('獨體編碼')
		rtlist=[]
		str_rtlist=infoDict.get('資訊表示式')
		if str_rtlist!=None:
			rtlist=str_rtlist.split(CJCodeInfo.RADIX_SEPERATOR)

		if str_rtlist in CJCodeInfo.radixToCodeDict:
			# work around
			direction=CJCodeInfo.radixToCodeDict[str_rtlist][0]

		cjBody=CJCodeInfo.computeBodyCode(rtlist, direction)
		codeInfo=CJCodeInfo(singleCode, direction, rtlist, cjBody)

		return codeInfo

