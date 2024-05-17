from coding.Base import CodeInfo
from coding.Base import CodeInfoEncoder
from coding.Base import CodingRadixParser

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

	def __init__(self, codes = ()):
		super().__init__()

		self.codes = codes

	@staticmethod
	def generateDefaultCodeInfo(codeList):
		codeInfo=DYCodeInfo(codeList)
		return codeInfo

	def toCode(self):
		mainRadixList = self.getMainCodeList()
		mainCodeList = tuple(map(lambda x: DYCodeInfo.radixToCodeDict[x], mainRadixList))
		code="".join(mainCodeList)
		return (code[:3]+code[-1:] if len(code)>4 else code)


	def getMainCodeList(self):
		return self.codes

class DYCodeInfoEncoder(CodeInfoEncoder):
	def generateDefaultCodeInfo(self, codeList):
		return DYCodeInfo.generateDefaultCodeInfo(codeList)

	def isAvailableOperation(self, codeInfoList):
		isAllWithCode=all(map(lambda x: x.getMainCodeList(), codeInfoList))
		return isAllWithCode


	def encodeAsLoong(self, codeInfoList):
		"""運算 "龍" """

		dyCodeList=list(map(lambda c: c.getMainCodeList(), codeInfoList))
		dyCode=DYCodeInfoEncoder.computeDaYiCodeByCodeList(dyCodeList)
		codeInfo=self.generateDefaultCodeInfo(dyCode)
		return codeInfo


	def encodeAsHan(self, codeInfoList):
		"""運算 "函" """
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]

		newCodeInfoList=[secondCodeInfo, firstCodeInfo]
		codeInfo=self.encodeAsLoong(newCodeInfoList)
		return codeInfo


	def encodeAsZhe(self, codeInfoList):
		"""運算 "這" """
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]

		codeInfo=self.encodeAsLoong([secondCodeInfo, firstCodeInfo])
		return codeInfo


	def encodeAsLuan(self, codeInfoList):
		"""運算 "䜌" """
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		codeInfo=self.encodeAsLoong([firstCodeInfo, secondCodeInfo, secondCodeInfo])
		return codeInfo


	def getCodeInfoExceptLast(self, codeInfo):
		mainCodeList=codeInfo.getMainCodeList()

		if len(mainCodeList)>1:
			tmpCodeInfo=self.generateDefaultCodeInfo([mainCodeList[:-1]])
		else:
			tmpCodeInfo=None

		return tmpCodeInfo

	def getCodeInfoExceptFirst(self, codeInfo):
		mainCodeList=codeInfo.getMainCodeList()

		if len(mainCodeList)>1:
			tmpCodeInfo=self.generateDefaultCodeInfo([mainCodeList[1:]])
		else:
			tmpCodeInfo=None

		return tmpCodeInfo

	def convertMergedCode(self, firstCodeInfo, secondCodeInfo, firstRadix, secondRadix, targetRadix):
		firstMainCodeList=firstCodeInfo.getMainCodeList()
		secondMainCodeList=secondCodeInfo.getMainCodeList()

		if firstMainCodeList[-1]==firstRadix and secondMainCodeList[0]==secondRadix:
			newFirstCodeInfo=self.getCodeInfoExceptLast(firstCodeInfo)
			targetCodeInfo=self.generateDefaultCodeInfo([[targetRadix]])
			newSecondCodeInfo=self.getCodeInfoExceptFirst(secondCodeInfo)
		else:
			newFirstCodeInfo=firstCodeInfo
			targetCodeInfo=None
			newSecondCodeInfo=secondCodeInfo
		return [newFirstCodeInfo, targetCodeInfo, newSecondCodeInfo]

	@staticmethod
	def computeDaYiCodeByCodeList(dyCodeList):
		cat=sum(dyCodeList, [])
		dyCode=cat[:3]+cat[-1:] if len(cat)>4 else cat
		return dyCode

class DYRadixParser(CodingRadixParser):
	RADIX_SEPERATOR=','

	ATTRIB_CODE_EXPRESSION='編碼表示式'

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
			codeList = strCodeList.split(DYRadixParser.RADIX_SEPERATOR)

		codeInfo=DYCodeInfo(codeList)
		return codeInfo

