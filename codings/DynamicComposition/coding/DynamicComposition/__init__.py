from coding.Base import CodingType
from coding.Base import FontVariance

from .DynamicComposition import DCCodeInfoEncoder as CodeInfoEncoder
from .DynamicComposition import DCRadixParser as CodingRadixParser
from .DynamicComposition import DCCodeMappingInfoInterpreter

codingType = CodingType.Drawing
fontVariance = FontVariance.Traditional
codeMappingInfoInterpreter = DCCodeMappingInfoInterpreter(codingType)

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

