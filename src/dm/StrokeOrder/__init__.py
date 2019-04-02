from .StrokeOrder import StrokeOrderInfo as CodingInfo
from .StrokeOrder import SOCodeInfoEncoder as CodeInfoEncoder
from .StrokeOrder import SORadixParser as CodingRadixParser

codingMethodName = "dy"
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

