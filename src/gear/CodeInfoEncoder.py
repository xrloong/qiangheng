from .CodeInfo import CodeInfo
from gear import Operator

class CodeInfoEncoder:
	def __init__(self):
		pass

	def generateCodeInfo(self, propDict, codeVariance):
		codeInfo=CodeInfo(propDict, codeVariance)
		return codeInfo

	def encode(self, codeInfo, operator, codeInfoList):
		for childCodeInfo in codeInfoList:
			codeVariance=childCodeInfo.getCodeVarianceType()
			codeInfo.multiplyCodeVarianceType(codeVariance)

		self.setByComps(codeInfo, operator, codeInfoList)

	def setByComps(self, codeInfo, operator, codeInfoList):
		isAvailable=self.isAvailableOperation(operator, codeInfoList)
		if isAvailable:
			if Operator.OperatorTurtle.equals(operator):
				self.encodeAsTurtle(codeInfo, operator, codeInfoList)
			elif Operator.OperatorLoong.equals(operator):
				self.encodeAsLoong(codeInfo, operator, codeInfoList)
			elif Operator.OperatorEast.equals(operator):
				self.encodeAsEast(codeInfo, operator, codeInfoList)
			elif Operator.OperatorEqual.equals(operator):
				self.encodeAsEqual(codeInfo, operator, codeInfoList)

			elif Operator.OperatorSilkworm.equals(operator):
				self.encodeAsSilkworm(codeInfo, operator, codeInfoList)
			elif Operator.OperatorGoose.equals(operator):
				self.encodeAsGoose(codeInfo, operator, codeInfoList)
			elif Operator.OperatorLoop.equals(operator):
				self.encodeAsLoop(codeInfo, operator, codeInfoList)

			elif Operator.OperatorQi.equals(operator):
				self.encodeAsQi(codeInfo, operator, codeInfoList)
			elif Operator.OperatorLiao.equals(operator):
				self.encodeAsLiao(codeInfo, operator, codeInfoList)
			elif Operator.OperatorZai.equals(operator):
				self.encodeAsZai(codeInfo, operator, codeInfoList)
			elif Operator.OperatorDou.equals(operator):
				self.encodeAsDou(codeInfo, operator, codeInfoList)

			elif Operator.OperatorTong.equals(operator):
				self.encodeAsTong(codeInfo, operator, codeInfoList)
			elif Operator.OperatorQu.equals(operator):
				self.encodeAsQu(codeInfo, operator, codeInfoList)
			elif Operator.OperatorHan.equals(operator):
				self.encodeAsHan(codeInfo, operator, codeInfoList)
			elif Operator.OperatorLeft.equals(operator):
				self.encodeAsLeft(codeInfo, operator, codeInfoList)

			elif Operator.OperatorMu.equals(operator):
				self.encodeAsMu(codeInfo, operator, codeInfoList)
			elif Operator.OperatorZuo.equals(operator):
				self.encodeAsZuo(codeInfo, operator, codeInfoList)
			elif Operator.OperatorYou.equals(operator):
				self.encodeAsYou(codeInfo, operator, codeInfoList)
			elif Operator.OperatorLiang.equals(operator):
				self.encodeAsLiang(codeInfo, operator, codeInfoList)
			elif Operator.OperatorJia.equals(operator):
				self.encodeAsJia(codeInfo, operator, codeInfoList)

			else:
				self.encodeAsInvalidate(codeInfo, operator, codeInfoList)

	def isAvailableOperation(self, operator, codeInfoList):
		return True

	def encodeAsInvalidate(self, codeInfo, operator, codeInfoList):
		"""不合法的運算"""
		pass


	def encodeAsTurtle(self, codeInfo, operator, codeInfoList):
		"""運算 "龜" """
		pass

	def encodeAsLoong(self, codeInfo, operator, codeInfoList):
		"""運算 "龍" """
		pass

	def encodeAsEast(self, codeInfo, operator, codeInfoList):
		"""運算 "東" """
		pass

	def encodeAsEqual(self, codeInfo, operator, codeInfoList):
		"""運算 "爲" """
		pass


	def encodeAsSilkworm(self, codeInfo, operator, codeInfoList):
		"""運算 "蚕" """
		self.encodeAsLoong(codeInfo, operator, codeInfoList)

	def encodeAsGoose(self, codeInfo, operator, codeInfoList):
		"""運算 "鴻" """
		self.encodeAsLoong(codeInfo, operator, codeInfoList)

	def encodeAsLoop(self, codeInfo, operator, codeInfoList):
		"""運算 "回" """
		self.encodeAsLoong(codeInfo, operator, codeInfoList)


	def encodeAsQi(self, codeInfo, operator, codeInfoList):
		"""運算 "起" """
		self.encodeAsLoong(codeInfo, operator, codeInfoList)

	def encodeAsLiao(self, codeInfo, operator, codeInfoList):
		"""運算 "廖" """
		self.encodeAsLoong(codeInfo, operator, codeInfoList)

	def encodeAsZai(self, codeInfo, operator, codeInfoList):
		"""運算 "載" """
		self.encodeAsLoong(codeInfo, operator, codeInfoList)

	def encodeAsDou(self, codeInfo, operator, codeInfoList):
		"""運算 "斗" """
		self.encodeAsLoong(codeInfo, operator, codeInfoList)


	def encodeAsTong(self, codeInfo, operator, codeInfoList):
		"""運算 "同" """
		self.encodeAsLoop(codeInfo, operator, codeInfoList)

	def encodeAsQu(self, codeInfo, operator, codeInfoList):
		"""運算 "區" """
		self.encodeAsLoop(codeInfo, operator, codeInfoList)

	def encodeAsHan(self, codeInfo, operator, codeInfoList):
		"""運算 "函" """
		self.encodeAsLoop(codeInfo, operator, codeInfoList)

	def encodeAsLeft(self, codeInfo, operator, codeInfoList):
		"""運算 "左" """
		self.encodeAsLoop(codeInfo, operator, codeInfoList)


	def encodeAsMu(self, codeInfo, operator, codeInfoList):
		"""運算 "畞" """
		self.encodeAsLoong(codeInfo, operator, codeInfoList)

	def encodeAsZuo(self, codeInfo, operator, codeInfoList):
		"""運算 "㘴" """
		self.encodeAsLoong(codeInfo, operator, codeInfoList)

	def encodeAsYou(self, codeInfo, operator, codeInfoList):
		"""運算 "幽" """
		self.encodeAsLoong(codeInfo, operator, codeInfoList)

	def encodeAsLiang(self, codeInfo, operator, codeInfoList):
		"""運算 "㒳" """
		self.encodeAsLoong(codeInfo, operator, codeInfoList)

	def encodeAsJia(self, codeInfo, operator, codeInfoList):
		"""運算 "夾" """
		self.encodeAsLoong(codeInfo, operator, codeInfoList)

