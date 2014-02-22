from im.gear import OperatorManager

class StructureRearranger:
	def __init__(self):
		self.operationMgr=OperatorManager.OperatorManager()

	def rearrangeOn(self, charDesc):
		self.operationMgr.rearrangeOn(charDesc)

	def setTemplateDB(self, templateDB):
		self.operationMgr.setTemplateDB(templateDB)

	def getOperatorGenerator(self):
		return self.operationMgr.getOperatorGenerator()

