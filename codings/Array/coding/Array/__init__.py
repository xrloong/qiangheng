from coding.Input import FontVariance
from coding.Input import CodeMappingInfoInterpreter

from .Array import ARCodeInfoEncoder as CodeInfoEncoder
from .Array import ARRadixParser as CodingRadixParser

fontVariance = FontVariance.Traditional
codeMappingInfoInterpreter = CodeMappingInfoInterpreter()

codingMethodName = "ar"
codingMethodDir = "gen/qhdata/{method}/".format(method=codingMethodName)
CodingSubstituteFileList = [
    codingMethodDir + "substitute.yaml",
]
CodingRadixFileList = [
    codingMethodDir + "radix/CJK.yaml",
    codingMethodDir + "radix/CJK-A.yaml",
]
CodingAdjustFileList = [
    codingMethodDir + "adjust.yaml",
]
