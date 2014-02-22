from .CodeInfo import CodeInfo
from ..gear import Operator

class CodeInfoEncoder:
	@staticmethod
	def computeSupportingFromProperty(propDict):
		return CodeInfo.computeSupportingFromProperty(propDict)

	@staticmethod
	def computeSupporting(hasCharacter, hasRadix):
		return CodeInfo.computeSupporting(hasCharacter, hasRadix)

	@classmethod
	def generateDefaultCodeInfo(cls):
		return CodeInfo.generateDefaultCodeInfo()

	def encode(self, operator, codeInfoList):
		codeInfo=self.setByComps(operator, codeInfoList)
		return codeInfo

	def setByComps(self, operator, codeInfoList):
		codeInfo=None

		isAvailable=self.isAvailableOperation(codeInfoList)
		if isAvailable:
			if Operator.OperatorTurtle.equals(operator):
				codeInfo=self.encodeAsTurtle(codeInfoList)
			elif Operator.OperatorLoong.equals(operator):
				codeInfo=self.encodeAsLoong(codeInfoList)
			elif Operator.OperatorEast.equals(operator):
				codeInfo=self.encodeAsEast(codeInfoList)
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

			else:
				codeInfo=self.encodeAsInvalidate(codeInfoList)
		return codeInfo

	@classmethod
	def isAvailableOperation(cls, codeInfoList):
		return True


	@classmethod
	def encodeAsInvalidate(cls, codeInfoList):
		"""不合法的運算"""
		return None


	@classmethod
	def encodeAsTurtle(cls, codeInfoList):
		"""運算 "龜" """
		codeInfo=cls.generateDefaultCodeInfo()
		return codeInfo

	@classmethod
	def encodeAsLoong(cls, codeInfoList):
		"""運算 "龍" """
		codeInfo=cls.generateDefaultCodeInfo()
		return codeInfo

	@classmethod
	def encodeAsEast(cls, codeInfoList):
		"""運算 "東" """
		codeInfo=cls.generateDefaultCodeInfo()
		return codeInfo

	@classmethod
	def encodeAsEqual(cls, codeInfoList):
		"""運算 "爲" """
		codeInfo=cls.generateDefaultCodeInfo()
		return codeInfo


	@classmethod
	def encodeAsSilkworm(cls, codeInfoList):
		"""運算 "蚕" """
		codeInfo=cls.encodeAsLoong(codeInfoList)
		return codeInfo

	@classmethod
	def encodeAsGoose(cls, codeInfoList):
		"""運算 "鴻" """
		codeInfo=cls.encodeAsLoong(codeInfoList)
		return codeInfo

	@classmethod
	def encodeAsLoop(cls, codeInfoList):
		"""運算 "回" """
		codeInfo=cls.encodeAsLoong(codeInfoList)
		return codeInfo


	@classmethod
	def encodeAsQi(cls, codeInfoList):
		"""運算 "起" """
		codeInfo=cls.encodeAsLoong(codeInfoList)
		return codeInfo

	@classmethod
	def encodeAsZhe(cls, codeInfoList):
		"""運算 "這" """
		codeInfo=cls.encodeAsQi(codeInfoList)
		return codeInfo

	@classmethod
	def encodeAsLiao(cls, codeInfoList):
		"""運算 "廖" """
		codeInfo=cls.encodeAsLoong(codeInfoList)
		return codeInfo

	@classmethod
	def encodeAsZai(cls, codeInfoList):
		"""運算 "載" """
		codeInfo=cls.encodeAsLoong(codeInfoList)
		return codeInfo

	@classmethod
	def encodeAsDou(cls, codeInfoList):
		"""運算 "斗" """
		codeInfo=cls.encodeAsLoong(codeInfoList)
		return codeInfo


	@classmethod
	def encodeAsTong(cls, codeInfoList):
		"""運算 "同" """
		codeInfo=cls.encodeAsLoop(codeInfoList)
		return codeInfo

	@classmethod
	def encodeAsQu(cls, codeInfoList):
		"""運算 "區" """
		codeInfo=cls.encodeAsLoop(codeInfoList)
		return codeInfo

	@classmethod
	def encodeAsHan(cls, codeInfoList):
		"""運算 "函" """
		codeInfo=cls.encodeAsLoop(codeInfoList)
		return codeInfo

	@classmethod
	def encodeAsLeft(cls, codeInfoList):
		"""運算 "左" """
		codeInfo=cls.encodeAsLoop(codeInfoList)
		return codeInfo


	@classmethod
	def encodeAsMu(cls, codeInfoList):
		"""運算 "畞" """
		codeInfo=cls.encodeAsLoong(codeInfoList)
		return codeInfo

	@classmethod
	def convertCodeInfoListOfZuoOrder(cls, codeInfoList):
		# 㘴的參數順序為：土、口、人（大部分到小部件）。
		# 但大部分的輸入法順序為：口、人、土。

		tmpCodeInfoList=codeInfoList[1:]+codeInfoList[:1]
		return tmpCodeInfoList

	@classmethod
	def encodeAsZuo(cls, codeInfoList):
		"""運算 "㘴" """
		codeInfoList=cls.convertCodeInfoListOfZuoOrder(codeInfoList)
		codeInfo=cls.encodeAsLoong(codeInfoList)
		return codeInfo

	@classmethod
	def encodeAsYou(cls, codeInfoList):
		"""運算 "幽" """
		codeInfo=cls.encodeAsLoong(codeInfoList)
		return codeInfo

	@classmethod
	def encodeAsLiang(cls, codeInfoList):
		"""運算 "㒳" """
		codeInfo=cls.encodeAsLoong(codeInfoList)
		return codeInfo

	@classmethod
	def encodeAsJia(cls, codeInfoList):
		"""運算 "夾" """
		codeInfo=cls.encodeAsLoong(codeInfoList)
		return codeInfo


	@classmethod
	def encodeAsLuan(cls, codeInfoList):
		"""運算 "䜌" """
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		codeInfo=cls.encodeAsGoose([secondCodeInfo, firstCodeInfo, secondCodeInfo])
		return codeInfo

	@classmethod
	def encodeAsBan(cls, codeInfoList):
		"""運算 "辦" """
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		codeInfo=cls.encodeAsGoose([firstCodeInfo, secondCodeInfo, firstCodeInfo])
		return codeInfo


	@classmethod
	def encodeAsLin(cls, codeInfoList):
		"""運算 "粦" """
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		topCodeInfo=firstCodeInfo
		bottomCodeInfo=cls.encodeAsGoose([secondCodeInfo, thirdCodeInfo])

		codeInfo=cls.encodeAsSilkworm([topCodeInfo, bottomCodeInfo])
		return codeInfo

	@classmethod
	def encodeAsLi(cls, codeInfoList):
		"""運算 "瓥" """
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]
		fourthCodeInfo=codeInfoList[3]

		topCodeInfo=cls.encodeAsGoose([firstCodeInfo, secondCodeInfo])
		bottomCodeInfo=cls.encodeAsGoose([thirdCodeInfo, fourthCodeInfo])

		codeInfo=cls.encodeAsSilkworm([topCodeInfo, bottomCodeInfo])
		return codeInfo

