from ..base.StructureRearranger import StructureRearranger
from im.gear import Operator

class CJStructureRearranger(StructureRearranger):

	def rearrangeSpecial(self, structDesc):
		operator=structDesc.getOperator()
		compList=structDesc.getCompList()
		if operator.getName()=='範產':
			tmpStructDesc_文=self.generateStructureDescriptionWithName('文')
			tmpStructDesc_厂=self.generateStructureDescriptionWithName('厂')
			tmpChildStructDesc_0=structDesc.getCompList()[0]
			tmpStructDesc=self.generateStructureDescription(['範廖', [tmpStructDesc_厂,tmpChildStructDesc_0]])
			structDesc.setOperator(Operator.OperatorSilkworm)
			structDesc.setCompList([tmpStructDesc_文, tmpStructDesc])
		if operator.getName()=='範焤':
			self.rearrangeForFanFu(structDesc)

		if operator.getName()=='範湘' and len(compList)>=2:
			firstStructDesc=compList[0]
			lastStructDesc=compList[-1]
			if firstStructDesc.getReferenceExpression()=='儿.0' and lastStructDesc.getReferenceExpression()=='儿.1':
				tmpStructDesc_丨=self.generateStructureDescriptionWithName('丨')
				tmpStructDesc_乚=self.generateStructureDescriptionWithName('乚')
				structDesc.setOperator(Operator.OperatorGoose)
				structDesc.setCompList([tmpStructDesc_丨]+compList[1:-1]+[tmpStructDesc_乚])

	def getRearrangeListFanFu(self):
		rearrangeList=['厭', '辰', '麻']
		return rearrangeList


