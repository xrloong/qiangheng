from coding.Base import CodingType
from coding.Base import FontVariance

from coding.util import readCodingInfo

from .Boshiamy import BSCodeInfoEncoder as CodeInfoEncoder
from .Boshiamy import BSRadixParser as CodingRadixParser

codingType = CodingType.Input
fontVariance = FontVariance.Traditional

codingMethodName = "bs"
codingMethodDir = "gen/qhdata/{method}/".format(method=codingMethodName)
CodingInfoFile = codingMethodDir + 'info.yaml'
CodingSubstituteFileList = [
	codingMethodDir + 'substitute.yaml',
]
CodingRadixFileList = [
	codingMethodDir + 'radix/CJK.yaml',
	codingMethodDir + 'radix/CJK-A.yaml',
	codingMethodDir + 'radix/adjust.yaml'
]

CodingInfo=lambda :readCodingInfo(CodingInfoFile)

