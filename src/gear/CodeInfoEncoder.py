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
		isAvailable=self.isAvailableOperation(codeInfoList)
		if isAvailable:
			if Operator.OperatorTurtle.equals(operator):
				self.encodeAsTurtle(codeInfo, codeInfoList)
			elif Operator.OperatorLoong.equals(operator):
				self.encodeAsLoong(codeInfo, codeInfoList)
			elif Operator.OperatorEast.equals(operator):
				self.encodeAsEast(codeInfo, codeInfoList)
			elif Operator.OperatorEqual.equals(operator):
				self.encodeAsEqual(codeInfo, codeInfoList)

			elif Operator.OperatorSilkworm.equals(operator):
				self.encodeAsSilkworm(codeInfo, codeInfoList)
			elif Operator.OperatorGoose.equals(operator):
				self.encodeAsGoose(codeInfo, codeInfoList)
			elif Operator.OperatorLoop.equals(operator):
				self.encodeAsLoop(codeInfo, codeInfoList)

			elif Operator.OperatorQi.equals(operator):
				self.encodeAsQi(codeInfo, codeInfoList)
			elif Operator.OperatorLiao.equals(operator):
				self.encodeAsLiao(codeInfo, codeInfoList)
			elif Operator.OperatorZai.equals(operator):
				self.encodeAsZai(codeInfo, codeInfoList)
			elif Operator.OperatorDou.equals(operator):
				self.encodeAsDou(codeInfo, codeInfoList)

			elif Operator.OperatorTong.equals(operator):
				self.encodeAsTong(codeInfo, codeInfoList)
			elif Operator.OperatorQu.equals(operator):
				self.encodeAsQu(codeInfo, codeInfoList)
			elif Operator.OperatorHan.equals(operator):
				self.encodeAsHan(codeInfo, codeInfoList)
			elif Operator.OperatorLeft.equals(operator):
				self.encodeAsLeft(codeInfo, codeInfoList)

			elif Operator.OperatorMu.equals(operator):
				self.encodeAsMu(codeInfo, codeInfoList)
			elif Operator.OperatorZuo.equals(operator):
				self.encodeAsZuo(codeInfo, codeInfoList)
			elif Operator.OperatorYou.equals(operator):
				self.encodeAsYou(codeInfo, codeInfoList)
			elif Operator.OperatorLiang.equals(operator):
				self.encodeAsLiang(codeInfo, codeInfoList)
			elif Operator.OperatorJia.equals(operator):
				self.encodeAsJia(codeInfo, codeInfoList)

			else:
				self.encodeAsInvalidate(codeInfo, codeInfoList)

	def isAvailableOperation(self, codeInfoList):
		return True

	def encodeAsInvalidate(self, codeInfo, codeInfoList):
		"""不合法的運算"""
		pass


	def encodeAsTurtle(self, codeInfo, codeInfoList):
		"""運算 "龜" """
		pass

	def encodeAsLoong(self, codeInfo, codeInfoList):
		"""運算 "龍" """
		pass

	def encodeAsEast(self, codeInfo, codeInfoList):
		"""運算 "東" """
		pass

	def encodeAsEqual(self, codeInfo, codeInfoList):
		"""運算 "爲" """
		pass


	def encodeAsSilkworm(self, codeInfo, codeInfoList):
		"""運算 "蚕" """
		self.encodeAsLoong(codeInfo, codeInfoList)

	def encodeAsGoose(self, codeInfo, codeInfoList):
		"""運算 "鴻" """
		self.encodeAsLoong(codeInfo, codeInfoList)

	def encodeAsLoop(self, codeInfo, codeInfoList):
		"""運算 "回" """
		self.encodeAsLoong(codeInfo, codeInfoList)


	def encodeAsQi(self, codeInfo, codeInfoList):
		"""運算 "起" """
		self.encodeAsLoong(codeInfo, codeInfoList)

	def encodeAsLiao(self, codeInfo, codeInfoList):
		"""運算 "廖" """
		self.encodeAsLoong(codeInfo, codeInfoList)

	def encodeAsZai(self, codeInfo, codeInfoList):
		"""運算 "載" """
		self.encodeAsLoong(codeInfo, codeInfoList)

	def encodeAsDou(self, codeInfo, codeInfoList):
		"""運算 "斗" """
		self.encodeAsLoong(codeInfo, codeInfoList)


	def encodeAsTong(self, codeInfo, codeInfoList):
		"""運算 "同" """
		self.encodeAsLoop(codeInfo, codeInfoList)

	def encodeAsQu(self, codeInfo, codeInfoList):
		"""運算 "區" """
		self.encodeAsLoop(codeInfo, codeInfoList)

	def encodeAsHan(self, codeInfo, codeInfoList):
		"""運算 "函" """
		self.encodeAsLoop(codeInfo, codeInfoList)

	def encodeAsLeft(self, codeInfo, codeInfoList):
		"""運算 "左" """
		self.encodeAsLoop(codeInfo, codeInfoList)


	def encodeAsMu(self, codeInfo, codeInfoList):
		"""運算 "畞" """
		self.encodeAsLoong(codeInfo, codeInfoList)

	def encodeAsZuo(self, codeInfo, codeInfoList):
		"""運算 "㘴" """
		self.encodeAsLoong(codeInfo, codeInfoList)

	def encodeAsYou(self, codeInfo, codeInfoList):
		"""運算 "幽" """
		self.encodeAsLoong(codeInfo, codeInfoList)

	def encodeAsLiang(self, codeInfo, codeInfoList):
		"""運算 "㒳" """
		self.encodeAsLoong(codeInfo, codeInfoList)

	def encodeAsJia(self, codeInfo, codeInfoList):
		"""運算 "夾" """
		self.encodeAsLoong(codeInfo, codeInfoList)

