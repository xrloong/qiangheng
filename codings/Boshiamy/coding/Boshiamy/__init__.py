from coding.Input import FontVariance
from coding.Input import CodeMappingInfoInterpreter

from .Boshiamy import BSCodeInfoEncoder as CodeInfoEncoder
from .Boshiamy import BSRadixParser as CodingRadixParser

fontVariance = FontVariance.Traditional
codeMappingInfoInterpreter = CodeMappingInfoInterpreter()

codingMethodName = "bs"
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

