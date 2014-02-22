from ..base.StructureRearranger import StructureRearranger
from im.gear import Operator

class ZMStructureRearranger(StructureRearranger):

	def rearrangeSpecial(self, structDesc):
		operator=structDesc.getOperator()
		if operator.getName()=='範焤':
			compList=structDesc.getCompList()
			childStructDesc=compList[0]
			if childStructDesc.getReferenceExpression() in ['辰', '廣']:
				structDesc.setOperator(Operator.OperatorLiao)

		return False

