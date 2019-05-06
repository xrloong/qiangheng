from coding.Base import CodeInfo
from coding.Base import CodeInfoEncoder
from coding.Base import CodingRadixParser

class BSCodeInfo(CodeInfo):
	RADIX_A='a'
	RADIX_B='b'
	RADIX_C='c'
	RADIX_D='d'
	RADIX_E='e'
	RADIX_F='f'
	RADIX_G='g'
	RADIX_H='h'
	RADIX_I='i'
	RADIX_J='j'
	RADIX_K='k'
	RADIX_L='l'
	RADIX_M='m'
	RADIX_N='n'
	RADIX_O='o'
	RADIX_P='p'
	RADIX_Q='q'
	RADIX_R='r'
	RADIX_S='s'
	RADIX_T='t'
	RADIX_U='u'
	RADIX_V='v'
	RADIX_W='w'
	RADIX_X='x'
	RADIX_Y='y'
	RADIX_Z='z'

	COMPLEMENTARY_A='a'
	COMPLEMENTARY_E='e'
	COMPLEMENTARY_I='i'
	COMPLEMENTARY_J='j'
	COMPLEMENTARY_K='k'
	COMPLEMENTARY_L='l'
	COMPLEMENTARY_N='n'
	COMPLEMENTARY_O='o'
	COMPLEMENTARY_P='p'
	COMPLEMENTARY_X='x'
	COMPLEMENTARY_Y='y'

	radixToCodeDict={
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

	def __init__(self, codeList, supplementCode, isDigital):
		super().__init__()

		self._codeList=codeList
		self._bs_spcode=supplementCode
		self._is_digital=isDigital

	@staticmethod
	def generateDefaultCodeInfo(codeList, supplementCode):
		codeInfo=BSCodeInfo(codeList, supplementCode, False)
		return codeInfo

	def toCode(self):
		codeList=self.getBSCodeList()
		supplementCode=self.getBSSupplement()
		
		if codeList==None or supplementCode==None:
			return None
		else:
			code="".join(map(lambda x: BSCodeInfo.radixToCodeDict[x], codeList))
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
		return self.getMainCodeList()

	def getBSSupplement(self):
		return self._bs_spcode

	def isDigital(self):
		return self._is_digital

	def isInstallmentEncoded(self):
		return len(self._codeList)>1

	def getMainCodeList(self):
		if self._codeList != None:
			return sum(self._codeList, [])
		return None

	def getInstallmentCode(self, index):
		return self._codeList[index]

class BSCodeInfoEncoder(CodeInfoEncoder):
	INSTALLMENT_SEPERATOR='|'
	RADIX_SEPERATOR=','

	@classmethod
	def generateDefaultCodeInfo(cls, codeList, supplementCode):
		return BSCodeInfo.generateDefaultCodeInfo(codeList, supplementCode)

	@classmethod
	def isAvailableOperation(cls, codeInfoList):
		isAllWithCode=all(map(lambda x: x.getBSCodeList(), codeInfoList))
		return isAllWithCode


	@classmethod
	def encodeAsTurtle(cls, codeInfoList):
		"""運算 "龜" """
		codeInfo=cls.encodeAsLoong(codeInfoList)
		return codeInfo

	@classmethod
	def encodeAsLoong(cls, codeInfoList):
		"""運算 "龍" """

		bslist=list(map(lambda c: c.getBSCodeList(), codeInfoList))
		bs_code_list=BSCodeInfoEncoder.computeBoshiamyCode(bslist)
		bs_spcode=codeInfoList[-1].getBSSupplement()

		codeInfo=cls.generateDefaultCodeInfo([bs_code_list], bs_spcode)
		return codeInfo

	@classmethod
	def encodeAsSparrow(cls, codeInfoList):
		"""運算 "雀" """
		codeInfo=cls.encodeAsLoong(codeInfoList)
		return codeInfo

	@classmethod
	def encodeAsEqual(cls, codeInfoList):
		"""運算 "爲" """
		codeInfo=cls.encodeAsLoong(codeInfoList)
		return codeInfo


	@classmethod
	def encodeAsHan(cls, codeInfoList):
		"""運算 "函" """
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]

		newCodeInfoList=[secondCodeInfo, firstCodeInfo]
		codeInfo=cls.encodeAsLoong(newCodeInfoList)
		return codeInfo

	@classmethod
	def encodeAsTong(cls, codeInfoList):
		"""運算 "同" """
		newCodeInfoList=cls.getMergedCodeInfoListAsForGe(codeInfoList)
		codeInfo=cls.encodeAsLoong(newCodeInfoList)
		return codeInfo


	@classmethod
	def encodeAsZhe(cls, codeInfoList):
		"""運算 "這" """
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]

		codeInfo=cls.encodeAsLoong([secondCodeInfo, firstCodeInfo])
		return codeInfo

	@classmethod
	def encodeAsYou(cls, codeInfoList):
		"""運算 "幽" """

		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		newCodeInfoList=[secondCodeInfo, thirdCodeInfo, firstCodeInfo]
		codeInfo=cls.encodeAsLoong(newCodeInfoList)
		return codeInfo

	@classmethod
	def getMergedCodeInfoListAsForGe(cls, codeInfoList):
		# 贏
		if len(codeInfoList)<=1:
			print("錯誤：", file=sys.stderr)
			return codeInfoList
		else:
			firstCodeInfo=codeInfoList[0]
			if firstCodeInfo.isInstallmentEncoded():
				frontMainCode=firstCodeInfo.getInstallmentCode(0)
				rearMainCode=firstCodeInfo.getInstallmentCode(1)

				bs_spcode=firstCodeInfo.getBSSupplement()

				# 第一個的補碼不影響結果
				frontCodeInfo=cls.generateDefaultCodeInfo([frontMainCode], bs_spcode)
				rearCodeInfo=cls.generateDefaultCodeInfo([rearMainCode], bs_spcode)
				return [frontCodeInfo]+codeInfoList[1:]+[rearCodeInfo]
			else:
				return codeInfoList

	@staticmethod
	def computeBoshiamyCode(bsCodeList):
		bslist=list(sum(bsCodeList, []))
		bs_code_list=(bslist[:3]+bslist[-1:]) if len(bslist)>4 else bslist
		return bs_code_list

class BSRadixParser(CodingRadixParser):
	INSTALLMENT_SEPERATOR='|'
	RADIX_SEPERATOR=','

	ATTRIB_CODE_EXPRESSION='資訊表示式'
	ATTRIB_DIGITAL='基本數字'
	ATTRIB_SUPPLEMENTARY_CODE='嘸蝦米補碼'

	# 多型
	def convertRadixDescToCodeInfo(self, radixDesc):
		codeInfo=self.convertRadixDescToCodeInfoByExpression(radixDesc)
		return codeInfo

	def convertRadixDescToCodeInfoByExpression(self, radixInfo):
		elementCodeInfo=radixInfo.getCodeElement()

		infoDict=elementCodeInfo

		strCodeList=infoDict.get(BSRadixParser.ATTRIB_CODE_EXPRESSION)
		supplementCode=infoDict.get(BSRadixParser.ATTRIB_SUPPLEMENTARY_CODE)
		isDigital=True if infoDict.get(BSRadixParser.ATTRIB_DIGITAL) != None else False

		codeList=None
		if strCodeList!=None:
			codeList=strCodeList.split(BSRadixParser.INSTALLMENT_SEPERATOR)
			codeList=list(map(lambda x: x.split(BSRadixParser.RADIX_SEPERATOR), codeList))

		codeInfo=BSCodeInfo(codeList, supplementCode, isDigital)
		return codeInfo

