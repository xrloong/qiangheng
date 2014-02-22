from ..base.StructureRearranger import StructureRearranger
from im.gear import Operator

class DYStructureRearranger(StructureRearranger):

	def rearrangeSpecial(self, structDesc):
		operator=structDesc.getOperator()
		compList=structDesc.getCompList()
		lenCompList=len(compList)

		if operator.getName()=='範同' and lenCompList>=2:
			firstChilStructDesc=compList[0]
			secondChilStructDesc=compList[1]

			firstName=firstChilStructDesc.getReferenceName()
			secondName=secondChilStructDesc.getReferenceName()

			secondeCompList=secondChilStructDesc.getCompList()
			if firstName=='戊' and len(secondeCompList)>=2:
				secondFirstChilStructDesc=secondeCompList[0]
				secondSecondChilStructDesc=secondeCompList[1]

				secondFirstName=secondFirstChilStructDesc.getReferenceName()

				isMatch=(secondFirstName=='一')

				if isMatch:
					newStructDesc=self.generateStructureDescriptionWithName('[厂一]')
					newStructDesc_特戈=self.generateStructureDescriptionWithName('[特戈]')
					structDescList=[newStructDesc]+secondeCompList[1:]+[newStructDesc_特戈]
					structDesc.setCompList(structDescList)
					structDesc.setOperator(Operator.OperatorGoose)
		if operator.getName()=='範同' and lenCompList>=2:
			pass

		if operator.getName()=='範湘' and lenCompList>=2:
			self.rearrangeForFanYan(structDesc)

	def getRearrangeListFanYan(self):
		rearrangeList=[
			['儿.0', '儿.1', '儿'],
			['[丨丨].0', '[丨丨].1', '[丨丨]'],
			['[丨丿].0', '[丨丿].1', '[丨丿]'],
			['[丿丨].0', '[丿丨].1', '[丿丨]'],
			]
		return rearrangeList

