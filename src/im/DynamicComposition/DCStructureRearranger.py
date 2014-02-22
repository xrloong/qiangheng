from ..base.StructureRearranger import StructureRearranger
from im.gear import Operator

class DCStructureRearranger(StructureRearranger):

	def rearrangeSpecial(self, structDesc):
		operator=structDesc.getOperator()
		compList=structDesc.getCompList()
		lenCompList=len(compList)

		if operator.getName()=='範產':
			tmpStructDesc_文=self.generateStructureDescriptionWithName('文')
			tmpStructDesc_厂=self.generateStructureDescriptionWithName('厂')
			tmpChildStructDesc_0=structDesc.getCompList()[0]
			tmpStructDesc=self.generateStructureDescription(['範廖', [tmpStructDesc_厂,tmpChildStructDesc_0]])
			structDesc.setOperator(Operator.OperatorSilkworm)
			structDesc.setCompList([tmpStructDesc_文, tmpStructDesc])

		if operator.getName()=='範湘' and lenCompList>=2:
			self.rearrangeForFanYan(structDesc)

	def getRearrangeListFanYan(self):
		rearrangeList=[
			['儿.0', '儿.1', ['丿', '乚']],
			]
		return rearrangeList

