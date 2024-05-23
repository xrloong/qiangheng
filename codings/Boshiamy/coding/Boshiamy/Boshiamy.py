from coding.Base import CodeInfo
from coding.Base import CodeInfoEncoder
from coding.Base import CodingRadixParser

class BSCodeInfo(CodeInfo):
	RADIX_A = 'a'
	RADIX_B = 'b'
	RADIX_C = 'c'
	RADIX_D = 'd'
	RADIX_E = 'e'
	RADIX_F = 'f'
	RADIX_G = 'g'
	RADIX_H = 'h'
	RADIX_I = 'i'
	RADIX_J = 'j'
	RADIX_K = 'k'
	RADIX_L = 'l'
	RADIX_M = 'm'
	RADIX_N = 'n'
	RADIX_O = 'o'
	RADIX_P = 'p'
	RADIX_Q = 'q'
	RADIX_R = 'r'
	RADIX_S = 's'
	RADIX_T = 't'
	RADIX_U = 'u'
	RADIX_V = 'v'
	RADIX_W = 'w'
	RADIX_X = 'x'
	RADIX_Y = 'y'
	RADIX_Z = 'z'

	COMPLEMENTARY_A = 'a'
	COMPLEMENTARY_E = 'e'
	COMPLEMENTARY_I = 'i'
	COMPLEMENTARY_J = 'j'
	COMPLEMENTARY_K = 'k'
	COMPLEMENTARY_L = 'l'
	COMPLEMENTARY_N = 'n'
	COMPLEMENTARY_O = 'o'
	COMPLEMENTARY_P = 'p'
	COMPLEMENTARY_X = 'x'
	COMPLEMENTARY_Y = 'y'

	radixToCodeDict = {
		RADIX_A:'a',
		RADIX_B:'b',
		RADIX_C:'c',
		RADIX_D:'d',
		RADIX_E:'e',
		RADIX_F:'f',
		RADIX_G:'g',
		RADIX_H:'h',
		RADIX_I:'i',
		RADIX_J:'j',
		RADIX_K:'k',
		RADIX_L:'l',
		RADIX_M:'m',
		RADIX_N:'n',
		RADIX_O:'o',
		RADIX_P:'p',
		RADIX_Q:'q',
		RADIX_R:'r',
		RADIX_S:'s',
		RADIX_T:'t',
		RADIX_U:'u',
		RADIX_V:'v',
		RADIX_W:'w',
		RADIX_X:'x',
		RADIX_Y:'y',
		RADIX_Z:'z',
	}

	def __init__(self, codes, supplementCode, isDigital):
		super().__init__()

		self._codes = codes
		self._bs_spcode = supplementCode
		self._is_digital = isDigital

	@staticmethod
	def generateDefaultCodeInfo(codeList, supplementCode):
		codeInfo = BSCodeInfo(codeList, supplementCode, False)
		return codeInfo

	@property
	def code(self):
		codeList = self.getBSCodeList()
		supplementCode = self.getBSSupplement()
		
		if codeList == None or supplementCode == None:
			return None
		else:
			code = "".join(map(lambda x: BSCodeInfo.radixToCodeDict[x], codeList))
			if len(code)<3:
				if self.isDigital():
					# 根據嘸蝦米規則，如果是一到十等數目的字，則不用加補碼
					return code
				else:
					return code+supplementCode
			elif len(code)>4:
				return code[:3]+code[-1:]
			else:
				return code

	def getBSCodeList(self):
		return self._codes

	def getBSSupplement(self):
		return self._bs_spcode

	def isDigital(self):
		return self._is_digital

class BSCodeInfoEncoder(CodeInfoEncoder):
	RADIX_SEPERATOR = ','

	def generateDefaultCodeInfo(self, codeList, supplementCode):
		return BSCodeInfo.generateDefaultCodeInfo(codeList, supplementCode)

	def isAvailableOperation(self, codeInfoList):
		isAllWithCode = all(map(lambda x: x.getBSCodeList(), codeInfoList))
		return isAllWithCode


	def encodeAsLoong(self, codeInfoList):
		"""運算 "龍" """

		bslist = list(map(lambda c: c.getBSCodeList(), codeInfoList))
		bs_code_list = BSCodeInfoEncoder.computeBoshiamyCode(bslist)
		bs_spcode = codeInfoList[-1].getBSSupplement()

		codeInfo = self.generateDefaultCodeInfo(bs_code_list, bs_spcode)
		return codeInfo


	def encodeAsHan(self, codeInfoList):
		"""運算 "函" """
		firstCodeInfo = codeInfoList[0]
		secondCodeInfo = codeInfoList[1]

		newCodeInfoList = [secondCodeInfo, firstCodeInfo]
		codeInfo = self.encodeAsLoong(newCodeInfoList)
		return codeInfo


	def encodeAsZhe(self, codeInfoList):
		"""運算 "這" """
		firstCodeInfo = codeInfoList[0]
		secondCodeInfo = codeInfoList[1]

		codeInfo = self.encodeAsLoong([secondCodeInfo, firstCodeInfo])
		return codeInfo

	def encodeAsYou(self, codeInfoList):
		"""運算 "幽" """

		firstCodeInfo = codeInfoList[0]
		secondCodeInfo = codeInfoList[1]
		thirdCodeInfo = codeInfoList[2]

		newCodeInfoList = [secondCodeInfo, thirdCodeInfo, firstCodeInfo]
		codeInfo = self.encodeAsLoong(newCodeInfoList)
		return codeInfo

	@staticmethod
	def computeBoshiamyCode(bsCodeList):
		bslist = list(sum(bsCodeList, []))
		bs_code_list = (bslist[:3]+bslist[-1:]) if len(bslist)>4 else bslist
		return bs_code_list

class BSRadixParser(CodingRadixParser):
	RADIX_SEPERATOR = ','

	ATTRIB_CODE_EXPRESSION = '編碼表示式'
	ATTRIB_DIGITAL = '基本數字'
	ATTRIB_SUPPLEMENTARY_CODE = '嘸蝦米補碼'

	# 多型
	def convertRadixDescToCodeInfo(self, radixDesc):
		codeInfo = self.convertRadixDescToCodeInfoByExpression(radixDesc)
		return codeInfo

	def convertRadixDescToCodeInfoByExpression(self, radixInfo):
		elementCodeInfo = radixInfo.codeElement

		infoDict = elementCodeInfo

		strCodeList = infoDict.get(BSRadixParser.ATTRIB_CODE_EXPRESSION)
		supplementCode = infoDict.get(BSRadixParser.ATTRIB_SUPPLEMENTARY_CODE)
		isDigital = True if infoDict.get(BSRadixParser.ATTRIB_DIGITAL) != None else False

		codeList = None
		if strCodeList != None:
			codeList = strCodeList.split(BSRadixParser.RADIX_SEPERATOR)

		codeInfo = BSCodeInfo(codeList, supplementCode, isDigital)
		return codeInfo

