from .CodeInfo import CodeInfo
from gear import Operator

class CodeInfoEncoder:
	def __init__(self):
		pass

	@staticmethod
	def computeSupportingFromProperty(propDict):
		hasCharacter=bool("字符碼" in propDict)
		hasRadix=bool("字根碼" in propDict)

		[isSupportCharacterCode, isSupportRadixCode]=CodeInfo.computeSupporting(hasCharacter, hasRadix)
		return [isSupportCharacterCode, isSupportRadixCode]

	@staticmethod
	def computeSupporting(hasCharacter, hasRadix):
		if hasCharacter or hasRadix:
			isSupportCharacterCode=False
			isSupportRadixCode=False
			if hasCharacter:
				isSupportCharacterCode=True
			if hasRadix:
				isSupportRadixCode=True
		else:
			isSupportCharacterCode=True
			isSupportRadixCode=True
		return [isSupportCharacterCode, isSupportRadixCode]

	def generateCodeInfo(self, propDict):
		[isSupportCharacterCode, isSupportRadixCode]=CodeInfoEncoder.computeSupportingFromProperty(propDict)
		codeInfo=CodeInfo(isSupportCharacterCode, isSupportRadixCode)
		return codeInfo

	def generateDefaultCodeInfo(self):
		return self.generateCodeInfo({})

	def interprettCharacterCode(self, codeInfo):
		return codeInfo.characterCode

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

	def isAvailableOperation(self, codeInfoList):
		return True


	def encodeAsInvalidate(self, codeInfoList):
		"""不合法的運算"""
		return None


	def encodeAsTurtle(self, codeInfoList):
		"""運算 "龜" """
		codeInfo=self.generateDefaultCodeInfo()
		return codeInfo

	def encodeAsLoong(self, codeInfoList):
		"""運算 "龍" """
		codeInfo=self.generateDefaultCodeInfo()
		return codeInfo

	def encodeAsEast(self, codeInfoList):
		"""運算 "東" """
		codeInfo=self.generateDefaultCodeInfo()
		return codeInfo

	def encodeAsEqual(self, codeInfoList):
		"""運算 "爲" """
		codeInfo=self.generateDefaultCodeInfo()
		return codeInfo


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

	def encodeAsZuo(self, codeInfoList):
		"""運算 "㘴" """
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

