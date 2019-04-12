from coding.Base import CodingType
from coding.Base import FontVariance

from .Array import ArrayInfo as CodingInfo
from .Array import ARCodeInfoEncoder as CodeInfoEncoder
from .Array import ARRadixParser as CodingRadixParser

codingType = CodingType.Input
fontVariance = FontVariance.Traditional

codingMethodName = "ar"
codingMethodDir = "gen/qhdata/{method}/".format(method=codingMethodName)
CodingSubstituteFileList = [
	codingMethodDir + 'substitute.yaml',
]
CodingRadixFileList = [
	codingMethodDir + 'radix/CJK.yaml',
	codingMethodDir + 'radix/CJK-A.yaml',
	codingMethodDir + 'radix/adjust.yaml'
]

