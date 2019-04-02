from .Array import ArrayInfo as CodingInfo
from .Array import ARCodeInfoEncoder as CodeInfoEncoder
from .Array import ARRadixParser as CodingRadixParser

codingMethodName = "ar"
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

