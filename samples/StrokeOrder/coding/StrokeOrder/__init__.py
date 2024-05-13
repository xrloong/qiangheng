from coding.Base import CodingType
from coding.Base import FontVariance

from .StrokeOrder import SOCodeInfoEncoder as CodeInfoEncoder
from .StrokeOrder import SORadixParser as CodingRadixParser
from .StrokeOrder import SOCodeMappingInfoInterpreter

codingType = CodingType.Input
fontVariance = FontVariance.Traditional
codeMappingInfoInterpreter = SOCodeMappingInfoInterpreter(codingType)

codingMethodName = "dc"
codingMethodDir = "gen/qhdata/{method}/".format(method=codingMethodName)
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
CodingTemplateFile = codingMethodDir + 'radix/template.yaml'

