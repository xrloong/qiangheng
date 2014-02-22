from im.gear import OperatorManager

class StructureRearranger:
	def __init__(self):
		pass

	def rearrangeOn(self, charDesc):
		structDescList=charDesc.getStructureList()
		for structDesc in structDescList:
			self.rearrangeRecursively(structDesc)

	def rearrangeRecursively(self, structDesc):
		self.rearrangeDesc(structDesc)
		for childDesc in structDesc.getCompList():
			self.rearrangeRecursively(childDesc)
		return structDesc

	def rearrangeDesc(self, structDesc):
		if self.rearrangeSpecial(structDesc):
			pass
		else:
			operator=structDesc.getOperator()
			if not operator.isBuiltin():
				rearrangeInfo=operator.getRearrangeInfo()

				if rearrangeInfo!=None:
					rearrangeInfo.rearrange(structDesc)
					operator=structDesc.getOperator()
					self.rearrangeDesc(structDesc)

	def rearrangeSpecial(self, structDesc):
		return False

