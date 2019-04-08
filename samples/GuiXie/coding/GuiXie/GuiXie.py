from coding.BaseCoding import CodingInfo
from coding.BaseCoding import CodeInfo
from coding.BaseCoding import CodeInfoEncoder
from coding.BaseCoding import CodingRadixParser

class GuiXieInfo(CodingInfo):
	"中國字庋㩪"

	IMName="庋㩪"
	def __init__(self):
		self.keyMaps=[
			['0', '0',],
			['1', '1',],
			['2', '2',],
			['3', '3',],
			['4', '4',],
			['5', '5',],
			['6', '6',],
			['7', '7',],
			['8', '8',],
			['9', '9',],
			]
		self.nameDict={
				'cn':'庋㩪',
				'tw':'庋㩪',
				'hk':'庋㩪',
				'en':'GuiXie',
				}
		self.iconfile="qhgx.svg"
		self.maxkeylength=6

class GXCodeInfo(CodeInfo):
	def __init__(self, characterCode):
		super().__init__()

	@staticmethod
	def generateDefaultCodeInfo(characterCode):
		codeInfo=GXCodeInfo(characterCode)
		return codeInfo

	def toCode(self):
		return ""

class GXCodeInfoEncoder(CodeInfoEncoder):
	@classmethod
	def generateDefaultCodeInfo(cls, characterCode):
		return GXCodeInfo.generateDefaultCodeInfo(characterCode)

	@classmethod
	def isAvailableOperation(cls, codeInfoList):
		isAllWithCode=all(map(lambda x: x.toCode(), codeInfoList))
		return isAllWithCode


	@classmethod
	def encodeAsTurtle(cls, codeInfoList):
		"""運算 "龜" """
		codeInfo=cls.encodeAsLoong(codeInfoList)
		return codeInfo

	@classmethod
	def encodeAsLoong(cls, codeInfoList):
		"""運算 "龍" """
		codeInfo=cls.generateDefaultCodeInfo('GGGG')
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

class GXRadixParser(CodingRadixParser):
	def convertRadixDescToCodeInfo(self, radixDesc):
		return GXCodeInfo()

codingMethodName = "gx"
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
CodingInfo = GuiXieInfo
CodeInfoEncoder = GXCodeInfoEncoder
CodingRadixParser = GXRadixParser

