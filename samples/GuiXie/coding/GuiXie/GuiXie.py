from coding.Base import CodeInfo
from coding.Base import CodeInfoEncoder
from coding.Base import CodingRadixParser

from .constant import GXGenre
from .constant import GXStroke
from .constant import GXCorner
from .item import GXLump
from .util import computeGenreCode, computeStrokeCode, computeRectCountCode
from .util import constructCorners

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

	@property
	def code(self):
		if not self.isValid():
			return ""
		if self._genre != GXGenre.Zhong and len(self._lumps)<=1:
			return ""
		return self.computeCode()

class GXCodeInfoEncoder(CodeInfoEncoder):
	def generateDefaultCodeInfo(self):
		return GXCodeInfo.generateDefaultCodeInfo()

	def isAvailableOperation(self, codeInfoList):
		isAllWithCode=all(map(lambda codeInfo: codeInfo.isValid(), codeInfoList))
		return isAllWithCode

	def encodeAsLoong(self, codeInfoList):
		"""運算 "龍" """
		return self.generateDefaultCodeInfo()

	def encodeAsSilkworm(self, codeInfoList):
		"""運算 "蚕" """
		gxLumps = sum((codeInfo.lumps for codeInfo in codeInfoList), ())
		return GXCodeInfo(GXGenre.Zi, gxLumps)

	def encodeAsGoose(self, codeInfoList):
		"""運算 "鴻" """
		gxLumps = sum((codeInfo.lumps for codeInfo in codeInfoList), ())
		return GXCodeInfo(GXGenre.Xie, gxLumps)

class GXRadixParser(CodingRadixParser):
	ATTRIB_GENRE = '體'
	ATTRIB_COMPONENT = '組件'
	ATTRIB_COMPONENT_CODING = '四角編碼'
	ATTRIB_COMPONENT_RECT_COUNT = '方格數'

	genreNameToGenre = {
		"中": GXGenre.Zhong,
		"國": GXGenre.Guo,
		"字": GXGenre.Zi,
		"庋": GXGenre.Gui,
		"㩪": GXGenre.Xie,
	}

	def convertCompoentDictToLump(self, componentDicts):
		gxLumps = []
		for componentDict in componentDicts:
			codingDesc = componentDict[GXRadixParser.ATTRIB_COMPONENT_CODING]
			rectCount = componentDict.get(GXRadixParser.ATTRIB_COMPONENT_RECT_COUNT, 0)
			corners = constructCorners(codingDesc)
			gxLump = GXLump(corners, rectCount)
			gxLumps.append(gxLump)
		return tuple(gxLumps)

	def convertRadixDescToCodeInfo(self, radixDesc):
		codeElement = radixDesc.getCodeElement()
		if GXRadixParser.ATTRIB_GENRE in codeElement:
			genreDesc = codeElement[GXRadixParser.ATTRIB_GENRE]
			genre = GXRadixParser.genreNameToGenre[genreDesc]
			components = codeElement[GXRadixParser.ATTRIB_COMPONENT]
			gxLumps = self.convertCompoentDictToLump(components)
			return GXCodeInfo(genre, gxLumps)
		else:
			return GXCodeInfo.generateDefaultCodeInfo()

