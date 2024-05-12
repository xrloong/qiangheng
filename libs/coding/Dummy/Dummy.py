from coding.Base import CodeInfo
from coding.Base import CodeInfoEncoder
from coding.Base import CodingRadixParser

class DummyCodeInfo(CodeInfo):
	pass

class DummyCodeInfoEncoder(CodeInfoEncoder):
	pass

class DummyRadixParser(CodingRadixParser):
	# 多型
	def convertRadixDescToCodeInfo(self, radixDesc):
		return DummyCodeInfo()

