from .constant import FCStroke

charToStrokeDict = {
	"0": FCStroke.Stroke0,
	"1": FCStroke.Stroke1,
	"2": FCStroke.Stroke2,
	"3": FCStroke.Stroke3,
	"4": FCStroke.Stroke4,
	"5": FCStroke.Stroke5,
	"6": FCStroke.Stroke6,
	"7": FCStroke.Stroke7,
	"8": FCStroke.Stroke8,
	"9": FCStroke.Stroke9,
}

def convertCharToCornerUnit(characterCode):
	if characterCode in charToStrokeDict:
		return charToStrokeDict.get(characterCode, FCStroke.StrokeNone)
	return characterCode

def computeCornerUnitCode(stroke: FCStroke):
	if isinstance(stroke, FCStroke):
		if stroke == FCStroke.StrokeNone:
			return "0"
		return stroke.value
	return stroke
