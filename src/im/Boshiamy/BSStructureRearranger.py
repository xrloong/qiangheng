from ..base.StructureRearranger import StructureRearranger
from im.gear import Operator

class BSStructureRearranger(StructureRearranger):

	def rearrangeSpecial(self, structDesc):
		operator=structDesc.getOperator()
		compList=structDesc.getCompList()
		lenCompList=len(compList)

		if operator.getName()=='鴻' and lenCompList>=2:
			firstChilStructDesc=compList[0]
			secondChilStructDesc=compList[1]

			firstName=firstChilStructDesc.getReferenceName()
			secondName=secondChilStructDesc.getReferenceName()

			secondeCompList=secondChilStructDesc.getCompList()
			if firstName=='彳' and len(secondeCompList)>=2:
				secondFirstChilStructDesc=secondeCompList[0]
				secondSecondChilStructDesc=secondeCompList[1]

				secondFirstName=secondFirstChilStructDesc.getReferenceName()
				secondSecondName=secondSecondChilStructDesc.getReferenceName()

				isMatch=(secondFirstName=='山' and secondSecondName=='一')

				if isMatch:
					newStructDesc=self.generateStructureDescriptionWithName('[特微]')
					newStructDesc_丨=self.generateStructureDescriptionWithName('丨')
					structDescList=[newStructDesc, newStructDesc_丨]+secondeCompList[2:]+compList[2:]
					structDesc.setCompList(structDescList)
					structDesc.setOperator(Operator.OperatorGoose)
			if secondName=='[䘗中]':
				newStructDesc=self.generateStructureDescriptionWithName('[特微]')
				newStructDesc_丨=self.generateStructureDescriptionWithName('丨')
				newStructDesc_糸=self.generateStructureDescriptionWithName('糸')
				structDescList=[newStructDesc, newStructDesc_丨, newStructDesc_糸]+compList[2:]
				structDesc.setCompList(structDescList)
				structDesc.setOperator(Operator.OperatorGoose)

		if operator.getName()=='範廖' and lenCompList>=2:
			firstChilStructDesc=compList[0]
			secondChilStructDesc=compList[1]

			firstName=firstChilStructDesc.getReferenceName()
			secondName=secondChilStructDesc.getReferenceName()
			if firstName=='厂' and secondName=='[辰下]':
				newStructDesc=self.generateStructureDescriptionWithName('[厂一]')
				newStructDesc_畏下=self.generateStructureDescriptionWithName('[畏下]')
				structDescList=[newStructDesc, newStructDesc_畏下]
				structDesc.setCompList(structDescList)
				structDesc.setOperator(Operator.OperatorGoose)

			if firstName=='厂' and secondName=='[一幺]':
				newStructDesc=self.generateStructureDescriptionWithName('[厂一]')
				newStructDesc_畏下=self.generateStructureDescriptionWithName('幺')
				structDescList=[newStructDesc, newStructDesc_畏下]
				structDesc.setCompList(structDescList)
				structDesc.setOperator(Operator.OperatorGoose)

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

