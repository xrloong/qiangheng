from coding.Base import CodingType
from coding.Base import FontVariance

from .ZhengMa import ZhengMaInfo as CodingInfo
from .ZhengMa import ZMCodeInfoEncoder as CodeInfoEncoder
from .ZhengMa import ZMRadixParser as CodingRadixParser

codingType = CodingType.Input
fontVariance = FontVariance.Simplified

codingMethodName = "zm"
codingMethodDir = "gen/qhdata/{method}/".format(method=codingMethodName)
CodingComponentFileList = [
]
CodingSubstituteFileList = [
	codingMethodDir + 'substitute.yaml',
]
CodingRadixFileList = [
	codingMethodDir + 'radix/CJK.yaml',
	codingMethodDir + 'radix/CJK-A.yaml',
	codingMethodDir + 'radix/adjust.yaml'
]

