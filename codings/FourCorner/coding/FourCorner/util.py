from .constant import FCStroke
from .constant import FCCorner

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
    "x": FCStroke.StrokeNone,
    "X": FCStroke.StrokeNone,
}

charToCornerDict = {
    "a": FCCorner.TopLeft,
    "A": FCCorner.TopLeft,
    "b": FCCorner.TopRight,
    "B": FCCorner.TopRight,
    "c": FCCorner.BottomLeft,
    "C": FCCorner.BottomLeft,
    "d": FCCorner.BottomRight,
    "D": FCCorner.BottomRight,
}


def convertCharToCornerUnit(characterCode):
    if characterCode in charToStrokeDict:
        return charToStrokeDict.get(characterCode, FCStroke.StrokeNone)
    elif characterCode in charToCornerDict:
        return charToCornerDict.get(characterCode, FCCorner.CornerNone)
    return characterCode


def computeCornerUnitCode(stroke: FCStroke):
    if isinstance(stroke, FCStroke):
        if stroke == FCStroke.StrokeNone:
            return "0"
        return stroke.value
    elif isinstance(stroke, FCCorner):
        return "0"
    return stroke


def convertCornerCodeToCornerUnits(code):
    if len(code) == 4:
        top_left = convertCharToCornerUnit(code[0])
        top_right = convertCharToCornerUnit(code[1])
        bottom_left = convertCharToCornerUnit(code[2])
        bottom_right = convertCharToCornerUnit(code[3])
        corners = [top_left, top_right, bottom_left, bottom_right]
    else:
        corners = [
            FCStroke.StrokeNone,
            FCStroke.StrokeNone,
            FCStroke.StrokeNone,
            FCStroke.StrokeNone,
        ]
    return corners
