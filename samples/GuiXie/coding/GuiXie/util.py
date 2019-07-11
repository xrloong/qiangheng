from .constant import GXGenre
from .constant import GXStroke

genreToCodeDict = {
	GXGenre.Zhong: "1",
	GXGenre.Guo: "2",
	GXGenre.Zi: "3",
	GXGenre.Gui: "4",
	GXGenre.Xie: "5",
}

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

