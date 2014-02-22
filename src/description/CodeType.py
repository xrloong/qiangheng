class CodeType:
	CODE_TYPE_STANDARD=0
	CODE_TYPE_SIMPLIFIED=1
	CODE_TYPE_TOLERANT=2
	codeTypeDict={
		CODE_TYPE_STANDARD:"標準",
		CODE_TYPE_SIMPLIFIED:"簡快",
		CODE_TYPE_TOLERANT:"容錯",
	}

	codeTypeStringDict={
		"標準":CODE_TYPE_STANDARD,
		"簡快":CODE_TYPE_SIMPLIFIED,
		"容錯":CODE_TYPE_TOLERANT,
	}

	def __init__(self):
		self.codeType=CodeType.CODE_TYPE_STANDARD

	def setType(self, codeType):
		self.codeType=codeType

	def getType(self):
		return self.codeType

	def setTypeString(self, codeTypeString):
		codeType=CodeType.codeTypeStringDict.get(codeTypeString, CodeType.CODE_TYPE_STANDARD)
		self.setType(codeType)

	def getTypeString(self):
		codeType=self.getType()
		codeTypeString=CodeType.codeTypeDict.get(codeType)
		return codeTypeString

	def multi(self, xType):
		codeType=self.getType()
		if codeType<xType.getType():
			codeType=xType.getType()
		self.setType(codeType)

