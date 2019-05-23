from coding.Base import CodingType
from coding.Base import FontVariance
from coding.Base import CodeMappingInfoInterpreter

from .ZhengMa import ZMCodeInfoEncoder as CodeInfoEncoder
from .ZhengMa import ZMRadixParser as CodingRadixParser

codingType = CodingType.Input
fontVariance = FontVariance.Simplified
codeMappingInfoInterpreter = CodeMappingInfoInterpreter(codingType)

codingMethodName = "zm"
codingMethodDir = "gen/qhdata/{method}/".format(method=codingMethodName)
CodingSubstituteFileList = [
	codingMethodDir + 'substitute.yaml',
]
CodingRadixFileList = [
	codingMethodDir + 'radix/CJK.yaml',
	codingMethodDir + 'radix/CJK-A.yaml',
	codingMethodDir + 'radix/adjust.yaml'
]

