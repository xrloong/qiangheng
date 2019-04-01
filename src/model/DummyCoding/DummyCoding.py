from model.BaseCoding import CodingInfo
from model.BaseCoding import CodeInfo
from model.BaseCoding import CodeInfoEncoder

class DummyInfo(CodingInfo):
	pass

class DummyCodeInfo(CodeInfo):
	pass

class DummyCodeInfoEncoder(CodeInfoEncoder):
	pass

class DummyRadixParser():
	# 多型
	def convertRadixDescToCodeInfo(self, radixDesc):
		return DummyCodeInfo()

