from coding.Base import CodingType
from coding.Base import FontVariance

from coding.util import readCodingInfo

from .DynamicComposition import DCCodeInfoEncoder as CodeInfoEncoder
from .DynamicComposition import DCRadixParser as CodingRadixParser

codingType = CodingType.Drawing
fontVariance = FontVariance.Traditional

codingMethodName = "dc"
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
CodingTemplateFile = codingMethodDir + 'radix/template.yaml'

CodingInfo=lambda :readCodingInfo(CodingInfoFile)

