from ..base.StructureRearranger import StructureRearranger
from im.gear import Operator

class ZMStructureRearranger(StructureRearranger):

	def rearrangeSpecial(self, structDesc):
		operator=structDesc.getOperator()
		compList=structDesc.getCompList()
		lenCompList=len(compList)
		if operator.getName()=='範焤' and lenCompList>=2:
			self.rearrangeForFanFu(structDesc)

		if operator.getName()=='範湘' and lenCompList>=2:
			self.rearrangeForFanYan(structDesc)

	def getRearrangeListFanFu(self):
		rearrangeList=['辰', '廣']
		return rearrangeList

	def getRearrangeListFanYan(self):
		rearrangeList=[
			['行.0', '行.1', '行'],
			['儿.0', '儿.1', '儿'],
			['[丨丨].0', '[丨丨].1', '[丨丨]'],
			['[丨丿].0', '[丨丿].1', '[丨丿]'],
			['[丿丨].0', '[丿丨].1', '[丿丨]'],
			]
		return rearrangeList

