from coding.Base import CodingType

from .CangJie import CangJieInfo as CodingInfo
from .CangJie import CJCodeInfoEncoder as CodeInfoEncoder
from .CangJie import CJRadixParser as CodingRadixParser

codingType = CodingType.Input
codingMethodName = "cj"
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

