from enum import Enum

class GXGenre(Enum):
	# 「中」體
	Zhong = 1

	# 「國」體
	Guo = 2

	# 「字」體
	Zi = 3

	# 「庋」體
	Gui = 4

	# 「㩪」體
	Xie = 5

class GXStroke(Enum):
	Stroke0 = '0'
	Stroke1 = '1'
	Stroke2 = '2'
	Stroke3 = '3'
	Stroke4 = '4'
	Stroke5 = '5'
	Stroke6 = '6'
	Stroke7 = '7'
	Stroke8 = '8'
	Stroke9 = '9'
	StrokeNone = 'x'

class GXCorner(Enum):
	TopLeft = 'a'
	TopRight = 'b'
	BottomLeft = 'c'
	BottomRight = 'd'
	CornerNone = None

