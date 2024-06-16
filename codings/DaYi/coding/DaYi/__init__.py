from coding.Input import FontVariance
from coding.Input import CodeMappingInfoInterpreter

from .DaYi import DYCodeInfoEncoder as CodeInfoEncoder
from .DaYi import DYRadixParser as CodingRadixParser

fontVariance = FontVariance.Traditional
codeMappingInfoInterpreter = CodeMappingInfoInterpreter()

codingMethodName = "dy"
codingMethodDir = "gen/qhdata/{method}/".format(method=codingMethodName)
CodingSubstituteFileList = [
    codingMethodDir + "substitute.yaml",
]
CodingRadixFileList = [
    codingMethodDir + "radix/CJK.yaml",
    codingMethodDir + "radix/CJK-A.yaml",
]
CodingAdjustFileList = [codingMethodDir + "adjust.yaml"]
