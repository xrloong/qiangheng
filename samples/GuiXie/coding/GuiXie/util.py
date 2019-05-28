from .constant import GXGenre
from .constant import GXStroke
from .constant import GXCorner

genreToCodeDict = {
	GXGenre.Zhong: "1",
	GXGenre.Guo: "2",
	GXGenre.Zi: "3",
	GXGenre.Gui: "4",
	GXGenre.Xie: "5",
}

charToStrokeDict = {
	"0": GXStroke.Stroke0,
	"1": GXStroke.Stroke1,
	"2": GXStroke.Stroke2,
	"3": GXStroke.Stroke3,
	"4": GXStroke.Stroke4,
	"5": GXStroke.Stroke5,
	"6": GXStroke.Stroke6,
	"7": GXStroke.Stroke7,
	"8": GXStroke.Stroke8,
	"9": GXStroke.Stroke9,
	"x": GXStroke.StrokeNone,
	"X": GXStroke.StrokeNone,
}

charToCornerDict = {
	"a": GXCorner.TopLeft,
	"A": GXCorner.TopLeft,
	"b": GXCorner.TopRight,
	"B": GXCorner.TopRight,
	"c": GXCorner.BottomLeft,
	"C": GXCorner.BottomLeft,
	"d": GXCorner.BottomRight,
	"D": GXCorner.BottomRight,
}

def constructCorners(cornerDescs):
	global charToStrokeDict
	global charToCornerDict

	corners = []
	for c in cornerDescs:
		if c in charToStrokeDict:
			stroke = charToStrokeDict[c]
			corners.append(stroke)
		elif c in charToCornerDict:
			corner = charToCornerDict[c]
			corners.append(corner)
		else:
			corners.append(None)
	return tuple(corners)

def computeGenreCode(genre: GXGenre):
	global genreToCodeDict
	return genreToCodeDict[genre]

def computeStrokeCode(stroke: GXStroke):
	if stroke == GXStroke.StrokeNone:
		return "0"
	else:
		return stroke.value

def computeRectCountCode(rectCount):
	if rectCount < 0:
		return "0"
	elif 0 <= rectCount <= 9:
		return "{}".format(rectCount)
	elif 9 < rectCount:
		return "9"
	else:
		return "0"

