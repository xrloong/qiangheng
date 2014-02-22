
class CharacterDescriptionRearranger:
	def __init__(self, operationMgr):
		self.operationMgr=operationMgr

	def rearrange(self, charDesc):
		pass

	def rearrangeRecursively(self, charDesc):
		operationMgr=self.operationMgr
		operationMgr.rearrangeDesc(charDesc)
		for childDesc in charDesc.getCompList():
			operationMgr.rearrangeRecursively(childDesc)
		return charDesc

