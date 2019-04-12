from coding.Base import CodingType
from coding.Base import FontVariance

from .StrokeOrder import StrokeOrderInfo as CodingInfo
from .StrokeOrder import SOCodeInfoEncoder as CodeInfoEncoder
from .StrokeOrder import SORadixParser as CodingRadixParser

codingType = CodingType.Input
fontVariance = FontVariance.Traditional

codingMethodName = "dy"
codingMethodDir = "gen/qhdata/{method}/".format(method=codingMethodName)
CodingSubstituteFileList = [
	codingMethodDir + 'substitute.yaml',
]
CodingRadixFileList = [
	codingMethodDir + 'radix/CJK.yaml',
	codingMethodDir + 'radix/CJK-A.yaml',
	codingMethodDir + 'radix/adjust.yaml'
]

