import abc

class IfCodingInfo(object, metaclass=abc.ABCMeta):
	pass

class IfCodeInfo(object, metaclass=abc.ABCMeta):
	pass

class IfCodeInfoEncoder(object, metaclass=abc.ABCMeta):
	pass

class IfCodingRadixParser(object, metaclass=abc.ABCMeta):
	@abc.abstractmethod
	def convertRadixDescToCodeInfo(self, radixDesc):
		return CodeInfo()

