
class RearrangeInfo:
	def __init__(self):
		pass

	def rearrange(self, charDesc):
		pass

class RearrangeInfoSame(RearrangeInfo):
	def __init__(self):
		pass

	def rearrange(self, charDesc):
		pass

class RearrangeInfoTemplate(RearrangeInfo):
	def __init__(self, templateDesc):
		self.templateDesc=templateDesc

	def rearrange(self, charDesc):
		self.templateDesc.rearrange(charDesc)

