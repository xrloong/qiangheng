from coding.Base import FontVariance
from coding.Base import CodeMappingInfoInterpreter

from .FourCorner import FCCodeInfoEncoder as CodeInfoEncoder
from .FourCorner import FCRadixParser as CodingRadixParser

fontVariance = FontVariance.Traditional
codeMappingInfoInterpreter = CodeMappingInfoInterpreter()

codingMethodName = "fc"
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

