from coding.Base import CodeInfo
from coding.Base import CodeInfoEncoder
from coding.Base import CodingRadixParser

from .constant import FCCorner

from .item import FCLump
from .item import FCGrid

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

	def toCode(self):
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


	def encodeAsTurtle(self, codeInfoList):
		"""運算 "龜" """
		print("不合法的運算：龜", file=sys.stderr)
		codeInfo=self.encodeAsInvalidate(codeInfoList)
		return codeInfo

	def encodeAsLoong(self, codeInfoList):
		"""運算 "龍" """
		print("不合法的運算：龍", file=sys.stderr)
		codeInfo=self.encodeAsInvalidate(codeInfoList)
		return codeInfo

	def encodeAsSparrow(self, codeInfoList):
		"""運算 "雀" """
		firstCodeInfo = codeInfoList[0]
		lastCodeInfo = codeInfoList[-1]

		lump1 = firstCodeInfo.cornerLump
		lump2 = lastCodeInfo.cornerLump

		fcLump1 = FCLump(lump1)
		fcLump2 = FCLump(lump1.computeCodesOfTop() + lump2.computeCodesOfBottom())
		return FCCodeInfo(fcLump1, fcLump2)

	def encodeAsEqual(self, codeInfoList):
		"""運算 "爲" """
		targetCodeInfo=codeInfoList[0]
		corners=[targetCodeInfo.topLeft,
			targetCodeInfo.topRight,
			targetCodeInfo.bottomLeft,
			targetCodeInfo.bottomRight ]
		codeInfo=self.generateDefaultCodeInfo(corners)
		return codeInfo


	def encodeAsLoop(self, codeInfoList):
		firstCodeInfo = codeInfoList[0]
		lastCodeInfo = codeInfoList[-1]

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
		firstCodeInfo=codeInfoList[0]
		lastCodeInfo=codeInfoList[-1]

		grid=FCGrid()
		grid.setAsLeft_Right(firstCodeInfo, lastCodeInfo)
		[top_left, top_right, bottom_left, bottom_right]=grid.getFourCorner()
		corners=[top_left, top_right, bottom_left, bottom_right]
		codeInfo=self.generateDefaultCodeInfo(corners)
		return codeInfo

	def encodeAsQi(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		lastCodeInfo=codeInfoList[-1]

		grid=FCGrid()
		grid.setAsBottomLeft_TopRight(firstCodeInfo, lastCodeInfo)
		[top_left, top_right, bottom_left, bottom_right]=grid.getFourCorner()
		corners=[top_left, top_right, bottom_left, bottom_right]
		codeInfo=self.generateDefaultCodeInfo(corners)
		return codeInfo

	def encodeAsLiao(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		lastCodeInfo=codeInfoList[-1]

		grid=FCGrid()
		grid.setAsTopLeft_BottomRight(firstCodeInfo, lastCodeInfo)
		[top_left, top_right, bottom_left, bottom_right]=grid.getFourCorner()
		corners=[top_left, top_right, bottom_left, bottom_right]
		codeInfo=self.generateDefaultCodeInfo(corners)
		return codeInfo

	def encodeAsZai(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		lastCodeInfo=codeInfoList[-1]

		grid=FCGrid()
		grid.setAsTopRight_BottomLeft(firstCodeInfo, lastCodeInfo)
		[top_left, top_right, bottom_left, bottom_right]=grid.getFourCorner()
		corners=[top_left, top_right, bottom_left, bottom_right]
		codeInfo=self.generateDefaultCodeInfo(corners)
		return codeInfo

	def encodeAsDou(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		lastCodeInfo=codeInfoList[-1]

		grid=FCGrid()
		grid.setAsBottomRight_TopLeft(firstCodeInfo, lastCodeInfo)
		[top_left, top_right, bottom_left, bottom_right]=grid.getFourCorner()
		corners=[top_left, top_right, bottom_left, bottom_right]
		codeInfo=self.generateDefaultCodeInfo(corners)
		return codeInfo

	def encodeAsMu(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		grid=FCGrid()
		grid.setAsTop_BottomLeft_BottomRight(firstCodeInfo, secondCodeInfo, thirdCodeInfo)
		[top_left, top_right, bottom_left, bottom_right]=grid.getFourCorner()
		corners=[top_left, top_right, bottom_left, bottom_right]
		codeInfo=self.generateDefaultCodeInfo(corners)
		return codeInfo

	def encodeAsZuo(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		grid=FCGrid()
		grid.setAsBottom_TopLeft_TopRight(firstCodeInfo, secondCodeInfo, thirdCodeInfo)
		[top_left, top_right, bottom_left, bottom_right]=grid.getFourCorner()
		corners=[top_left, top_right, bottom_left, bottom_right]
		codeInfo=self.generateDefaultCodeInfo(corners)
		return codeInfo

	def encodeAsYou(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		grid=FCGrid()
		grid.setAsBottom_InTopLeft_InTopRight(firstCodeInfo, secondCodeInfo, thirdCodeInfo)
		[top_left, top_right, bottom_left, bottom_right]=grid.getFourCorner()
		corners=[top_left, top_right, bottom_left, bottom_right]
		codeInfo=self.generateDefaultCodeInfo(corners)
		return codeInfo

	def encodeAsLiang(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		grid=FCGrid()
		grid.setAsTop_InBottomLeft_InBottomRight(firstCodeInfo, secondCodeInfo, thirdCodeInfo)
		[top_left, top_right, bottom_left, bottom_right]=grid.getFourCorner()
		corners=[top_left, top_right, bottom_left, bottom_right]
		codeInfo=self.generateDefaultCodeInfo(corners)
		return codeInfo

	def encodeAsJia(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		secondCodeInfo=codeInfoList[1]
		thirdCodeInfo=codeInfoList[2]

		grid=FCGrid()
		grid.setAsBottom_InTopLeft_InTopRight(firstCodeInfo, secondCodeInfo, thirdCodeInfo)
		[top_left, top_right, bottom_left, bottom_right]=grid.getFourCorner()
		corners=[top_left, top_right, bottom_left, bottom_right]
		codeInfo=self.generateDefaultCodeInfo(corners)
		return codeInfo

class FCRadixParser(CodingRadixParser):
	ATTRIB_CODE_EXPRESSION='編碼表示式'
	ATTRIB_ARCHITECTURE='結構'

	# 多型
	def convertRadixDescToCodeInfo(self, radixDesc):
		codeInfo=self.convertRadixDescToCodeInfoByExpression(radixDesc)
		return codeInfo

	def convertRadixDescToCodeInfoByExpression(self, radixInfo):
		elementCodeInfo = radixInfo.getCodeElement()

		cornerCodeList = elementCodeInfo.get(FCRadixParser.ATTRIB_ARCHITECTURE)
		corners = tuple(convertCornerCodeToCornerUnits(cornerCode) for cornerCode in cornerCodeList)

		if len(corners) >= 2:
			codeInfo = FCCodeInfo(FCLump(corners[0]), FCLump(corners[1]))
		elif len(corners) == 1:
			codeInfo = FCCodeInfo(FCLump(corners[0]))
		return codeInfo

