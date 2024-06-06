from element import operator as Operator

from element.enum import CodingType
from element.enum import CodeVariance

from .interface import IfCodeInfo, IfCodeInfoEncoder, IfCodingRadixParser

class CodeInfo(IfCodeInfo):
	def __init__(self):
		self.codeVariance = CodeVariance.STANDARD
		self._isSupportRadixCode = True

	@staticmethod
	def generateDefaultCodeInfo():
		codeInfo = CodeInfo()
		return codeInfo

	@property
	def code(self):
		return ""

	def setCodeInfoAttribute(self, codeVariance, isSupportRadixCode):
		self.multiplyCodeVariance(codeVariance)
		self._isSupportRadixCode = isSupportRadixCode

	def __str__(self):
		return "{{{0}}}".format(self.toCode())

	def __repr__(self):
		return str(self)

	def isSupportRadixCode(self):
		return self._isSupportRadixCode

	def getCodeVariance(self):
		return self.codeVariance

	def multiplyCodeVariance(self, codeVariance):
		self.codeVariance = self.codeVariance*codeVariance

	@property
	def variance(self):
		return self.codeVariance


class CodeInfoEncoder(IfCodeInfoEncoder):
	def generateDefaultCodeInfo(self):
		return CodeInfo.generateDefaultCodeInfo()

	def setByComps(self, operator, codeInfoList):
		codeInfo = None

		isAvailable = self.isAvailableOperation(codeInfoList)
		if isAvailable:
			if operator == Operator.OperatorTurtle:
				codeInfo = self.encodeAsTurtle(codeInfoList)
			elif operator == Operator.OperatorLoong:
				codeInfo = self.encodeAsLoong(codeInfoList)
			elif operator == Operator.OperatorSparrow:
				codeInfo = self.encodeAsSparrow(codeInfoList)
			elif operator == Operator.OperatorEqual:
				codeInfo = self.encodeAsEqual(codeInfoList)

			elif operator == Operator.OperatorSilkworm:
				codeInfo = self.encodeAsSilkworm(codeInfoList)
			elif operator == Operator.OperatorGoose:
				codeInfo = self.encodeAsGoose(codeInfoList)
			elif operator == Operator.OperatorLoop:
				codeInfo = self.encodeAsLoop(codeInfoList)

			elif operator == Operator.OperatorQi:
				codeInfo = self.encodeAsQi(codeInfoList)
			elif operator == Operator.OperatorZhe:
				codeInfo = self.encodeAsZhe(codeInfoList)
			elif operator == Operator.OperatorLiao:
				codeInfo = self.encodeAsLiao(codeInfoList)
			elif operator == Operator.OperatorZai:
				codeInfo = self.encodeAsZai(codeInfoList)
			elif operator == Operator.OperatorDou:
				codeInfo = self.encodeAsDou(codeInfoList)

			elif operator == Operator.OperatorTong:
				codeInfo = self.encodeAsTong(codeInfoList)
			elif operator == Operator.OperatorQu:
				codeInfo = self.encodeAsQu(codeInfoList)
			elif operator == Operator.OperatorHan:
				codeInfo = self.encodeAsHan(codeInfoList)
			elif operator == Operator.OperatorLeft:
				codeInfo = self.encodeAsLeft(codeInfoList)

			elif operator == Operator.OperatorMu:
				codeInfo = self.encodeAsMu(codeInfoList)
			elif operator == Operator.OperatorZuo:
				codeInfo = self.encodeAsZuo(codeInfoList)
			elif operator == Operator.OperatorYou:
				codeInfo = self.encodeAsYou(codeInfoList)
			elif operator == Operator.OperatorLiang:
				codeInfo = self.encodeAsLiang(codeInfoList)
			elif operator == Operator.OperatorJia:
				codeInfo = self.encodeAsJia(codeInfoList)

			elif operator == Operator.OperatorLuan:
				codeInfo = self.encodeAsLuan(codeInfoList)
			elif operator == Operator.OperatorBan:
				codeInfo = self.encodeAsBan(codeInfoList)
			elif operator == Operator.OperatorLin:
				codeInfo = self.encodeAsLin(codeInfoList)
			elif operator == Operator.OperatorLi:
				codeInfo = self.encodeAsLi(codeInfoList)
			elif operator == Operator.OperatorYi:
				codeInfo = self.encodeAsYi(codeInfoList)

			else:
				codeInfo = self.encodeAsInvalidate(codeInfoList)
		return codeInfo

	def isAvailableOperation(self, codeInfoList):
		return True


	def encodeAsInvalidate(self, codeInfoList):
		"""不合法的運算"""
		assert False
		return None


	def encodeAsTurtle(self, codeInfoList):
		"""運算 "龜" """
		return self.encodeAsInvalidate(codeInfoList)

	def encodeAsLoong(self, codeInfoList):
		"""運算 "龍" """
		return self.encodeAsInvalidate(codeInfoList)

	def encodeAsSparrow(self, codeInfoList):
		"""運算 "雀" """
		return self.encodeAsInvalidate(codeInfoList)

	def encodeAsEqual(self, codeInfoList):
		"""運算 "爲" """
		assert len(codeInfoList) == 1
		return self.encodeAsLoong(codeInfoList)


	def encodeAsSilkworm(self, codeInfoList):
		"""運算 "蚕" """
		codeInfo = self.encodeAsLoong(codeInfoList)
		return codeInfo

	def encodeAsGoose(self, codeInfoList):
		"""運算 "鴻" """
		codeInfo = self.encodeAsLoong(codeInfoList)
		return codeInfo

	def encodeAsLoop(self, codeInfoList):
		"""運算 "回" """
		codeInfo = self.encodeAsLoong(codeInfoList)
		return codeInfo


	def encodeAsQi(self, codeInfoList):
		"""運算 "起" """
		codeInfo = self.encodeAsLoong(codeInfoList)
		return codeInfo

	def encodeAsZhe(self, codeInfoList):
		"""運算 "這" """
		codeInfo = self.encodeAsQi(codeInfoList)
		return codeInfo

	def encodeAsLiao(self, codeInfoList):
		"""運算 "廖" """
		codeInfo = self.encodeAsLoong(codeInfoList)
		return codeInfo

	def encodeAsZai(self, codeInfoList):
		"""運算 "載" """
		codeInfo = self.encodeAsLoong(codeInfoList)
		return codeInfo

	def encodeAsDou(self, codeInfoList):
		"""運算 "斗" """
		codeInfo = self.encodeAsLoong(codeInfoList)
		return codeInfo


	def encodeAsTong(self, codeInfoList):
		"""運算 "同" """
		codeInfo = self.encodeAsLoop(codeInfoList)
		return codeInfo

	def encodeAsQu(self, codeInfoList):
		"""運算 "區" """
		codeInfo = self.encodeAsLoop(codeInfoList)
		return codeInfo

	def encodeAsHan(self, codeInfoList):
		"""運算 "函" """
		codeInfo = self.encodeAsLoop(codeInfoList)
		return codeInfo

	def encodeAsLeft(self, codeInfoList):
		"""運算 "左" """
		codeInfo = self.encodeAsLoop(codeInfoList)
		return codeInfo


	def encodeAsMu(self, codeInfoList):
		"""運算 "畞" """
		codeInfo = self.encodeAsLoong(codeInfoList)
		return codeInfo

	def convertCodeInfoListOfZuoOrder(self, codeInfoList):
		# 㘴的參數順序為：土、口、人（大部分到小部件）。
		# 但大部分的輸入法順序為：口、人、土。

		tmpCodeInfoList = codeInfoList[1:]+codeInfoList[:1]
		return tmpCodeInfoList

	def encodeAsZuo(self, codeInfoList):
		"""運算 "㘴" """
		codeInfoList = self.convertCodeInfoListOfZuoOrder(codeInfoList)
		codeInfo = self.encodeAsLoong(codeInfoList)
		return codeInfo

	def encodeAsYou(self, codeInfoList):
		"""運算 "幽" """
		codeInfo = self.encodeAsLoong(codeInfoList)
		return codeInfo

	def encodeAsLiang(self, codeInfoList):
		"""運算 "㒳" """
		codeInfo = self.encodeAsLoong(codeInfoList)
		return codeInfo

	def encodeAsJia(self, codeInfoList):
		"""運算 "夾" """
		codeInfo = self.encodeAsLoong(codeInfoList)
		return codeInfo


	def encodeAsLuan(self, codeInfoList):
		"""運算 "䜌" """
		firstCodeInfo = codeInfoList[0]
		secondCodeInfo = codeInfoList[1]
		codeInfo = self.encodeAsGoose([secondCodeInfo, firstCodeInfo, secondCodeInfo])
		return codeInfo

	def encodeAsBan(self, codeInfoList):
		"""運算 "辦" """
		firstCodeInfo = codeInfoList[0]
		secondCodeInfo = codeInfoList[1]
		codeInfo = self.encodeAsGoose([firstCodeInfo, secondCodeInfo, firstCodeInfo])
		return codeInfo


	def encodeAsLin(self, codeInfoList):
		"""運算 "粦" """
		firstCodeInfo = codeInfoList[0]
		secondCodeInfo = codeInfoList[1]
		thirdCodeInfo = codeInfoList[2]

		topCodeInfo = firstCodeInfo
		bottomCodeInfo = self.encodeAsGoose([secondCodeInfo, thirdCodeInfo])

		codeInfo = self.encodeAsSilkworm([topCodeInfo, bottomCodeInfo])
		return codeInfo

	def encodeAsLi(self, codeInfoList):
		"""運算 "瓥" """
		firstCodeInfo = codeInfoList[0]
		secondCodeInfo = codeInfoList[1]
		thirdCodeInfo = codeInfoList[2]
		fourthCodeInfo = codeInfoList[3]

		topCodeInfo = self.encodeAsGoose([firstCodeInfo, secondCodeInfo])
		bottomCodeInfo = self.encodeAsGoose([thirdCodeInfo, fourthCodeInfo])

		codeInfo = self.encodeAsSilkworm([topCodeInfo, bottomCodeInfo])
		return codeInfo

	def encodeAsYi(self, codeInfoList):
		"""運算 "燚" """
		firstCodeInfo = codeInfoList[0]

		return self.encodeAsLi([firstCodeInfo, firstCodeInfo, firstCodeInfo, firstCodeInfo, ])

class CodingRadixParser(IfCodingRadixParser):
	pass

class CodeMappingInfoInterpreter:
	def __init__(self, codingType = CodingType.Input):
		self.codingType = codingType

	def getCodingTypeName(self):
		if CodingType.Input == self.codingType:
			return "輸入法"
		else:
			return "描繪法"

	def interpretCodeMappingInfo(self, codeMappingInfo):
		return {"字符": codeMappingInfo.getName(),
			"類型": codeMappingInfo.getVariance(),
			"按鍵序列": codeMappingInfo.getCode()}

