from coding.Base import CodingType

from .Boshiamy import BoshiamyInfo as CodingInfo
from .Boshiamy import BSCodeInfoEncoder as CodeInfoEncoder
from .Boshiamy import BSRadixParser as CodingRadixParser

codingType = CodingType.Input
codingMethodName = "bs"
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

