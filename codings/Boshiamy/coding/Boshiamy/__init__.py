from coding.Base import CodingType
from coding.Base import FontVariance

from .Boshiamy import BoshiamyInfo as CodingInfo
from .Boshiamy import BSCodeInfoEncoder as CodeInfoEncoder
from .Boshiamy import BSRadixParser as CodingRadixParser

codingType = CodingType.Input
fontVariance = FontVariance.Traditional

codingMethodName = "bs"
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

