from model.element import Operator
from model.element.CodeVarianceType import CodeVarianceTypeFactory

from model.element.enum import CodingType

from .interface import IfCodeInfo, IfCodeInfoEncoder, IfCodingRadixParser

class CodeInfo(IfCodeInfo):
	def __init__(self):
		self.codeVariance=CodeVarianceTypeFactory.generate()
		self._isSupportCharacterCode=True
		self._isSupportRadixCode=True

	@staticmethod
	def generateDefaultCodeInfo():
		codeInfo=CodeInfo()
		return codeInfo

	@property
	def code(self):
		return ""

	@staticmethod
	def computeSupportingFromProperty(propDict):
		hasCharacter=bool("字符碼" in propDict)

		[isSupportCharacterCode, isSupportRadixCode]=CodeInfo.computeSupporting(hasCharacter)
		return [isSupportCharacterCode, isSupportRadixCode]

	@staticmethod
	def computeSupporting(hasCharacter):
		isSupportCharacterCode = True
		isSupportRadixCode = not hasCharacter
		return [isSupportCharacterCode, isSupportRadixCode]

	def setCodeInfoAttribute(self, codeVariance, isSupportCharacterCode, isSupportRadixCode):
		self.multiplyCodeVarianceType(codeVariance)
		self._isSupportCharacterCode=isSupportCharacterCode
		self._isSupportRadixCode=isSupportRadixCode

	def __str__(self):
		return "{{{0}}}".format(self.toCode())

	def __repr__(self):
		return str(self)

	def isSupportCharacterCode(self):
		return self._isSupportCharacterCode

	def isSupportRadixCode(self):
		return self._isSupportRadixCode

	def getCodeVarianceType(self):
		return self.codeVariance

	def multiplyCodeVarianceType(self, codeVariance):
		self.codeVariance=self.codeVariance*codeVariance

	@property
	def variance(self):
		return self.codeVariance.getVarianceByString()


class CodeInfoEncoder(IfCodeInfoEncoder):
	def generateDefaultCodeInfo(self):
		return CodeInfo.generateDefaultCodeInfo()

	def setByComps(self, operator, codeInfoList):
		codeInfo=None

		isAvailable=self.isAvailableOperation(codeInfoList)
		if isAvailable:
			if Operator.OperatorTurtle.equals(operator):
				codeInfo=self.encodeAsTurtle(codeInfoList)
			elif Operator.OperatorLoong.equals(operator):
				codeInfo=self.encodeAsLoong(codeInfoList)
			elif Operator.OperatorSparrow.equals(operator):
				codeInfo=self.encodeAsSparrow(codeInfoList)
			elif Operator.OperatorEqual.equals(operator):
				codeInfo=self.encodeAsEqual(codeInfoList)

			elif Operator.OperatorSilkworm.equals(operator):
				codeInfo=self.encodeAsSilkworm(codeInfoList)
			elif Operator.OperatorGoose.equals(operator):
				codeInfo=self.encodeAsGoose(codeInfoList)
			elif Operator.OperatorLoop.equals(operator):
				codeInfo=self.encodeAsLoop(codeInfoList)

			elif Operator.OperatorQi.equals(operator):
				codeInfo=self.encodeAsQi(codeInfoList)
			elif Operator.OperatorZhe.equals(operator):
				codeInfo=self.encodeAsZhe(codeInfoList)
			elif Operator.OperatorLiao.equals(operator):
				codeInfo=self.encodeAsLiao(codeInfoList)
			elif Operator.OperatorZai.equals(operator):
				codeInfo=self.encodeAsZai(codeInfoList)
			elif Operator.OperatorDou.equals(operator):
				codeInfo=self.encodeAsDou(codeInfoList)

			elif Operator.OperatorTong.equals(operator):
				codeInfo=self.encodeAsTong(codeInfoList)
			elif Operator.OperatorQu.equals(operator):
				codeInfo=self.encodeAsQu(codeInfoList)
			elif Operator.OperatorHan.equals(operator):
				codeInfo=self.encodeAsHan(codeInfoList)
			elif Operator.OperatorLeft.equals(operator):
				codeInfo=self.encodeAsLeft(codeInfoList)

			elif Operator.OperatorMu.equals(operator):
				codeInfo=self.encodeAsMu(codeInfoList)
			elif Operator.OperatorZuo.equals(operator):
				codeInfo=self.encodeAsZuo(codeInfoList)
			elif Operator.OperatorYou.equals(operator):
				codeInfo=self.encodeAsYou(codeInfoList)
			elif Operator.OperatorLiang.equals(operator):
				codeInfo=self.encodeAsLiang(codeInfoList)
			elif Operator.OperatorJia.equals(operator):
				codeInfo=self.encodeAsJia(codeInfoList)

			elif Operator.OperatorLuan.equals(operator):
				codeInfo=self.encodeAsLuan(codeInfoList)
			elif Operator.OperatorBan.equals(operator):
				codeInfo=self.encodeAsBan(codeInfoList)
			elif Operator.OperatorLin.equals(operator):
				codeInfo=self.encodeAsLin(codeInfoList)
			elif Operator.OperatorLi.equals(operator):
				codeInfo=self.encodeAsLi(codeInfoList)
			elif Operator.OperatorYi.equals(operator):
				codeInfo=self.encodeAsYi(codeInfoList)

			else:
				codeInfo=self.encodeAsInvalidate(codeInfoList)
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
		codeInfo=self.encodeAsLoong(codeInfoList)
		return codeInfo

	def encodeAsGoose(self, codeInfoList):
		"""運算 "鴻" """
		codeInfo=self.encodeAsLoong(codeInfoList)
		return codeInfo

	def encodeAsLoop(self, codeInfoList):
		"""運算 "回" """
		codeInfo=self.encodeAsLoong(codeInfoList)
		return codeInfo


	def encodeAsQi(self, codeInfoList):
		"""運算 "起" """
		codeInfo=self.encodeAsLoong(codeInfoList)
		return codeInfo

	def encodeAsZhe(self, codeInfoList):
		"""運算 "這" """
		codeInfo=self.encodeAsQi(codeInfoList)
		return codeInfo

	def encodeAsLiao(self, codeInfoList):
		"""運算 "廖" """
		codeInfo=self.encodeAsLoong(codeInfoList)
		return codeInfo

	def encodeAsZai(self, codeInfoList):
		"""運算 "載" """
		codeInfo=self.encodeAsLoong(codeInfoList)
		return codeInfo

	def encodeAsDou(self, codeInfoList):
		"""運算 "斗" """
		codeInfo=self.encodeAsLoong(codeInfoList)
		return codeInfo


	def encodeAsTong(self, codeInfoList):
		"""運算 "同" """
		codeInfo=self.encodeAsLoop(codeInfoList)
		return codeInfo

	def encodeAsQu(self, codeInfoList):
		"""運算 "區" """
		codeInfo=self.encodeAsLoop(codeInfoList)
		return codeInfo

	def encodeAsHan(self, codeInfoList):
		"""運算 "函" """
		codeInfo=self.encodeAsLoop(codeInfoList)
		return codeInfo

	def encodeAsLeft(self, codeInfoList):
		"""運算 "左" """
		codeInfo=self.encodeAsLoop(codeInfoList)
		return codeInfo


	def encodeAsMu(self, codeInfoList):
		"""運算 "畞" """
		codeInfo=self.encodeAsLoong(codeInfoList)
		return codeInfo

	def convertCodeInfoListOfZuoOrder(self, codeInfoList):
		# 㘴的參數順序為：土、口、人（大部分到小部件）。
		# 但大部分的輸入法順序為：口、人、土。

		tmpCodeInfoList=codeInfoList[1:]+codeInfoList[:1]
		return tmpCodeInfoList

	def encodeAsZuo(self, codeInfoList):
		"""運算 "㘴" """
		codeInfoList=self.convertCodeInfoListOfZuoOrder(codeInfoList)
		codeInfo=self.encodeAsLoong(codeInfoList)
		return codeInfo

	def encodeAsYou(self, codeInfoList):
		"""運算 "幽" """
		codeInfo=self.encodeAsLoong(codeInfoList)
		return codeInfo

	def encodeAsLiang(self, codeInfoList):
		"""運算 "㒳" """
		codeInfo=self.encodeAsLoong(codeInfoList)
		return codeInfo

	def encodeAsJia(self, codeInfoList):
		"""運算 "夾" """
		codeInfo=self.encodeAsLoong(codeInfoList)
		return codeInfo


	def encodeAsLuan(self, codeInfoList):
		"""運算 "䜌" """
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		codeInfo=self.encodeAsGoose([secondCodeInfo, firstCodeInfo, secondCodeInfo])
		return codeInfo

	def encodeAsBan(self, codeInfoList):
		"""運算 "辦" """
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		codeInfo=self.encodeAsGoose([firstCodeInfo, secondCodeInfo, firstCodeInfo])
		return codeInfo


	def encodeAsLin(self, codeInfoList):
		"""運算 "粦" """
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		topCodeInfo=firstCodeInfo
		bottomCodeInfo=self.encodeAsGoose([secondCodeInfo, thirdCodeInfo])

		codeInfo=self.encodeAsSilkworm([topCodeInfo, bottomCodeInfo])
		return codeInfo

	def encodeAsLi(self, codeInfoList):
		"""運算 "瓥" """
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]
		fourthCodeInfo=codeInfoList[3]

		topCodeInfo=self.encodeAsGoose([firstCodeInfo, secondCodeInfo])
		bottomCodeInfo=self.encodeAsGoose([thirdCodeInfo, fourthCodeInfo])

		codeInfo=self.encodeAsSilkworm([topCodeInfo, bottomCodeInfo])
		return codeInfo

	def encodeAsYi(self, codeInfoList):
		"""運算 "燚" """
		firstCodeInfo=codeInfoList[0]

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

