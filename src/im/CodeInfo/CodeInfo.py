class CodeInfo:
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

	def __init__(self, propDict={}):
		self.setDataEmpty()
		self.setSingleDataEmpty()

		self.codeType=CodeInfo.CODE_TYPE_STANDARD
		self.setCodeTypeProperties(propDict)
		self.setRadixCodeProperties(propDict)

	def __str__(self):
		return "{{{0}}}".format(self.getCode())

	def __repr__(self):
		return str(self)

	def setRadixCodeProperties(self, propDict):
		pass

	def setCodeTypeProperties(self, propDict):
		typeString=propDict.get('類型')
		if typeString:
			self.codeType=CodeInfo.codeTypeStringDict.get(typeString)

	def setCompositions(self, operator, complist):
		# 計算倉頡碼時，需要知道此字的組成方向
		# 計算行列、大易、嘸蝦米及鄭碼時，不需要知道此字的組成方向
		codeType=self.getCodeType()
		for codeInfo in complist:
			tmpCodeType=codeInfo.getCodeType()
			if tmpCodeType>codeType:
				codeType=tmpCodeType
		self.codeType=codeType

		self.setByComps(operator, complist)

	def setByComps(self, operator, complist):
		pass

	def getCodeType(self):
		return self.codeType

	def getCodeProperties(self):
		characterCode=self.characterCode
		if characterCode:
			return [characterCode, CodeInfo.codeTypeDict.get(self.codeType)]
		else:
			return []

	def setDataEmpty(self):
		pass

	def setSingleDataEmpty(self):
		pass

	@property
	def code(self):
		return self.characterCode

	@property
	def characterCode(self):
		return None

	@property
	def radixCode(self):
		return None

