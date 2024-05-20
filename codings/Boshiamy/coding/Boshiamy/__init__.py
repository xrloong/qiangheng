from coding.Base import FontVariance
from coding.Base import CodeMappingInfoInterpreter

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

