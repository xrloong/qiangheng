from coding.Base import CodingType
from coding.Base import FontVariance
from coding.Base import CodeMappingInfoInterpreter

from .CangJie import CJCodeInfoEncoder as CodeInfoEncoder
from .CangJie import CJRadixParser as CodingRadixParser

codingType = CodingType.Input
fontVariance = FontVariance.Traditional
codeMappingInfoInterpreter = CodeMappingInfoInterpreter(codingType)

codingMethodName = "cj"
codingMethodDir = "gen/qhdata/{method}/".format(method=codingMethodName)
CodingSubstituteFileList = [
	codingMethodDir + 'substitute.yaml',
]
CodingRadixFileList = [
	codingMethodDir + 'radix/CJK.yaml',
	codingMethodDir + 'radix/CJK-A.yaml',
	codingMethodDir + 'radix/adjust.yaml'
]

