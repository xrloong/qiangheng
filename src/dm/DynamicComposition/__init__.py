from model.BaseCoding import CodingType

from .DynamicComposition import DynamicCompositionInfo as CodingInfo
from .DynamicComposition import DCCodeInfoEncoder as CodeInfoEncoder
from .DynamicComposition import DCRadixParser as CodingRadixParser

codingType = CodingType.Drawing
codingMethodName = "dc"
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

if __name__=='__main__':
	pass

