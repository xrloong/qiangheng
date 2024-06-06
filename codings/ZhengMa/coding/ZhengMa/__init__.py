from coding.Input import FontVariance
from coding.Input import CodeMappingInfoInterpreter

from .ZhengMa import ZMCodeInfoEncoder as CodeInfoEncoder
from .ZhengMa import ZMRadixParser as CodingRadixParser

fontVariance = FontVariance.Simplified
codeMappingInfoInterpreter = CodeMappingInfoInterpreter()

codingMethodName = "zm"
codingMethodDir = "gen/qhdata/{method}/".format(method = codingMethodName)
CodingSubstituteFileList = [
	codingMethodDir + 'substitute.yaml',
]
CodingRadixFileList = [
	codingMethodDir + 'radix/CJK.yaml',
	codingMethodDir + 'radix/CJK-A.yaml',
]
CodingAdjustFileList = [
	codingMethodDir + 'adjust.yaml'
]
CodingFastFile = codingMethodDir + "fast.yaml"

