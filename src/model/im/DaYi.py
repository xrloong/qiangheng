from model.BaseCoding import CodingInfo
from model.BaseCoding import CodeInfo
from model.BaseCoding import CodeInfoEncoder
from model.BaseCoding import CodingRadixParser

class DaYiInfo(CodingInfo):
	"大易輸入法"

	IMName="大易"
	def __init__(self):
		self.keyMaps=[
			[',', '力',],
			['.', '點',],
			['/', '竹',],
			['0', '金',],
			['1', '言',],
			['2', '牛',],
			['3', '目',],
			['4', '四',],
			['5', '王',],
			['6', '門',],
			['7', '田',],
			['8', '米',],
			['9', '足',],
			[';', '虫',],
			['a', '人',],
			['b', '馬',],
			['c', '七',],
			['d', '日',],
			['e', '一',],
			['f', '土',],
			['g', '手',],
			['h', '鳥',],
			['i', '木',],
			['j', '月',],
			['k', '立',],
			['l', '女',],
			['m', '雨',],
			['n', '魚',],
			['o', '口',],
			['p', '耳',],
			['q', '石',],
			['r', '工',],
			['s', '革',],
			['t', '糸',],
			['u', '艸',],
			['v', '禾',],
			['w', '山',],
			['x', '水',],
			['y', '火',],
			['z', '心',],
			]
		self.nameDict={
				'cn':'大易',
				'tw':'大易',
				'hk':'大易',
				'en':'DaYi',
				}
		self.iconfile="qhdy.svg"
		self.maxkeylength=4

class DYCodeInfo(CodeInfo):
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
	RADIX_0='0'
	RADIX_1='1'
	RADIX_2='2'
	RADIX_3='3'
	RADIX_4='4'
	RADIX_5='5'
	RADIX_6='6'
	RADIX_7='7'
	RADIX_8='8'
	RADIX_9='9'
	RADIX_DOT='.'
	RADIX_COMMA=':'
	RADIX_SEMICOLON=';'
	RADIX_SLASH='/'

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
		RADIX_0:'0',
		RADIX_1:'1',
		RADIX_2:'2',
		RADIX_3:'3',
		RADIX_4:'4',
		RADIX_5:'5',
		RADIX_6:'6',
		RADIX_7:'7',
		RADIX_8:'8',
		RADIX_9:'9',
		RADIX_DOT:'.',
		RADIX_COMMA:',',
		RADIX_SEMICOLON:';',
		RADIX_SLASH:'/',
	}

	def __init__(self, codeList):
		super().__init__()

		self._codeList=codeList

	@staticmethod
	def generateDefaultCodeInfo(codeList):
		codeInfo=DYCodeInfo(codeList)
		return codeInfo

	def toCode(self):
		mainRadixList=self.getMainCodeList()
		mainCodeList=list(map(lambda x: DYCodeInfo.radixToCodeDict[x], mainRadixList))
		code="".join(mainCodeList)
		return (code[:3]+code[-1:] if len(code)>4 else code)

	def isInstallmentEncoded(self):
		return len(self._codeList)>1

	def getMainCodeList(self):
		if self._codeList != None:
			return sum(self._codeList, [])
		return None

	def getInstallmentCode(self, index):
		return self._codeList[index]

class DYCodeInfoEncoder(CodeInfoEncoder):
	@classmethod
	def generateDefaultCodeInfo(cls, codeList):
		return DYCodeInfo.generateDefaultCodeInfo(codeList)

	@classmethod
	def isAvailableOperation(cls, codeInfoList):
		isAllWithCode=all(map(lambda x: x.getMainCodeList(), codeInfoList))
		return isAllWithCode


	@classmethod
	def encodeAsTurtle(cls, codeInfoList):
		"""運算 "龜" """
		codeInfo=cls.encodeAsLoong(codeInfoList)
		return codeInfo

	@classmethod
	def encodeAsLoong(cls, codeInfoList):
		"""運算 "龍" """

		dyCodeList=list(map(lambda c: c.getMainCodeList(), codeInfoList))
		dyCode=DYCodeInfoEncoder.computeDaYiCodeByCodeList(dyCodeList)
		codeInfo=cls.generateDefaultCodeInfo([dyCode])
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
	def encodeAsLoop(cls, codeInfoList):
		"""運算 "回" """
		newCodeInfoList=cls.getMergedCodeInfoListAsForGe(codeInfoList)
		codeInfo=cls.encodeAsLoong(newCodeInfoList)
		return codeInfo

	@classmethod
	def encodeAsTong(cls, codeInfoList):
		"""運算 "同" """
		newCodeInfoList=cls.getMergedCodeInfoListAsForGe(codeInfoList)
		codeInfo=cls.encodeAsLoong(newCodeInfoList)
		return codeInfo

	@classmethod
	def encodeAsHan(cls, codeInfoList):
		"""運算 "函" """
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]

		newCodeInfoList=[secondCodeInfo, firstCodeInfo]
		newCodeInfoList=cls.getMergedCodeInfoListAsForGe(newCodeInfoList)
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
	def encodeAsZai(cls, codeInfoList):
		"""運算 "載" """
		newCodeInfoList=cls.getMergedCodeInfoListAsForGe(codeInfoList)
		codeInfo=cls.encodeAsLoong(newCodeInfoList)
		return codeInfo


	@classmethod
	def encodeAsLuan(cls, codeInfoList):
		"""運算 "䜌" """
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		codeInfo=cls.encodeAsLoong([firstCodeInfo, secondCodeInfo, secondCodeInfo])
		return codeInfo

	@classmethod
	def getCodeInfoExceptLast(cls, codeInfo):
		mainCodeList=codeInfo.getMainCodeList()

		if len(mainCodeList)>1:
			tmpCodeInfo=cls.generateDefaultCodeInfo([mainCodeList[:-1]])
		else:
			tmpCodeInfo=None

		return tmpCodeInfo

	@classmethod
	def getCodeInfoExceptFirst(cls, codeInfo):
		mainCodeList=codeInfo.getMainCodeList()

		if len(mainCodeList)>1:
			tmpCodeInfo=cls.generateDefaultCodeInfo([mainCodeList[1:]])
		else:
			tmpCodeInfo=None

		return tmpCodeInfo

	@classmethod
	def convertMergedCode(cls, firstCodeInfo, secondCodeInfo, firstRadix, secondRadix, targetRadix):
		firstMainCodeList=firstCodeInfo.getMainCodeList()
		secondMainCodeList=secondCodeInfo.getMainCodeList()

		if firstMainCodeList[-1]==firstRadix and secondMainCodeList[0]==secondRadix:
			newFirstCodeInfo=cls.getCodeInfoExceptLast(firstCodeInfo)
			targetCodeInfo=cls.generateDefaultCodeInfo([[targetRadix]])
			newSecondCodeInfo=cls.getCodeInfoExceptFirst(secondCodeInfo)
		else:
			newFirstCodeInfo=firstCodeInfo
			targetCodeInfo=None
			newSecondCodeInfo=secondCodeInfo
		return [newFirstCodeInfo, targetCodeInfo, newSecondCodeInfo]

	@classmethod
	def getMergedCodeInfoListAsForGe(cls, codeInfoList):
		# 如 咸、戎
		if len(codeInfoList)<=1:
			print("錯誤：", file=sys.stderr)
			return codeInfoList
		else:
			firstCodeInfo=codeInfoList[0]
			if firstCodeInfo.isInstallmentEncoded():
				frontMainCode=firstCodeInfo.getInstallmentCode(0)
				rearMainCode=firstCodeInfo.getInstallmentCode(1)

				frontCodeInfo=cls.generateDefaultCodeInfo([frontMainCode])
				rearCodeInfo=cls.generateDefaultCodeInfo([rearMainCode])
				return [frontCodeInfo]+codeInfoList[1:]+[rearCodeInfo]
			else:
				return codeInfoList

	@staticmethod
	def computeDaYiCodeByCodeList(dyCodeList):
		cat=sum(dyCodeList, [])
		dyCode=cat[:3]+cat[-1:] if len(cat)>4 else cat
		return dyCode

class DYRadixParser(CodingRadixParser):
	INSTALLMENT_SEPERATOR='|'
	RADIX_SEPERATOR=','

	ATTRIB_CODE_EXPRESSION='資訊表示式'

	# 多型
	def convertRadixDescToCodeInfo(self, radixDesc):
		codeInfo=self.convertRadixDescToCodeInfoByExpression(radixDesc)
		return codeInfo

	def convertRadixDescToCodeInfoByExpression(self, radixInfo):
		elementCodeInfo=radixInfo.getCodeElement()

		infoDict=elementCodeInfo

		strCodeList=infoDict.get(DYRadixParser.ATTRIB_CODE_EXPRESSION)

		codeList=None
		if strCodeList!=None:
			codeList=strCodeList.split(DYRadixParser.INSTALLMENT_SEPERATOR)
			codeList=list(map(lambda x: x.split(DYRadixParser.RADIX_SEPERATOR), codeList))

		codeInfo=DYCodeInfo(codeList)
		return codeInfo

codingMethodName = "dy"
codingMethodDir = "gen/qhdata/{method}/".format(method=codingMethodName)
CodingComponentFileList = [
	codingMethodDir + 'style.yaml',
]
CodingSubstituteFileList = [
	codingMethodDir + 'substitute.yaml',
]
CodingRadixFileList = [
	codingMethodDir + 'radix/CJK.yaml',
	codingMethodDir + 'radix/CJK-A.yaml',
	codingMethodDir + 'radix/adjust.yaml'
]
CodingInfo = DaYiInfo
CodeInfoEncoder = DYCodeInfoEncoder
CodingRadixParser = DYRadixParser

