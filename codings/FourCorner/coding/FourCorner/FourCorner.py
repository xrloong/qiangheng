from coding.Base import CodeInfo
from coding.Base import CodeInfoEncoder
from coding.Base import CodingRadixParser

from .item import FCLump
from .item import FCGrid

from .util import convertCornerCodeToCornerUnits
from .util import computeCornerUnitCode

class FCCodeInfo(CodeInfo):
	def __init__(self, lump, innerLump = None):
		super().__init__()

		self.lump = lump
		self.innerLump = innerLump

	@staticmethod
	def generateDefaultCodeInfo(lump):
		codeInfo=FCCodeInfo(lump)
		return codeInfo

	def toCode(self):
		if self.innerLump:
			return "%s%s%s%s"%(computeCornerUnitCode(self.topLeft),
					computeCornerUnitCode(self.topRight),
					computeCornerUnitCode(self.innerLump.bottomLeft),
					computeCornerUnitCode(self.innerLump.bottomRight))
		return "%s%s%s%s"%(computeCornerUnitCode(self.topLeft),
				computeCornerUnitCode(self.topRight),
				computeCornerUnitCode(self.bottomLeft),
				computeCornerUnitCode(self.bottomRight))

	@property
	def topLeft(self):
		return self.lump.topLeft

	@property
	def topRight(self):
		return self.lump.topRight

	@property
	def bottomLeft(self):
		return self.lump.bottomLeft

	@property
	def bottomRight(self):
		return self.lump.bottomRight


class FCCodeInfoEncoder(CodeInfoEncoder):
	def generateDefaultCodeInfo(self, corners):
		lump = FCLump(corners)
		return FCCodeInfo.generateDefaultCodeInfo(lump)

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
		firstCodeInfo=codeInfoList[0]
		lastCodeInfo=codeInfoList[-1]
		grid=FCGrid()
		grid.setAsOut_In(firstCodeInfo, lastCodeInfo)
		[top_left, top_right, bottom_left, bottom_right]=grid.getFourCorner()
		corners=[top_left, top_right, bottom_left, bottom_right]
		codeInfo=self.generateDefaultCodeInfo(corners)
		fcLump = FCLump(corners)
		codeInfo=FCCodeInfo(fcLump, lastCodeInfo.lump)
		return codeInfo

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
		firstCodeInfo=codeInfoList[0]
		lastCodeInfo=codeInfoList[-1]
		grid=FCGrid()
		grid.setAsOut_In(firstCodeInfo, lastCodeInfo)
		[top_left, top_right, bottom_left, bottom_right]=grid.getFourCorner()
		corners=[top_left, top_right, bottom_left, bottom_right]
		codeInfo=self.generateDefaultCodeInfo(corners)
		return codeInfo

	def encodeAsSilkworm(self, codeInfoList):
		firstCodeInfo=codeInfoList[0]
		lastCodeInfo=codeInfoList[-1]

		grid=FCGrid()
		grid.setAsTop_Bottom(firstCodeInfo, lastCodeInfo)
		[top_left, top_right, bottom_left, bottom_right]=grid.getFourCorner()
		corners=[top_left, top_right, bottom_left, bottom_right]
		codeInfo=self.generateDefaultCodeInfo(corners)
		return codeInfo

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

