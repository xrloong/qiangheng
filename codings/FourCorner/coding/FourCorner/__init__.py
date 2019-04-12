from coding.Base import CodingType

from .FourCorner import FourCornerInfo as CodingInfo
from .FourCorner import FCCodeInfoEncoder as CodeInfoEncoder
from .FourCorner import FCRadixParser as CodingRadixParser

codingType = CodingType.Input
codingMethodName = "fc"
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

