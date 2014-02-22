from ..base.StructureRearranger import StructureRearranger
from im.gear import Operator

class CJStructureRearranger(StructureRearranger):

	def rearrangeSpecial(self, structDesc):
		operator=structDesc.getOperator()
		if operator.getName()=='範焤':
			self.rearrangeForFanFu(structDesc)

		return False

	def getRearrangeListFanFu(self):
		rearrangeList=['厭', '辰', '麻']
		return rearrangeList


