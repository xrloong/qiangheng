from coding.Base import CodingType

from .DaYi import DaYiInfo as CodingInfo
from .DaYi import DYCodeInfoEncoder as CodeInfoEncoder
from .DaYi import DYRadixParser as CodingRadixParser

codingType = CodingType.Input
codingMethodName = "dy"
codingMethodDir = "gen/qhdata/{method}/".format(method=codingMethodName)
CodingComponentFileList = [
	codingMethodDir + 'style.yaml',
]
CodingSubstituteFileList = [
	codingMethodDir + 'substitute.yaml',
]
CodingRadixFileList = [
	codingMethodDir + 'radix/CJK.yaml',
	codingMethodDir + 'radix/CJK-A.yaml',
	codingMethodDir + 'radix/adjust.yaml'
]

