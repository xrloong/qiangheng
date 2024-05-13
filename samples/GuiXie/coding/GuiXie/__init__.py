from coding.Base import CodingType
from coding.Base import FontVariance
from coding.Base import CodeMappingInfoInterpreter

from .GuiXie import GXCodeInfoEncoder as CodeInfoEncoder
from .GuiXie import GXRadixParser as CodingRadixParser

codingType = CodingType.Input
fontVariance = FontVariance.Traditional
codeMappingInfoInterpreter = CodeMappingInfoInterpreter(codingType)

codingMethodName = "gx"
codingMethodDir = "samples/GuiXie/qhdata/"
CodingSubstituteFileList = [
	codingMethodDir + 'substitute.yaml',
]
CodingRadixFileList = [
	codingMethodDir + 'radix/CJK.yaml',
	codingMethodDir + 'radix/CJK-A.yaml',
]
CodingAdjustFileList = [
	codingMethodDir + 'radix/adjust.yaml'
]

