from coding.Base import CodingType
from .GuiXie import GuiXieInfo as CodingInfo
from .GuiXie import GXCodeInfoEncoder as CodeInfoEncoder
from .GuiXie import GXRadixParser as CodingRadixParser

codingType = CodingType.Input

codingMethodName = "gx"
codingMethodDir = "gen/qhdata/{method}/".format(method=codingMethodName)
CodingComponentFileList = [
	codingMethodDir + 'style.yaml',
]
CodingSubstituteFileList = [
	codingMethodDir + 'substitute.yaml',
]
CodingRadixFileList = [
	codingMethodDir + 'radix/CJK.yaml',
	codingMethodDir + 'radix/CJK-A.yaml',
	codingMethodDir + 'radix/adjust.yaml'
]

