from coding.Base import CodeInfo
from coding.Base import CodeInfoEncoder
from coding.Base import CodingRadixParser

from .constant import GXGenre
from .constant import GXStroke
from .constant import GXCorner
from .item import GXLump
from .util import computeGenreCode, computeStrokeCode, computeRectCountCode

def computeStrokes(genre: GXGenre, lumps):
	if genre == GXGenre.Zhong:
		lump = lumps[0]
		strokes = lump.computeStrokesOnAllCorners()
	elif genre == GXGenre.Guo:
		lump1 = lumps[0]
		lump2 = lumps[1]
		strokes = lump1.computeStrokesOnMainDiagonal() + lump2.computeStrokesOnMainDiagonal()
	elif genre == GXGenre.Zi:
		lump1 = lumps[0]
		lump2 = lumps[1]
		strokes = lump1.computeStrokesOnMainDiagonal() + lump2.computeStrokesOnMainDiagonal()
	elif genre == GXGenre.Gui:
		lump1 = lumps[0]
		lump2 = lumps[1]
		strokes = lump1.computeStrokesOnAntiDiagonal() + lump2.computeStrokesOnMainDiagonal()
	elif genre == GXGenre.Xie:
		lump1 = lumps[0]
		lump2 = lumps[1]
		strokes = lump1.computeStrokesOnMainDiagonal() + lump2.computeStrokesOnMainDiagonal()
	else:
		strokes = [GXStroke.StrokeNone, GXStroke.StrokeNone, GXStroke.StrokeNone, GXStroke.StrokeNone, ]
	return strokes

def computeBodyCode(genre: GXGenre, lumps):
	strokes = computeStrokes(genre, lumps)
	return "".join(computeStrokeCode(stroke) for stroke in strokes)

class GXCodeInfo(CodeInfo):
	def __init__(self, genre, gxLumps, rectCountDiff=0):
		super().__init__()

		self._genre = genre
		self._lumps = gxLumps

		innerLump = None
		if genre:
			lump1 = gxLumps[0]
			lump2 = gxLumps[-1]
			codes1 = lump1.computeCodesOfTop()
			codes2 = lump2.computeCodesOfBottom()
			codeCorner = codes1 + codes2
			self._cornerLump = GXLump(codeCorner)

		lumpsRectCount = sum(lump.rectCount for lump in gxLumps)
		self._rectCount = lumpsRectCount + rectCountDiff

	@staticmethod
	def generateDefaultCodeInfo():
		return GXCodeInfo(None, ())

	@property
	def genre(self):
		return self._genre

	@property
	def lumps(self):
		return self._lumps

	@property
	def cornerLump(self):
		return self._cornerLump

	@property
	def codeLump(self):
		return self._codeLump

	@property
	def rectCount(self):
		return self._rectCount

	def isValid(self):
		return bool(self.genre)

	def computeGenreCode(self):
		return computeGenreCode(self._genre)

	def computeBodyCode(self):
		return computeBodyCode(self._genre, self._lumps)

	def computeRectCountCode(self):
		return computeRectCountCode(self._rectCount)

	def computeCode(self):
		return "{}/{}{}".format(self.computeGenreCode(), self.computeBodyCode(), self.computeRectCountCode())

	def toCode(self):
		if not self.isValid():
			return ""
		return self.computeCode()

class GXCodeInfoEncoder(CodeInfoEncoder):
	def generateDefaultCodeInfo(self):
		return GXCodeInfo.generateDefaultCodeInfo()

	def isAvailableOperation(self, codeInfoList):
		isAllWithCode=all(map(lambda codeInfo: codeInfo.isValid(), codeInfoList))
		return isAllWithCode

class GXRadixParser(CodingRadixParser):
	def convertRadixDescToCodeInfo(self, radixDesc):
		return GXCodeInfo.generateDefaultCodeInfo()

