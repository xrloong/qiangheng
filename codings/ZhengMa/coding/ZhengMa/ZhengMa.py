from coding.Base import CodeInfo
from coding.Base import CodeInfoEncoder
from coding.Base import CodingRadixParser

class ZMCodeInfo(CodeInfo):
	def __init__(self, codes, extraCode, codesSingleton):
		super().__init__()

		self._zm_code = ''
		self._codes = codes
		self._codesSingleton = codesSingleton

		self._zm_extra = extraCode

	@staticmethod
	def generateDefaultCodeInfo(rtlist):
		codeInfo = ZMCodeInfo(rtlist, None, None)
		return codeInfo

	@property
	def code(self):
		if self._codesSingleton:
			rtlist = self._codesSingleton
			codes = self.convertRadixListToCodeList(rtlist)
			ans = self.computeCharacterCode(codes)
			return ans
		else:
			rtlist = self.getRtList()
			codes = self.convertRadixListToCodeList(rtlist)
			ans = self.computeCharacterCode(codes)
			extraCode = self.getExtraCode()
			if extraCode:
				ans += extraCode
			return ans

	def convertRadixListToCodeList(self, radixList):
		return radixList

	def computeCharacterCode(self, rtlist):
		ans = ''
		tmp_rtlist = rtlist
		if len(tmp_rtlist) == 0:
			return None
		elif len(tmp_rtlist) == 1:
			ans = rtlist[0]
		elif len(tmp_rtlist) == 2:
			if len(tmp_rtlist[0]) == 1 and len(tmp_rtlist[1]) == 1:
				ans = ''.join(rtlist[0:2])
				ans = rtlist[0][0]+rtlist[-1][0]+'vv'
			else:
				ans = (rtlist[0]+rtlist[-1])[:4]
		elif len(tmp_rtlist) == 3:
			if len(tmp_rtlist[0]) == 1:
				ans = rtlist[0][0]+rtlist[1][0]+rtlist[-1][0:2]
			elif len(tmp_rtlist[0]) == 2:
				ans = rtlist[0][0:2]+rtlist[-2][0]+rtlist[-1][0]
			elif len(tmp_rtlist[0]) == 3:
				ans = rtlist[0][0:3]+rtlist[-1][0]
			else:
				# 錯誤處理
				ans = rtlist[0][0:4]
		elif len(tmp_rtlist) >= 4:
			if len(tmp_rtlist[0]) == 1:
				ans = rtlist[0][0]+rtlist[1][0]+rtlist[-2][0]+rtlist[-1][0]
			elif len(tmp_rtlist[0]) == 2:
				ans = rtlist[0][0:2]+rtlist[-2][0]+rtlist[-1][0]
			elif len(tmp_rtlist[0]) == 3:
				ans = rtlist[0][0:3]+rtlist[-1][0]
			else:
				# 錯誤處理
				ans = rtlist[0][0:4]
		else:
			ans = ''
		return ans

	def getExtraCode(self):
		return self._zm_extra

	def getRtList(self):
		return self.getMainCodeList()


	def getMainCodeList(self):
		if self._codes != None:
			return self._codes
		return None

class ZMCodeInfoEncoder(CodeInfoEncoder):
	def generateDefaultCodeInfo(self, rtlist):
		return ZMCodeInfo.generateDefaultCodeInfo(rtlist)

	def isAvailableOperation(self, codeInfoList):
		isAllWithCode = codeInfoList and all(map(lambda x: x.getRtList(), codeInfoList))
		return isAllWithCode


	def __computeRadicalsCodes(self, codeInfos):
		codes = sum(map(lambda c: c.getRtList(), codeInfos), ())
		codes = codes if len(codes) <= 4 else codes[:2]+codes[-2:]
		return codes

	def encodeAsLoong(self, codeInfoList):
		"""運算 "龍" """

		codes = self.__computeRadicalsCodes(codeInfoList)
		codeInfo = self.generateDefaultCodeInfo(codes)
		return codeInfo


	def encodeAsHan(self, codeInfoList):
		"""運算 "爲" """
		firstCodeInfo = codeInfoList[0]
		secondCodeInfo = codeInfoList[1]
		newCodeInfoList = (secondCodeInfo, firstCodeInfo)
		codeInfo = self.encodeAsLoong(newCodeInfoList)
		return codeInfo


	def encodeAsYou(self, codeInfoList):
		"""運算 "幽" """

		firstCodeInfo = codeInfoList[0]
		secondCodeInfo = codeInfoList[1]
		thirdCodeInfo = codeInfoList[2]

		newCodeInfoList = (secondCodeInfo, thirdCodeInfo, firstCodeInfo)
		codeInfo = self.encodeAsLoong(newCodeInfoList)
		return codeInfo

	def encodeAsLiang(self, codeInfoList):
		"""運算 "㒳" """

		codes = self.__computeRadicalsCodes(codeInfoList)
		codeInfo = self.generateDefaultCodeInfo(codes[:1])
		return codeInfo

class ZMRadixParser(CodingRadixParser):
	RADIX_SEPERATOR = ','

	ATTRIB_CODE_EXPRESSION = '編碼表示式'
	ATTRIB_SUPPLEMENTARY_CODE = '補充資訊'

	# 多型
	def convertRadixDescToCodeInfo(self, radixDesc):
		codeInfo = self.convertRadixDescToCodeInfoByExpression(radixDesc)
		return codeInfo

	def convertRadixDescToCodeInfoByExpression(self, radixInfo):
		elementCodeInfo = radixInfo.codeElement

		infoDict = elementCodeInfo

		extra_code = infoDict.get(ZMRadixParser.ATTRIB_SUPPLEMENTARY_CODE)
		strCodeList = infoDict.get(ZMRadixParser.ATTRIB_CODE_EXPRESSION)

		zm_code = ''
		zm_extra = extra_code
		codes = ()
		if strCodeList != None:
			codes = tuple(strCodeList.split(ZMRadixParser.RADIX_SEPERATOR))

		# 鄭碼對「冂」內含物的形式，都統合成一個字根，如：冈、网、岡、罔
		# 如果是構成其他字的一部分，就會當成一個字根，編碼為 LD
		# 如果是要對此字根編碼，就不合成一個字根，而是使用原字根序列來編碼
		codesSingleton = ()
		if codes[0][0] == '*':
			newFirstCode = codes[0][1:]
			codesSingleton = (newFirstCode, ) + codes[1:]
			codes = (newFirstCode, )

		codeInfo = ZMCodeInfo(tuple(codes), zm_extra, tuple(codesSingleton))
		return codeInfo

