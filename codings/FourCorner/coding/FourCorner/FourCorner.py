from coding.Input import CodeInfo
from coding.Input import CodeInfoEncoder
from coding.Input import CodingRadixParser

from .constant import FCCorner

from .item import FCLump

from .util import convertCornerCodeToCornerUnits
from .util import computeCornerUnitCode

class FCCodeInfo(CodeInfo):
	def __init__(self, lump, innerLump = None):
		super().__init__()
		self._cornerLump = FCLump(lump)

		codeCorner = ()
		if innerLump:
			codes1 = lump.computeCodesOfTop()
			codes2 = innerLump.computeCodesOfBottom()
			codeCorner = codes1 + codes2
		else:
			codeCorner = lump.computeCodesOfAll()
		self._codeLump = FCLump(codeCorner)

	@property
	def code(self):
		return "%s%s%s%s"%(computeCornerUnitCode(self.codeLump.topLeft),
				computeCornerUnitCode(self.codeLump.topRight),
				computeCornerUnitCode(self.codeLump.bottomLeft),
				computeCornerUnitCode(self.codeLump.bottomRight))

	@property
	def cornerLump(self):
		return self._cornerLump

	@property
	def codeLump(self):
		return self._codeLump

	@property
	def topLeft(self):
		return self.cornerLump.topLeft

	@property
	def topRight(self):
		return self.cornerLump.topRight

	@property
	def bottomLeft(self):
		return self.cornerLump.bottomLeft

	@property
	def bottomRight(self):
		return self.cornerLump.bottomRight


class FCCodeInfoEncoder(CodeInfoEncoder):
	def generateDefaultCodeInfo(self, corners):
		lump = FCLump(corners)
		return FCCodeInfo(lump)

	def isAvailableOperation(self, codeInfoList):
		return True


	def encodeAsEqual(self, codeInfoList):
		"""運算 "爲" """
		targetCodeInfo = codeInfoList[0]
		corners = [targetCodeInfo.topLeft,
			targetCodeInfo.topRight,
			targetCodeInfo.bottomLeft,
			targetCodeInfo.bottomRight ]
		codeInfo = self.generateDefaultCodeInfo(corners)
		return codeInfo


	def encodeAsLoop(self, codeInfoList):
		"""運算 "回" """
		firstCodeInfo = codeInfoList[0]
		lastCodeInfo = codeInfoList[-1]

		lump1 = firstCodeInfo.cornerLump
		lump2 = lastCodeInfo.cornerLump

		if lump1.sl:
			fcLump1 = FCLump(lump1)
			fcLump2 = FCLump(lump1.computeCodesOfTop() + lump2.computeCodesOfBottom())
			return FCCodeInfo(fcLump1, fcLump2)
		else:
			lump = firstCodeInfo.cornerLump
			return FCCodeInfo(FCLump(lump))

	def encodeAsSilkworm(self, codeInfoList):
		firstCodeInfo = codeInfoList[0]
		lastCodeInfo = codeInfoList[-1]

		lump1 = firstCodeInfo.cornerLump
		lump2 = lastCodeInfo.cornerLump


		corner1 = lump1.computeCodesOfTop()
		corner2 = lump2.computeCodesOfBottom()
		corners = [corner1[0], corner1[1], corner2[0], corner2[1]]
		return FCCodeInfo(FCLump(corners))

	def encodeAsGoose(self, codeInfoList):
		firstCodeInfo = codeInfoList[0]
		lastCodeInfo = codeInfoList[-1]

		lump1 = firstCodeInfo.cornerLump
		lump2 = lastCodeInfo.cornerLump

		corner1 = lump1.computeCodesOfLeft()
		corner2 = lump2.computeCodesOfRight()
		corners = [corner1[0], corner2[0], corner1[1], corner2[1]]
		return FCCodeInfo(FCLump(corners))

	def encodeAsQi(self, codeInfoList):
		firstCodeInfo = codeInfoList[0]
		lastCodeInfo = codeInfoList[-1]

		lump1 = firstCodeInfo.cornerLump
		lump2 = lastCodeInfo.cornerLump

		corner1 = lump1.computeCodesOfExceptTopRight()
		corner2 = lump2.computeCodesOfTopRight()
		corners = [corner1[0], corner2[0], corner1[1], corner1[2]]
		return FCCodeInfo(FCLump(corners))

	def encodeAsLiao(self, codeInfoList):
		firstCodeInfo = codeInfoList[0]
		lastCodeInfo = codeInfoList[-1]

		lump1 = firstCodeInfo.cornerLump
		lump2 = lastCodeInfo.cornerLump

		corner1 = lump1.computeCodesOfExceptBottomRight()
		corner2 = lump2.computeCodesOfBottomRight()
		corners = [corner1[0], corner1[1], corner1[2], corner2[0]]
		return FCCodeInfo(FCLump(corners))

	def encodeAsZai(self, codeInfoList):
		firstCodeInfo = codeInfoList[0]
		lastCodeInfo = codeInfoList[-1]

		lump1 = firstCodeInfo.cornerLump
		lump2 = lastCodeInfo.cornerLump

		corner1 = lump1.computeCodesOfExceptBottomLeft()
		corner2 = lump2.computeCodesOfBottomLeft()
		corners = [corner1[0], corner1[1], corner2[0], corner1[2]]
		return FCCodeInfo(FCLump(corners))

	def encodeAsDou(self, codeInfoList):
		firstCodeInfo = codeInfoList[0]
		lastCodeInfo = codeInfoList[-1]

		lump1 = firstCodeInfo.cornerLump
		lump2 = lastCodeInfo.cornerLump

		corner1 = lump1.computeCodesOfExceptTopLeft()
		corner2 = lump2.computeCodesOfTopLeft()
		corners = [corner2[0], corner1[0], corner1[1], corner1[2]]
		return FCCodeInfo(FCLump(corners))

	def encodeAsMu(self, codeInfoList):
		firstCodeInfo = codeInfoList[0]
		secondCodeInfo = codeInfoList[1]
		thirdCodeInfo = codeInfoList[2]

		lump1 = firstCodeInfo.cornerLump
		lump2 = secondCodeInfo.cornerLump
		lump3 = thirdCodeInfo.cornerLump

		corner1 = lump1.computeCodesOfTop()
		corner2 = lump2.computeCodesOfBottomLeft()
		corner3 = lump2.computeCodesOfBottomRight()
		corners = [corner1[0], corner1[1], corner2[0], corner3[0]]
		return FCCodeInfo(FCLump(corners))

	def encodeAsZuo(self, codeInfoList):
		firstCodeInfo = codeInfoList[0]
		secondCodeInfo = codeInfoList[1]
		thirdCodeInfo = codeInfoList[2]

		lump1 = firstCodeInfo.cornerLump
		lump2 = secondCodeInfo.cornerLump
		lump3 = thirdCodeInfo.cornerLump

		corner1 = lump1.computeCodesOfBottom()
		corner2 = lump2.computeCodesOfTopLeft()
		corner3 = lump3.computeCodesOfTopRight()
		corners = [corner2[0], corner3[0], corner1[0], corner1[1]]
		return FCCodeInfo(FCLump(corners))

	def encodeAsYou(self, codeInfoList):
		firstCodeInfo = codeInfoList[0]
		secondCodeInfo = codeInfoList[1]
		thirdCodeInfo = codeInfoList[2]

		lump1 = firstCodeInfo.cornerLump
		lump2 = secondCodeInfo.cornerLump
		lump3 = thirdCodeInfo.cornerLump

		corners = lump1.computeCodesOfAll()
		return FCCodeInfo(FCLump(corners))

	def encodeAsLiang(self, codeInfoList):
		firstCodeInfo = codeInfoList[0]
		secondCodeInfo = codeInfoList[1]
		thirdCodeInfo = codeInfoList[2]

		lump1 = firstCodeInfo.cornerLump
		lump2 = secondCodeInfo.cornerLump
		lump3 = thirdCodeInfo.cornerLump

		corners = lump1.computeCodesOfAll()
		return FCCodeInfo(FCLump(corners))

	def encodeAsJia(self, codeInfoList):
		firstCodeInfo = codeInfoList[0]
		secondCodeInfo = codeInfoList[1]
		thirdCodeInfo = codeInfoList[2]

		lump1 = firstCodeInfo.cornerLump
		lump2 = secondCodeInfo.cornerLump
		lump3 = thirdCodeInfo.cornerLump

		corners = lump1.computeCodesOfAll()
		return FCCodeInfo(FCLump(corners))

class FCRadixParser(CodingRadixParser):
	ATTRIB_CODE_EXPRESSION = '編碼表示式'
	ATTRIB_ARCHITECTURE = '結構'

	@staticmethod
	def convertCornerCodeToLump(cornerCode):
		sl = (cornerCode[0] == '*')
		if cornerCode[0] == '*':
			cornerCode = cornerCode[1:5]

		corner = convertCornerCodeToCornerUnits(cornerCode)
		lump = FCLump(corner, sl)
		return lump

	# 多型
	def convertRadixDescToCodeInfo(self, radixDesc):
		codeInfo = self.convertRadixDescToCodeInfoByExpression(radixDesc)
		return codeInfo

	def convertRadixDescToCodeInfoByExpression(self, radixInfo):
		elementCodeInfo = radixInfo.codeElement

		codes = elementCodeInfo.get(FCRadixParser.ATTRIB_CODE_EXPRESSION)
		cornerCodeList = codes.split("|")
		lumps = tuple(map(FCRadixParser.convertCornerCodeToLump, cornerCodeList))

		if len(lumps) >=  2:
			codeInfo = FCCodeInfo(lumps[0], lumps[1])
		elif len(lumps) == 1:
			codeInfo = FCCodeInfo(lumps[0])
		return codeInfo

