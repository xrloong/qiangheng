from coding.Input import FontVariance
from coding.Input import CodeMappingInfoInterpreter

from .GuiXie import GXCodeInfoEncoder as CodeInfoEncoder
from .GuiXie import GXRadixParser as CodingRadixParser

fontVariance = FontVariance.Traditional
codeMappingInfoInterpreter = CodeMappingInfoInterpreter()

codingMethodName = "gx"
codingMethodDir = "samples/GuiXie/qhdata/"
CodingSubstituteFileList = [
    codingMethodDir + "substitute.yaml",
]
CodingRadixFileList = [
    codingMethodDir + "radix/CJK.yaml",
    codingMethodDir + "radix/CJK-A.yaml",
]
CodingAdjustFileList = [codingMethodDir + "adjust.yaml"]
