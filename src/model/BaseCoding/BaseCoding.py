from injector import inject

from model.element import Operator
from model.element.CodeVarianceType import CodeVarianceTypeFactory

class CodingInfo:
	"編碼方式"

	IMName="空"
	def __init__(self):
		self.keyMaps=[]
		self.nameDict={
				'cn':'空',
				'tw':'空',
				'hk':'空',
				'en':'None',
				}
		self.iconfile="empty.png"
		self.maxkeylength=0

	def getName(self, localization):
		return self.nameDict.get(localization, "")

	def getIconFileName(self):
		return self.iconfile

	def getMaxKeyLength(self):
		return self.maxkeylength

	def getKeyMaps(self):
		return self.keyMaps

	def getKeyList(self):
		return "".join(list(zip(*self.keyMaps))[0])


class CodeInfo:
	def __init__(self):
		self.codeVariance=CodeVarianceTypeFactory.generate()
		self._isSupportCharacterCode=True
		self._isSupportRadixCode=True

	@staticmethod
	def generateDefaultCodeInfo():
		codeInfo=CodeInfo()
		return codeInfo

	def toCode(self):
		return ""

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
#		self.codeVariance.multi(codeVariance)

	@property
	def variance(self):
		return self.codeVariance.getVarianceByString()


class CodeInfoEncoder:
	@classmethod
	def generateDefaultCodeInfo(cls):
		return CodeInfo.generateDefaultCodeInfo()

	@classmethod
	def setByComps(cls, operator, codeInfoList):
		codeInfo=None

		isAvailable=cls.isAvailableOperation(codeInfoList)
		if isAvailable:
			if Operator.OperatorTurtle.equals(operator):
				codeInfo=cls.encodeAsTurtle(codeInfoList)
			elif Operator.OperatorLoong.equals(operator):
				codeInfo=cls.encodeAsLoong(codeInfoList)
			elif Operator.OperatorSparrow.equals(operator):
				codeInfo=cls.encodeAsSparrow(codeInfoList)
			elif Operator.OperatorEqual.equals(operator):
				codeInfo=cls.encodeAsEqual(codeInfoList)

			elif Operator.OperatorSilkworm.equals(operator):
				codeInfo=cls.encodeAsSilkworm(codeInfoList)
			elif Operator.OperatorGoose.equals(operator):
				codeInfo=cls.encodeAsGoose(codeInfoList)
			elif Operator.OperatorLoop.equals(operator):
				codeInfo=cls.encodeAsLoop(codeInfoList)

			elif Operator.OperatorQi.equals(operator):
				codeInfo=cls.encodeAsQi(codeInfoList)
			elif Operator.OperatorZhe.equals(operator):
				codeInfo=cls.encodeAsZhe(codeInfoList)
			elif Operator.OperatorLiao.equals(operator):
				codeInfo=cls.encodeAsLiao(codeInfoList)
			elif Operator.OperatorZai.equals(operator):
				codeInfo=cls.encodeAsZai(codeInfoList)
			elif Operator.OperatorDou.equals(operator):
				codeInfo=cls.encodeAsDou(codeInfoList)

			elif Operator.OperatorTong.equals(operator):
				codeInfo=cls.encodeAsTong(codeInfoList)
			elif Operator.OperatorQu.equals(operator):
				codeInfo=cls.encodeAsQu(codeInfoList)
			elif Operator.OperatorHan.equals(operator):
				codeInfo=cls.encodeAsHan(codeInfoList)
			elif Operator.OperatorLeft.equals(operator):
				codeInfo=cls.encodeAsLeft(codeInfoList)

			elif Operator.OperatorMu.equals(operator):
				codeInfo=cls.encodeAsMu(codeInfoList)
			elif Operator.OperatorZuo.equals(operator):
				codeInfo=cls.encodeAsZuo(codeInfoList)
			elif Operator.OperatorYou.equals(operator):
				codeInfo=cls.encodeAsYou(codeInfoList)
			elif Operator.OperatorLiang.equals(operator):
				codeInfo=cls.encodeAsLiang(codeInfoList)
			elif Operator.OperatorJia.equals(operator):
				codeInfo=cls.encodeAsJia(codeInfoList)

			elif Operator.OperatorLuan.equals(operator):
				codeInfo=cls.encodeAsLuan(codeInfoList)
			elif Operator.OperatorBan.equals(operator):
				codeInfo=cls.encodeAsBan(codeInfoList)

			elif Operator.OperatorLin.equals(operator):
				codeInfo=cls.encodeAsLin(codeInfoList)
			elif Operator.OperatorLi.equals(operator):
				codeInfo=cls.encodeAsLi(codeInfoList)
			elif Operator.OperatorYi.equals(operator):
				codeInfo=cls.encodeAsYi(codeInfoList)

			else:
				codeInfo=cls.encodeAsInvalidate(codeInfoList)
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
	def encodeAsSparrow(cls, codeInfoList):
		"""運算 "雀" """
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

	@classmethod
	def encodeAsYi(cls, codeInfoList):
		"""運算 "燚" """
		firstCodeInfo=codeInfoList[0]

		return cls.encodeAsLi([firstCodeInfo, firstCodeInfo, firstCodeInfo, firstCodeInfo, ])


